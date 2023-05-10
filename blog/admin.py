from django.contrib import admin
from .models import BlogUser

@admin.register(BlogUser)
class BlogUserAdmin(admin.ModelAdmin):
    pass