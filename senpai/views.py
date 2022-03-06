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
		context_dict['my_modules'] = Module.objects.filter(enrollment__in=my_enrollments) 
		# get 3 notes for each my_modules
		my_dict = {}
		for mod in context_dict['my_modules']:
			# module name as my_dict's key and map to a note list
			note_list = []
			for note in Note.objects.filter(module=mod).order_by("-likes")[:3]:
				note_list.append( note )
			my_dict[ mod.name ] = note_list
		context_dict['my_modules_dict'] = my_dict
		context_dict['other_modules'] = Module.objects.exclude(enrollment__in=my_enrollments)
		other_dict = {}
		for mod in context_dict['other_modules']:
			# module name as other_dict's key and map to a note list
			note_list = []
			for note in Note.objects.filter(module=mod).order_by("-likes")[:3]:
				note_list.append( note )
			other_dict[ mod.name ] = note_list
		context_dict['other_modules_dict'] = other_dict
		# get 3 notes for each other_modules
	except Exception:
		context_dict['my_modules'] = None
		context_dict['other_modules'] = None
	response = render( request, 'senpai/home.html', context=context_dict)
	return response
# module page
@login_required 
def show_module(request, module_name_slug):
	context_dict = {}
	note_dict = {}
	try:
		module = Module.objects.get(slug=module_name_slug)
		notes = Note.objects.filter(module=module)
		context_dict['module'] = module
		context_dict['notes'] = notes
		context_dict['all_modules'] = Module.objects.all()
		# calculate comment count for each note
		for note in notes:
			cnt = Comment.objects.filter(note=note).count()
			note_dict[ note.title ] = cnt
		context_dict['note_dict'] = note_dict
	except Module.DoesNotExist:
		context_dict['module'] = None
		context_dict['notes'] = None
		context_dict['all_modules'] = None
		context_dict['note_dict'] = None
	return render(request, 'senpai/module.html', context=context_dict)
# note page
@login_required 
def show_note(request, note_id):
	context_dict = {}
	try:
		context_dict['note'] = Note.objects.get(id=note_id)
		context_dict['module'] = context_dict['note'].module
		context_dict['comments'] = Comment.objects.filter(note=context_dict['note'])
	except Note.DoesNotExist:
		context_dict['module'] = None
		context_dict['note'] = None
		context_dict['comments'] = None
	return render(request, 'senpai/note.html', context=context_dict)
# user - my note
@login_required
def mynote(request,mynote_page_id=1):
	context_dict = {}
	if request.user.is_authenticated:
		# get note_list
		note_list = Note.objects.filter(user=request.user).order_by('date')[mynote_page_id*8-8:mynote_page_id*8]
		comment = {}
		for n in note_list:
			comment[n.id] = Comment.objects.filter(note=n).count()
		
		note_num = Note.objects.filter(user=request.user).count()
		page_maximum = math.ceil(note_num/8)
		context_dict['note'] = note_list
		context_dict['user'] = request.user
		context_dict['page'] = range(1,page_maximum+1)
		context_dict['page_now'] = mynote_page_id
		context_dict['page_last'] = mynote_page_id-1
		context_dict['page_next'] = mynote_page_id+1
		context_dict['comments'] = comment
	else:
		return render(request,'senpai/login_error.html')
	response = render(request,'senpai/mynote.html',context=context_dict)
	return response 
	
# user - mylike
@login_required
def mylike(request,mylike_page_id=1):	
	context_dict = {}
	if request.user.is_authenticated:
		# get note_list
		like_list = Like.objects.filter(user=request.user)[mylike_page_id*8-8:mylike_page_id*8]
		note = []
		for likes in like_list:
			note.append(likes.note)
			
		like_num = Like.objects.filter(user=request.user).count()
		page_maximum = math.ceil(like_num/8)
		context_dict['note'] = like_list
		context_dict['user'] = request.user
		context_dict['page'] = range(1,page_maximum+1)
		context_dict['page_now'] = mylike_page_id
		context_dict['page_last'] = mylike_page_id-1
		context_dict['page_next'] = mylike_page_id+1
	else:
		return render(request,'senpai/login_error.html')
	response = render(request,'senpai/mylike.html',context=context_dict)
	return response 

@login_required
def mymodule(request):
	response = HttpResponse('developing')
	return response 

@login_required
def delete_note(request,note_id):
	next = request.GET.get('next','/senpai/mynote/');
	
	if Note.objects.filter(id=note_id).exists():
		Note.objects.filter(id=note_id).delete()
	
	return redirect(next)
	
# login
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

@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('senpai:login'))