from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import BlogPost, BlogUser

class UserProfile(forms.ModelForm):
    class Meta:
        model = BlogUser
        fields = ['username', 'email', 'avatar']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = BlogUser
        fields = ['username', 'email', 'password1', 'password2']


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'image']


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=150, required=True)
    text = forms.CharField(widget=forms.Textarea, max_length=1000, required=True)