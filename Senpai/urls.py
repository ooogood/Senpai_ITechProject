from django.urls import path
from senpai import views

app_name = 'senpai'

urlpatterns = [
    # home page
    path('', views.home, name='home'),
    # user - my note
    path('mynote/', views.mynote, name='mynote'),
] 