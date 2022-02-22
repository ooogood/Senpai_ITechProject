from django.shortcuts import render
from django.http import HttpResponse
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
## import modelForms
from django.shortcuts import redirect
from django.urls import reverse
## import userForms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
# home page
# todo: add @login_required 
def home(request):
	context_dict = {}
	# add my modules to context_dict
	this_user = request.user
	# try:
	# 	my_enrollments = Enrollment.objects.filter(user=this_user)
	# 	my_modules = 
	# 	context_dict['my_modules'] = my_modules
	# 	context_dict['other_modules'] = None
	# except Exception:
	# 	context_dict['my_modules'] = None
	# 	context_dict['other_modules'] = None
	response = render( request, 'senpai/home.html', context=context_dict)
	return response
# user - my note
def mynote(request):
    context_dict = {}
    if request.user.is_authenticated:
        note_list = Note.objects.filter(User=request.user).order_by('Date')[:5]
        context_dict['note'] = note_list
        context_dict['user'] = request.user
    else:
        return render(request,'users/login_error.html')
    response = render(request,'users/mynote.html',context=context_dict)
    return response 
