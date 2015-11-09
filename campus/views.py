from django.views.decorators.csrf import csrf_exempt
import subprocess

from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

from campus.models import Subdomain
import os
# TODO to be replaced with your own domain name
DOMAIN = 'hackit.cn'
sudopwd = 'root_password'
def create_site(request):
    response = {}
    campus = ''
    campus_name = ''
    response['result'] = -1
    if request.method == 'POST':
        campus = request.POST.get('sub_domain', 'sample').lower()
        campus_name = request.POST.get('campus_name', 'Sample')
        delete = request.POST.get('delete', False)
        if delete == False:
            command = '/home/jiaqing/webapps/admin_campus/new_school.sh ' + campus
        else:
            command = '/home/jiaqing/webapps/admin_campus/del_school.sh ' + campus
    
        res = os.system('echo %s|sudo -S %s' % (sudopwd, command))
        if res == 0:
            domain = "http://"+campus+"."+DOMAIN
            univs = Subdomain.objects.filter(subdomain=campus)
            for univ in univs:
                univ.delete()

            if delete == False:
                univ = Subdomain.objects.create(domain=domain, campus_name_en=campus_name, subdomain=campus)
                univ.weight = 1
                univ.to_create = False
                univ.logo_url = "http://"+campus+"."+DOMAIN+"/media/univ/logo.jpg"
                univ.save()

            return redirect("http://"+campus+"."+DOMAIN)
        else:
            return render_to_response("new_domain.html", RequestContext(request, {'sub_domain':campus, 'campus_name':campus_name}))
    else:
        return render_to_response("new_domain.html", RequestContext(request, {'sub_domain':campus, 'campus_name':campus_name}))
       
def refresh(request):
    to_del = Subdomain.objects.filter(to_delete=True)
    for univ in to_del:
        try:
            command = '/home/jiaqing/webapps/admin_campus/del_school.sh ' + univ.subdomain 
            res = os.system('echo %s|sudo -S %s' % (sudopwd, command))
            univ.delete()
        except:
            pass

    to_create = Subdomain.objects.filter(to_create=True)
    for univ in to_create:
        try:
            command = '/home/jiaqing/webapps/admin_campus/new_school.sh ' + univ.subdomain
            res = os.system('echo %s|sudo -S %s' % (sudopwd, command))
            if res == 0:
                domain = "http://"+univ.subdomain+"."+DOMAIN
                univ.domain = domain
                univ.logo_url = "http://"+univ.subdomain+"."+DOMAIN+"/media/univ/logo.jpg"
                univ.weight = 1
                univ.to_create = False
                univ.save()
        except:
            pass
    return HttpResponse('<a href="/"><h1>Refresh Accomplished!</h1></a>')

def index(request):
    univs = Subdomain.objects.filter(weight__gte=1).order_by("-weight")
    return render_to_response("index.html", RequestContext(request, {'count':univs.count(), 'univs':univs}))
    
