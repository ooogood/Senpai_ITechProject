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
## helper
import math

# Create your views here.
# home page
@login_required 
def home(request):
	context_dict = {}
	# add my modules to context_dict
	try:
		my_enrollments = Enrollment.objects.filter(user=request.user)
		context_dict['my_modules'] =Module.objects.filter(enrollment__in=my_enrollments) 
		context_dict['other_modules'] = Module.objects.exclude(enrollment__in=my_enrollments)
	except Exception:
		context_dict['my_modules'] = None
		context_dict['other_modules'] = None
	response = render( request, 'senpai/home.html', context=context_dict)
	return response
    
# user - my note
@login_required
def mynote(request,mynote_page_id=1):
	context_dict = {}
	if request.user.is_authenticated:
		# get note_list
		note_list = Note.objects.filter(user=request.user).order_by('date')[mynote_page_id*8-8:mynote_page_id*8]
		i = 1
		for n in note_list:
			cstring = 'c{a}'.format(a=i)
			i = i+1
			context_dict[cstring] = Comment.objects.filter(note=n).count()
		
		note_num = Note.objects.filter(user=request.user).count()
		page_maximum = math.ceil(note_num/8)
		context_dict['note'] = note_list
		context_dict['user'] = request.user
		context_dict['page'] = range(1,page_maximum+1)
	else:
		return render(request,'senpai/login_error.html')
	response = render(request,'senpai/mynote.html',context=context_dict)
	return response 

def user_login(request):
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		# We use request.POST.get('<variable>') as opposed
		# to request.POST['<variable>'], because the
		# request.POST.get('<variable>') returns None if the
		# value does not exist, while request.POST['<variable>']
		# will raise a KeyError exception.
		username = request.POST.get('username')
		password = request.POST.get('password')
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				return redirect(reverse('senpai:home'))
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your Rango account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print(f"Invalid login details: {username}, {password}")
			return HttpResponse("Invalid login details supplied.")
	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'senpai/login.html')
