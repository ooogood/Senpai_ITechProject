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
	try:
		my_enrollments = Enrollment.objects.filter(user=this_user)
		context_dict['my_modules'] =Module.objects.filter(enrollment__in=my_enrollments) 
		context_dict['other_modules'] = Module.objects.exclude(enrollment__in=my_enrollments)
	except Exception:
		context_dict['my_modules'] = None
		context_dict['other_modules'] = None
	response = render( request, 'senpai/home.html', context=context_dict)
	return response
    
# user - my note
def mynote(request,mynote_page_id=1):
    context_dict = {}
    if request.user.is_authenticated:
        # get note_list
        note_list = Note.objects.filter(user=request.user).order_by('Date')[mynote_page_id*5-5:mynote_page_id*5]
        # note_num = Note.objects.filter(user=request.user).count()
        context_dict['note'] = note_list
        context_dict['user'] = request.user
        # context_dict['note_num'] = note_num
    else:
        return render(request,'senpai/login_error.html')
    response = render(request,'senpai/mynote.html',context=context_dict)
    return response 
