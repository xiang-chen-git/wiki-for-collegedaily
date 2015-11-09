#-*- coding:utf-8 -*-
from account.models import *
import json
from django.db.models import Q
from django.utils import simplejson
import re

import reversion
from reversion.diff_match_patch import diff_match_patch

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect

from django.core.urlresolvers import reverse

from wiki.forms import EditForm, EntryForm
from wiki.models import *
from redactor.widgets import RedactorEditor

from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_text

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import user_passes_test

def email_check(user):
    return user.checked

def patch_html(old_text, new_text):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(force_text(old_text), force_text(new_text))
    return dmp.diff_prettyHtml(diffs)

def index(request):
    hot_tags = HotTag.objects.order_by('-time_stamp')[:5]
    #view_most = Entry.objects.order_by('-view_cnt')[:5]
    #kaopu_most = Entry.objects.order_by('-up_count')[:5]
    #recent_most = Entry.objects.order_by('-time_stamp')[:5]
    #niu_most = WikiUser.objects.order_by('-kaopu_value')[:5]
    view_most = ViewMost.objects.order_by('-time_stamp')[:5]
    kaopu_most = KaopuMost.objects.order_by('-time_stamp')[:5]
    recent_most = RecentMost.objects.order_by('-time_stamp')[:5]
    niu_most = NiuMost.objects.order_by('-time_stamp')[:5]
    return render(request, 'index.html', {'hot_tags':hot_tags, 'view_most':view_most, 'kaopu_most':kaopu_most, 'recent_most':recent_most, 'niu_most':niu_most})

@login_required
def showform(request):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('wiki:index'))
    else:
        entry = Entry.objects.get(pk=1)
        form = EditForm(instance=entry)

    return render(request, 'wiki/showform.html', {
        'form':form,
    })

@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
def delete_entry(request, entry_id='0'):
    try:
        entry = Entry.objects.get(pk=entry_id)
    except:
        return render(request, '404.html')
    if entry.creator.pk == request.user.pk:
        reversion.revision.delete_for_object(entry)
        entry.delete()
    return redirect(reverse('ua:profile',kwargs={'user_id':request.user.pk,}))

@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
def edit_entry(request, entry_id='0'):
    if request.method == 'GET':
        try:
            entry = Entry.objects.get(pk=entry_id)
        except:
            #return render(request, 'wiki/entry_not_exist.html')
            entry = Entry(creator=request.user,saved=False)
            entry.save()
        form = EntryForm(instance=entry)
        return render(request, 'edit.html', {'form':form, 'entry':entry})
    else:
        entry_id = request.POST.get('entry_id', entry_id)
        comment = request.POST.get('comment', 'Content Modified')
        try:
            entry = Entry.objects.get(pk=entry_id)
        except:
            entry = Entry.objects.create(creator=request.user)
        if entry.saved != True:
            entry.saved = True
            comment = 'Entry created'

        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.instance.pass_audit = False
            form.instance.saved=True
            form.instance.ver_time = datetime.datetime.now()
            action = EditAction.objects.create(editor=request.user, entry=entry, comment=comment)
            with reversion.create_revision():
                reversion.default_revision_manager._post_save_receiver(instance=form.instance, created=True)
                reversion.set_user(request.user)
                reversion.set_comment(comment)

            if entry.creator.pk == request.user.pk:
                entry.pass_audit = True
                entry.saved = True
                entry.save() # comment to reversion
            else:
                message = Message(sender=request.user, receiver=entry.creator)
                message.title = 'Entry Modified'
                message.content = 'The entry:<br /><a href="/wiki/versions/'+str(entry.pk)+'/"><h2>'+entry.title+'</h2></a><br />You created have been modified, checkit out!'
                message.save()
                entry.creator.unread_cnt += 1
                entry.creator.save()

            return redirect(reverse('wiki:show', kwargs={'entry_id':entry.pk,}))
        return render_to_response('edit.html', RequestContext(request, {'form':form}))

def get_entry(request, entry_id='0', ver_id='0'):
    if request.method == 'GET':
        try:
            entry = Entry.objects.get(pk=entry_id)
        except:
            return render(request, 'wiki/entry_not_exist.html')
        vlist = reversion.get_for_object(entry)
        if ver_id != '0':
            try:
                ver = vlist.get(revision_id=ver_id)
            except:
                return render(request, 'wiki/version_not_exist.html')
            entry = ver.object_version.object
        entry.view_cnt += 1
        entry.save()
        return render_to_response('entry.html', RequestContext(request, {'entry':entry, }))
    else:
        return render(request, 'wiki/illegal_operation.html')

@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
def versions_entry(request, entry_id='0'):
    try:
        entry = Entry.objects.get(pk=entry_id)
    except:
        return render(request, 'wiki/entry_not_exist.html')
    if entry.creator.pk != request.user.pk:
        return HttpResponse('<a href="/"><h1>Operation not permitted!</h1></a>')

    vlist = reversion.get_for_object(entry)
    diff_html = patch_html(entry.content, entry.content)
    return render_to_response('reversion_diff.html', RequestContext(request, {'vlist':vlist,'diff_html':diff_html, 'entry':entry,'cur_ver':0,}))

@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
def revert_entry(request, entry_id='0', ver_id='0'):
    try:
        entry = Entry.objects.get(pk=entry_id)
    except:
        return render(request, 'wiki/entry_not_exist.html')
    if entry.creator.pk != request.user.pk:
        return HttpResponse('<a href="/"><h1>Operation not permitted!</h1></a>')
    vlist = reversion.get_for_object(entry)
    try:
        ver = vlist.get(revision_id=ver_id)
    except:
        return render(request, 'wiki/version_not_exist.html')
    if request.method == 'GET':
        new_entry = ver.object_version.object
        diff_html = patch_html(entry.content, new_entry.content)
        return render_to_response('reversion_diff.html', RequestContext(request, {'vlist':vlist, 'diff_html':diff_html, 'entry':new_entry, 'cur_ver':ver.revision_id,}))
    else:
        ver.revert()
        return redirect(reverse('wiki:show', kwargs={'entry_id':entry_id,}))

def search_suggest(request):
    output = []
    if request.method == 'GET':
        query = request.GET.get(u'term', '!@#$')
        qs = Entry.objects.filter(Q(title__startswith=query))
        output = [x.title for x in qs ]
        if len(output) == 0:
            qs = Entry.objects.filter(Q(title__icontains=query))
            output = [x.title for x in qs ]
    if len(output) == 0:
        output=['没有相关词条']

    output.sort()

    output = output[:8]
    json = simplejson.dumps(output)

    return HttpResponse(json, mimetype='application/json')


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def search_by_tag(request):
    if request.method == 'GET':
        query = request.GET.get(u'query', '!@#$')
        p = int(request.GET.get(u'p', '1'))
        paginator = None
        entry_list = []
        try:
            tag = Tag.objects.get(tag=query)
            entry_list = Ptag.entry_set.all()
            paginator = Paginator(entry_list, 15).page(p)
        except:
            pass
        return render_to_response('search.html', RequestContext(request, {'entry_list':paginator, 'query':query}))
    return render_to_response('search.html', RequestContext(request))

def search(request):
    if request.method == 'GET':
        query = request.GET.get(u'query', '!@#$')
        p = int(request.GET.get(u'p', '1'))
        entry_list = Entry.objects.filter(Q(title__startswith=query) | Q(title__icontains=query))
        paginator = Paginator(entry_list, 15).page(p)

        return render_to_response('search.html', RequestContext(request, {'entry_list':paginator, 'query':query}))
    return render_to_response('search.html', RequestContext(request))

def search_tag(request):
    if request.method == 'GET':
        query_tag = request.GET.get(u'tag', '!@#$')
        p = int(request.GET.get(u'p', '1'))
        paginator = None
        entry_list = []
        try:
            tag = Tag.objects.get(tag=query_tag)
            entry_list = tag.entry_set.all()
            paginator = Paginator(entry_list, 15).page(p)

        except:
            pass
        return render_to_response('search.html', RequestContext(request, {'entry_list':paginator,}))
    return render_to_response('search.html', RequestContext(request))

def vote_up(request, entry_id='0'):
    try:
        entry = Entry.objects.get(pk=entry_id)
        entry.up_count = entry.up_count + 1
        entry.save()
        # TODO
        entry.creator.kaopu_value += 1
        entry.creator.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('FAIL')

def vote_down(request, entry_id='0'):
    try:
        entry = Entry.objects.get(pk=entry_id)
        entry.down_count = entry.down_count + 1
        entry.save()
        # TODO
        entry.creator.bukaopu_value += 1
        entry.creator.save()
        return HttpResponse('OK')
    except:
        return HttpResponse('FAIL')

def suggest_tag(request):
    output = []
    if request.method == 'GET':
        query = request.GET.get(u'term', '!@#$')
        qs = Tag.objects.filter(Q(tag__startswith=query))
        output = [ {'id' : str(x.tag.encode('utf-8')), 'label' : str(x.tag.encode('utf-8')), 'value': str(x.tag.encode('utf-8')) } for x in qs ]
        if len(output) == 0:
            qs = Tag.objects.filter(Q(tag__icontains=query))
            output = [ {'id' : x.tag, 'label' : x.tag, 'value': x.tag } for x in qs ]
    if len(output) == 0:
        output=[]

    output.sort()

    output = output[:8]
    json = simplejson.dumps(output)

    return HttpResponse(json, mimetype='application/json')


def suggest_link(request):
    output = []
    if request.method == 'GET':
        query = request.GET.get(u'term', '!@#$')
        qs = Entry.objects.filter(Q(title__startswith=query) & Q(saved=True) )
        output = [ {'key' : x.title, 'value': x.pk } for x in qs ]
        if len(output) == 0:
            qs = Entry.objects.filter(Q(title__icontains=query))
            output = [{'value': x.pk, 'key' : x.title} for x in qs ]
    if len(output) == 0:
        output=[]
    output.sort()

    output = output[:8]
    json = simplejson.dumps(output)

    return HttpResponse(json, mimetype='application/json')


@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
def add_tag(request, entry_id='0'):
    if request.method == 'GET':
        tg = request.GET.get(u'tag', '!@#$')
        try:
            tag = Tag.objects.get(tag=tg)
        except:
            tag = Tag.objects.create(tag=tg)
        try:
            entry = Entry.objects.get(pk=entry_id)
            entry.tags.add(tag)
            return HttpResponse('OK')
        except:
            return HttpResponse('Fail')
    else:
        return HttpResponse('Fail')

@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
def remove_tag(request, entry_id='0'):
    if request.method == 'GET':
        tg = request.GET.get(u'tag', '!@#$')
        try:
            entry = Entry.objects.get(pk=entry_id)
            tag = Tag.objects.get(tag=tg)
            entry.tags.remove(tag)
            return HttpResponse('OK')
        except:
            return HttpResponse('Fail')
    else:
        return HttpResponse('Fail')

UPLOAD_PATH = getattr(settings, 'MEDIA_ROOT', 'media/')+"attach/"

@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
@csrf_exempt
def upload_attach(request, entry_id=0):
    resp = []
    try:
        afile = request.FILES['myfile']
        my_path = UPLOAD_PATH + entry_id + "/"
        filename = afile.name
        path = os.path.join(my_path, filename)
        real_path = default_storage.save(path, afile)
        resp.append(filename)

        entry = Entry.objects.get(pk=entry_id)
        try:
            attach = entry.attachments.get(filename__exact=filename)
        except:
            attach = Attachments.objects.create(entry=entry, filename=filename)
    except:
        pass
    json = simplejson.dumps(resp)
    return HttpResponse(json)

@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
@csrf_exempt
def delete_attach(request, entry_id=0):
    resp = []
    try:
        filename = request.POST['name']
        try:
            entry = Entry.objects.get(pk=entry_id)
            attach = entry.attachments.get(filename__exact=filename)
            attach.delete()
        except:
            pass
        my_path = UPLOAD_PATH + entry_id + "/"
        path = os.path.join(my_path, filename)
        real_path = default_storage.delete(path)
        resp.append(filename)
    except:
        pass
    json = simplejson.dumps(resp)
    return HttpResponse(json)

