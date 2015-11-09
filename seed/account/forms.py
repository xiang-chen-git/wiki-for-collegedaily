from models import WikiUser, Message
from django import forms
from globe import utils

# TODO exist email or usernames
class WikiUserRegisterForm(forms.ModelForm):
    class Meta:
        model = WikiUser
        fields = ('nickname','email', 'password', 'username')

    def clean(self):
        cleaned_data = super(WikiUserRegisterForm, self).clean()
        cleaned_data['email'] = cleaned_data['username']
        if not utils.validatePwd(cleaned_data.get('password')):
            self._errors['password'] = 'Illegal password format'
            raise forms.ValidationError('Invalid password')
        return cleaned_data

    def save(self, commit=True):
        user = super(WikiUserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user    

class WikiUserEditForm(forms.ModelForm):
    class Meta:
        model = WikiUser
        fields = ('head_icon', 'status', 'major', 'minor','renren_link', 'facebook_link', 'twitter_link', 'linkedin_link', 'weibo_link')
        
class WikiUserLoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64)        

    def clean(self):
        cleaned_data = super(WikiUserLoginForm, self).clean()
        if not utils.validatePwd(cleaned_data.get('password')):
            #self._errors['password'] = 'Illegal password format'
            raise forms.ValidationError('Invalid password')
        return cleaned_data

class WikiUserUploadIconForm(forms.Form):
    head_icon = forms.FileField()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'content')
