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
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Dweet something...",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'text', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }