from django.db import models
from django.contrib.auth.models import AbstractUser


class BlogUser(AbstractUser):
    avatar = models.ImageField(default='static/images/default.png', upload_to='images')
    bio = models.TextField()

    def __str__(self):
        return self.username

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return 'static/images/default.png'


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{str(self.title)}. Author: {str(self.author)}'


class Comment(models.Model):
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

