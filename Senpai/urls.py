from django.urls import path
from senpai import views

app_name = 'senpai'

urlpatterns = [
    path('', views.index, name='index'),
    path('mynote/', views.mynote, name='mynote'),
] 