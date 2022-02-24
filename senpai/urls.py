from django.urls import path
from senpai import views

app_name = 'senpai'

urlpatterns = [
    # home page
    path('', views.home, name='home'),
    # user - my note
    path('mynote/<int:mynote_page_id>/', views.mynote, name='mynote'),
    path('mynote/', views.mynote, name='mynote'),
	path('mylike/',views.mylike, name='mylike'),
	path('note/<int:note_id>/delete/',views.delete_note,name='del_note'),
	path('mymodule/',views.mymodule, name='mymodule'),
    path('login/', views.user_login, name='login'),
	path('logout/',views.user_logout, name='logout'),
] 