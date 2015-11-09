from django.forms import ModelForm
from wiki.models import Entry

from redactor.widgets import RedactorEditor

class EditForm(ModelForm):
    class Meta:
        model = Entry
        fields = ('content',)
        widgets = {
            'content': RedactorEditor(),
        }

    
class EntryForm(ModelForm):
    class Meta:
        model = Entry
        exclude = ('pass_audit', 'view_cnt', 'creator', 'up_count', 'down_count')
        widgets = {
            'content': RedactorEditor(),
        }
