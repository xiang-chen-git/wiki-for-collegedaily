import os

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
#from django.core.files.storage import default_storage
from globe.utils import OverwriteStorage
default_storage = OverwriteStorage()
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from redactor.forms import ImageForm

from django.utils import simplejson

UPLOAD_PATH = getattr(settings, 'REDACTOR_UPLOAD', 'redactor/')


@csrf_exempt
@require_POST
#@user_passes_test(lambda u: u.is_staff)
def redactor_upload(request, upload_to=None, form_class=ImageForm,
                    response=lambda name, url: url):
    form = form_class(request.POST, request.FILES)
    if form.is_valid():
        file_ = form.cleaned_data['file']
        path = os.path.join(upload_to or UPLOAD_PATH, file_.name)
        real_path = default_storage.save(path, file_)
        resp = {}
        resp['filelink'] = os.path.join(settings.MEDIA_URL, real_path)
        return HttpResponse(simplejson.dumps(resp)) 
        return HttpResponse(
            response(file_.name, os.path.join(settings.MEDIA_URL, real_path))
        )
    return HttpResponse(status=403)
