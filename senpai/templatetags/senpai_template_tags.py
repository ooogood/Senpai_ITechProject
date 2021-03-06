from django import template
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
from django.db.models import Count
import hashlib
from time import time

register = template.Library()

# get a value from dictuionary according to key in templates
@register.filter
def get_dict_item(dic, key):
	return dic.get( key )

# get username
@register.filter
def get_username(user):
	return user.username

# for home page #
# get module lists for home page
@register.inclusion_tag('senpai/home_modules.html')
def get_home_modules(user, query=''):
	context_dict = {}
	# if this is not a search request
	# get normal home page: my_modules / other_modules
	if query == '':
		# get my modules
		my_enrollments = Enrollment.objects.filter(user=user)
		context_dict['my_modules'] = Module.objects.filter(enrollment__in=my_enrollments).order_by('name')
		my_dict = {}
		for mod in context_dict['my_modules']:
			# module name as my_dict's key and map to a note list
			my_dict[ mod.name ] = get_three_notes_list(mod)
		context_dict['my_modules_dict'] = my_dict
		# get other modules
		context_dict['other_modules'] = Module.objects.exclude(enrollment__in=my_enrollments).order_by('name')
		other_dict = {}
		for mod in context_dict['other_modules']:
			# module name as other_dict's key and map to a note list
			other_dict[ mod.name ] = get_three_notes_list(mod)
		context_dict['other_modules_dict'] = other_dict
	# if this is a search request
	else:
		# get search result
		context_dict['search_results'] = Module.objects.filter(name__icontains=query).order_by('name')
		search_dict = {}
		for mod in context_dict['search_results']:
			# module name as other_dict's key and map to a note list
			search_dict[ mod.name ] = get_three_notes_list(mod)
		context_dict['search_dict'] = search_dict 
		context_dict['is_search_result'] = 'true'
	return context_dict

# helper function: get 3 most liked notes in this module
def get_three_notes_list(module):
	note_list = []
	for note in Note.objects.filter(module=module).order_by("-likes")[:3]:
		note_list.append( note )
	return note_list

# for module pages #
# get note list for this module page
@register.inclusion_tag('senpai/notelist.html')
def get_sorted_notes(module=None, sort_type='lik'):
	note_dict = {}
	# get all note for this module first
	notes = Note.objects.filter(module=module)
	for note in notes:
		cnt = Comment.objects.filter(note=note).count()
		note_dict[ note.title ] = cnt
	# sort the result according to input argument
	if sort_type == 'lik':
		notes = notes.order_by('-likes')
	elif sort_type == 'cmt':
		notes = Note.objects.filter(module=module).annotate(cmtcnt=Count('comment')).order_by('-cmtcnt')
	elif sort_type == 'new':
		notes = notes.order_by('-date')
	elif sort_type == 'old':
		notes = notes.order_by('date')
	return {'notes': notes,
			'note_dict': note_dict}

# for note pages #
# get all comments for this note page
@register.inclusion_tag('senpai/commentlist.html')
def get_comments(note, user):
	context_dict = {}
	all_cmt = Comment.objects.filter(note=note).order_by('-date')
	context_dict['comments'] = all_cmt
	context_dict['user'] = user
	return context_dict
	
# for mynote page #
# get all notes that this user uploaded, including their comment counts
@register.inclusion_tag('senpai/mynote_notes.html')
def get_mynote_notes(user):
	context_dict = {}
	note_list = Note.objects.filter(user=user).order_by('-date')
	comment = {}
	for n in note_list:
		comment[n.id] = Comment.objects.filter(note=n).count()
		
	context_dict['notes'] = note_list
	context_dict['comments'] = comment
	return context_dict
	
# for mymodule page #
# get all modules that the user has enrolled
@register.inclusion_tag('senpai/mymodule_usermodules.html')
def get_mymodule_usermodules(user):
	context_dict = {}
	# get user module_list
	my_enrollment = Enrollment.objects.filter(user=user)
	context_dict['user_modules'] = Module.objects.filter(enrollment__in=my_enrollment).order_by('name')
	context_dict['user']=user
	return context_dict

# get all modules that the user hasn't enrolled
@register.inclusion_tag('senpai/mymodule_othermodules.html')
def get_mymodule_othermodules(user):
	context_dict = {}
	# get other module_list
	my_enrollment = Enrollment.objects.filter(user=user)
	context_dict['other_modules'] = Module.objects.exclude(enrollment__in=my_enrollment).order_by('name')
	context_dict['user']=user
	return context_dict
	
# for module management page #
# get all modules in this website
@register.inclusion_tag('senpai/management_module_list.html')
def get_all_module_list():
	context_dict = {}
	context_dict['modules'] = Module.objects.all().order_by('name')
	return context_dict

# for generate admin key page #
# generate new admin key for this user
def gen_admin_key(userprofile):
    code = hashlib.md5(str(time()).encode("utf-8"))
    key = code.hexdigest()[:-10]
    userprofile.admin_key = key

# return true if this user is an admin
def is_admin(user):
	return ( UserProfile.objects.get(user=user).is_admin == 1 )
