from django.urls import path
from blog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reg/', views.index, name='reg')
]