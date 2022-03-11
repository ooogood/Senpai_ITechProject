from django.urls import path
from senpai import views

app_name = 'senpai'

urlpatterns = [
    # home page
    path('', views.HomePage.as_view(), name='home'),
    # module page
    path('module/<slug:module_name_slug>/', views.ModulePage.as_view(), name='show_module'),
    path('module/<slug:module_name_slug>/upload_note', views.upload_note, name='upload_note'),
    # note page
    path('note/<int:note_id>', views.NotePage.as_view(), name='show_note'),
    path('note/<int:note_id>/like_clicked', views.note_like_clicked, name='note_like_clicked'),
    path('note/<int:note_id>/download', views.note_download, name='note_download'),
    # user - my note
    path('mynote/<int:mynote_page_id>/', views.Mynote.as_view(), name='mynote'),
    path('mynote/', views.Mynote.as_view(), name='mynote'),
    # my like
    path('mylike/', views.mylike, name='mylike'),
    path('mylike/<int:mylike_page_id>/', views.mylike, name='mylike'),
    # note delete
    path('note/<int:note_id>/delete/', views.delete_note, name='del_note'),
    # my module
    path('mymodule/', views.mymodule, name='mymodule'),
    path('unenrollment/<int:module_id>/', views.unenrollment, name='del_module'),
    path('enrollment/<int:module_id>/', views.enrollment, name='add_module'),
    # register/log
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
]
