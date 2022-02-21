from django.urls import path
from rango import views

app_name = 'rango'
LOGIN_URL = 'rango:login'

urlpatterns = [
    path('', views.index, name='index'),
    path('mynote/', views.mynote, name='mynote'),
]