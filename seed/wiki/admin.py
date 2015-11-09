from django.contrib import admin
from django.contrib.contenttypes.generic import GenericStackedInline

from reversion.admin import VersionAdmin

from wiki.models import *

class EntryAdmin(VersionAdmin):
    pass

admin.site.register(Entry, EntryAdmin)    
admin.site.register(Tag)
admin.site.register(HotTag)
admin.site.register(ViewMost)
admin.site.register(KaopuMost)
admin.site.register(RecentMost)
admin.site.register(NiuMost)

