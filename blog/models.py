from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.TextField()
    text = models.TextField(blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'{str(self.title)}. Author: {str(self.author)}'


class UserModel(User):
    # add custom fields or methods here
    pass