#-*-coding:utf-8-*-
import os
import re
import time
import base64
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def validatePwd(pwd):
    valid_password_regex = re.compile(r"^([\~\!\@\#\$\%\^\&\*\(\)\_\+\`\-\=\[\]\\\{\}\|\;\'\:\"\<\>\?\,\.\/a-zA-Z0-9]{1,})$")
    r = valid_password_regex.match(pwd)
    return r!=None
    
def handle_uploaded_image(image):
    file_name = base64.b64encode(image.name + time.strftime('%m/%d/%Y %H:%M:%S'))+'.jpg' 
    with open('media/head_icon/'+file_name, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)
        return '/media/head_icon/'+filer_name                

def update_uploaded_filename(instance, filename):
    path = "head_icon/"
    ext = filename.split('.')[-1]
    file_name = base64.b64encode(filename.encode('utf-8') + time.strftime('%m/%d/%Y %H:%M:%S'))+'.' + ext 
    return os.path.join(path, file_name)

def upload_corner(instance, filename):
    path = "univ/"
    ext = filename.split('.')[-1]
    file_name = "logo.png" 
    full_name = os.path.join(path, file_name)
    if os.path.exists(full_name):
        os.remove(full_name)
    return full_name    

def upload_logo(instance, filename):
    path = "univ/"
    ext = filename.split('.')[-1]
    file_name = "logo.jpg" 
    full_name = os.path.join(path, file_name)
    if os.path.exists(full_name):
        os.remove(full_name)
    return full_name    

def upload_background(instance, filename):
    path = "univ/"
    ext = filename.split('.')[-1]
    file_name = "background.jpg" 
    full_name = os.path.join(path, file_name)
    if os.path.exists(full_name):
        os.remove(full_name)
    return full_name    

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        if self.exists(name):
            self.delete(name)
        return name    
