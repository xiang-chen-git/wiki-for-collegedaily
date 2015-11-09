import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello.settings")
from django.contrib.auth.models import Group

Group.objects.all().delete()
Group.objects.create(name="Normal User")
Group.objects.create(name="Entry Admin")
Group.objects.create(name="User Admin")
Group.objects.create(name="Super User")
