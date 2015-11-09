#-*- coding:utf-8 -*-
import datetime
from django.shortcuts import render, redirect, render_to_response
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from globe.utils import handle_uploaded_image
from django.http import HttpResponse
from django.db.models import Sum
from django.core.urlresolvers import reverse

from account.forms import *
from account.models import *
from wiki.models import *
import os
from django.conf import settings
from django.core.files.storage import default_storage
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test
from school.models import University

UPLOAD_PATH = getattr(settings, 'MEDIA_ROOT', 'media/')

def email_check(user):
    return user.checked

def signup(request):
    if request.method == 'POST':
        try:
            form = WikiUserRegisterForm(request.POST)
            try:
                univ = University.objects.all()[0]
                campus_name = univ.campus_name_en
            except:
                campus_name = "School Name"
            form.instance.campus_name = campus_name
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            login(request, user)
        except:
            form.error='valid error'
            return render_to_response('signup.html', RequestContext(request,{'form':form}))   
        
        return redirect('/ua/request_check/')
    
    elif request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('/')
        return render_to_response('signup.html', RequestContext(request))

def user_login(request, **kwargs):
    if request.method == 'POST':
        form = WikiUserLoginForm(request.POST)
        context = {'form':form}
        user = None

        if(form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                request.session.flush()
                login(request, user)

                if not user.checked:
                    return redirect('/ua/request_check/')

                prev = request.GET.get('next','/')
                return redirect(prev)
            else:
                error = 'User Forbiden'
                context['error'] = error
                return render_to_response('login.html', RequestContext(request,context))
        else:
            error = 'username/password error'
            context['error'] = error
            return render_to_response('login.html', RequestContext(request,context))
    elif request.method == 'GET':
        if request.user.is_authenticated():
            return redirect(reverse('ua:profile',kwargs={'user_id':request.user.pk}))
            
        return render_to_response('login.html', RequestContext(request))

def user_logout(request):
    logout(request)        
    return redirect('/')

@login_required            
@user_passes_test(email_check, login_url="/ua/request_check/")
def upload_head_url(request):
    if request.method == 'POST':
        form = WikiUserUploadIconForm(request.POST, request.FILES)             
        context = {'form':form}
        head_url = handle_uploaded_image(request.FILES['head_icon'])
        request.user.head_url = head_url
        request.user.save()
        return redirect(reverse('ua:profile',kwargs={'user_id':request.user.pk}))
    return redirect('/ua/login')    

@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
def edit_profile(request):
    if request.method == 'POST':
        wiki_user = WikiUser.objects.get(pk=request.user.pk)
        form = WikiUserEditForm(request.POST, request.FILES, instance=wiki_user)        
        if form.is_valid():
            form.save()
            #file_ = form.cleaned_data['head_icon']
            #path = os.path.join(UPLOAD_PATH, file_.name)
            #real_path = default_storage.save(path, file_)
            
            return redirect(reverse('ua:profile',kwargs={'user_id':request.user.pk}))
        else:
            return render_to_response('personal_edit.html', RequestContext(request, {'form':form}))
    else:
        return render_to_response('personal_edit.html', RequestContext(request, {'wiki_user':request.user,}))

    
def show_user(request, user_id='0'):
    for entry in Entry.objects.filter(saved=False):
        entry.delete()
    
    if True:#try:
        user = WikiUser.objects.get(pk=user_id)
        up_sum = user.created_entries.aggregate(Sum('up_count'))['up_count__sum']
        return render_to_response('personal.html', RequestContext(request, {'wiki_user':user,'up_sum':up_sum,}))
    else:#except:
        return render_to_response('404.html', RequestContext(request))

@login_required
def request_check(request):
    return render_to_response('check_email.html', RequestContext(request, {'wiki_user':request.user}))

from django.core.mail import send_mail
@login_required
def check(request, user_id='0', token=' '):
    if request.method == 'POST':
        try:
            user = WikiUser.objects.get(pk=user_id)
            user.link_expire_time = datetime.now() + timedelta(hours=5)
            user.save()
            link = request.build_absolute_uri(reverse('ua:check', kwargs={'user_id':user_id, 'token':user.check_string}))
            receiver = []
            receiver.append(user.email)
            try:
                send_mail("欢迎注册CollegeWiki，真实靠谱的校园百科平台", '欢迎您注册CollegeWiki，请点击以下链接完成注册：'+link+'                                                                         CollegeWiki团队敬上', 'wiki.cmu@gmail.com', receiver, fail_silently=True)
            except:
                pass
        except:
            pass
        return redirect(reverse('ua:edit'))
            
    else:
        try:
            user = WikiUser.objects.get(pk=user_id)
            if token == user.check_string:
                user.checked = True
                user.save()
        except:
            pass
        return redirect(reverse('ua:edit'))


def reset_password(request, user_id='0', token='@'):
    if request.method == 'POST':
        old_pwd = request.POST.get('old_pwd', '@')
        up_token = request.POST.get('token', '@')
        new_pwd = request.POST.get('new_pwd')
        try:
            username = WikiUser.objects.get(pk=user_id).username
            if up_token == '@':
                user = authenticate(username=username, password=old_pwd)
            else:
                user = WikiUser.objects.get(pk=user_id)
                if up_token != user.check_string:
                    user = None
            if user is not None:
                user.set_password(new_pwd)
                user.save()
                return render_to_response('reset_password_result.html', RequestContext(request,{'result':0})) 
        except:
            pass
        return render_to_response('reset_password_result.html', RequestContext(request,{'result':1})) 
    else:
        if token != '@':
            return render_to_response('password_reset.html', RequestContext(request, {'uid':user_id, 'token':token}))
        else:
            return render_to_response('password_reset.html', RequestContext(request, {'uid':user_id}))

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('username', '@')
        try:
            user = WikiUser.objects.get(username=email)
        except:
            return render_to_response('forget_password_result.html', RequestContext(request,{'result':1})) 
            
        user.link_expire_time = datetime.now() + timedelta(hours=5)
        user.save()
        link = request.build_absolute_uri(reverse('ua:reset_password', kwargs={'user_id':user.pk, 'token':user.check_string}))
        receiver = []
        receiver.append(user.email)
        try:
            send_mail('Wiki Reset Password', 'click '+link+' to reset password', 'wiki.cmu@gmail.com', receiver, fail_silently=True)
        except:
            return render_to_response('forget_password_result.html', RequestContext(request,{'result':-1})) 
        return render_to_response('forget_password_result.html', RequestContext(request,{'result':0})) 
    else:
        return render_to_response('password_forget.html', RequestContext(request))

@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
def message_center(request):
    return render_to_response('msg_center.html', RequestContext(request, {'wiki_user':request.user}))

@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
def send_message(request, receiver_id='0'):
    try:
        receiver = WikiUser.objects.get(pk=receiver_id)
    except:
        return render_to_response('404_user.html', RequestContext(request))

    if request.method == 'GET':
        message = Message(sender=request.user)
        form = MessageForm(instance=message)
        return render(request, 'send_mail.html', {'wiki_user':request.user, 'receiver':receiver, 'form':form})
    else:
        form = MessageForm(request.POST)
        form.instance.sender = request.user
        form.instance.receiver = receiver
        if form.is_valid():
            form.save()
            receiver.unread_cnt = receiver.unread_cnt + 1
            receiver.save()
            return render_to_response('msg_center.html', RequestContext(request, {'wiki_user':request.user}))
        return render_to_response('send_mail.html', {'wiki_user':request.user, 'receiver':receiver, 'form':form})    

@login_required
@user_passes_test(email_check, login_url="/ua/request_check/")
def view_message(request, user_id="0", msg_id="0"):
    if request.method == 'GET':
        try:
            msg = Message.objects.get(pk=msg_id)
        except:
            return render_to_response('view_mail.html', RequestContext(request, {'wiki_user':request.user, 'result':1, 'error':'Message dose not exist'}))
        if msg.receiver.pk == int(user_id) or msg.sender.pk == int(user_id):
            if msg.receiver.pk == int(user_id) and msg.read != True:
                msg.read = True
                msg.save()
                msg.receiver.unread_cnt = msg.receiver.unread_cnt - 1
                msg.receiver.save()
            return render_to_response('view_mail.html', RequestContext(request, {'wiki_user':request.user, 'result':0, 'msg':msg}))
        else:
            return render_to_response('view_mail.html', RequestContext(request, {'wiki_user':request.user, 'result':1, 'error':'Illegal operation'+'user_id='+str(user_id)+', receiver_id='+str(msg.receiver.pk)+', sender_id='+str(msg.sender.pk)}))
