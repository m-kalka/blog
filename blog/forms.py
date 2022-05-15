from django import forms
from .models import Post

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'user',
            'title',
            'content'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].disabled=True
        #self.fields['user'].widget=forms.HiddenInput()

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class MetaRegister:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 20)
	last_name = forms.CharField(max_length = 20)    
	email_address = forms.EmailField(max_length = 50)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)