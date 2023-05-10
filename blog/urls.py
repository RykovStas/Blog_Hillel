from django.urls import path
from blog import views


app_name = "blog"

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registerPage, name='reg'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('posts/', views.post_list, name='post_list'),
    path('profile/', views.profile, name='profile'),
    path('create_post/', views.create_post, name='create_post'),
]