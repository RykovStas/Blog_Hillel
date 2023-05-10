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