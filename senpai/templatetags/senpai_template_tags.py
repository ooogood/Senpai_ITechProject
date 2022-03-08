from django import template
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
from django.db.models import Count

register = template.Library()

@register.filter
def get_dict_item(dic, key):
	return dic.get( key )
@register.filter
def get_username(user):
	return user.username

# for home page
@register.inclusion_tag('senpai/home_modules.html')
def get_home_modules(user, query=''):
	context_dict = {}
	# get normal home page: my_modules / other_modules
	if query == '':
		# get my modules
		my_enrollments = Enrollment.objects.filter(user=user)
		context_dict['my_modules'] = Module.objects.filter(enrollment__in=my_enrollments) 
		my_dict = {}
		for mod in context_dict['my_modules']:
			# module name as my_dict's key and map to a note list
			my_dict[ mod.name ] = get_three_notes_list(mod)
		context_dict['my_modules_dict'] = my_dict
		# get other modules
		context_dict['other_modules'] = Module.objects.exclude(enrollment__in=my_enrollments)
		other_dict = {}
		for mod in context_dict['other_modules']:
			# module name as other_dict's key and map to a note list
			other_dict[ mod.name ] = get_three_notes_list(mod)
		context_dict['other_modules_dict'] = other_dict
	else:
		# get search result
		context_dict['search_results'] = Module.objects.filter(name__istartswith=query)
		context_dict['is_search_result'] = 'true'
	return context_dict

# helper function
def get_three_notes_list(module):
	note_list = []
	for note in Note.objects.filter(module=module).order_by("-likes")[:3]:
		note_list.append( note )
	return note_list

# for module pages
@register.inclusion_tag('senpai/notelist.html')
def get_sorted_notes(module=None, sort_type='lik'):
	note_dict = {}
	notes = Note.objects.filter(module=module)
	for note in notes:
		cnt = Comment.objects.filter(note=note).count()
		note_dict[ note.title ] = cnt
	# sort the result
	if sort_type == 'lik':
		notes.order_by('-likes')
	elif sort_type == 'cmt':
		notes = Note.objects.filter(module=module).annotate(cmtcnt=Count('comment')).order_by('-cmtcnt')
	elif sort_type == 'new':
		notes.order_by('-date')
	elif sort_type == 'old':
		notes.order_by('date')
	return {'notes': notes,
			'note_dict': note_dict}