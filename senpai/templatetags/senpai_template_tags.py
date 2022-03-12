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
		search_dict = {}
		for mod in context_dict['search_results']:
			# module name as other_dict's key and map to a note list
			search_dict[ mod.name ] = get_three_notes_list(mod)
		context_dict['search_dict'] = search_dict 
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
		notes = notes.order_by('-likes')
	elif sort_type == 'cmt':
		notes = Note.objects.filter(module=module).annotate(cmtcnt=Count('comment')).order_by('-cmtcnt')
	elif sort_type == 'new':
		notes = notes.order_by('-date')
	elif sort_type == 'old':
		notes = notes.order_by('date')
	print(notes)
	return {'notes': notes,
			'note_dict': note_dict}

# for note pages
@register.inclusion_tag('senpai/commentlist.html')
def get_comments(note, user, cmt_page=1):
	context_dict = {}
	cmt_per_page = 6
	start_idx = cmt_per_page * (cmt_page - 1)
	end_idx = cmt_per_page * (cmt_page)
	all_cmt = Comment.objects.filter(note=note).order_by('-date')
	context_dict['comments'] = all_cmt[start_idx:end_idx]
	context_dict['cmt_page_num'] = cmt_page
	context_dict['has_prev'] = (cmt_page > 1)
	context_dict['has_next'] = (end_idx < all_cmt.count())
	context_dict['user'] = user
	return context_dict
	
# for mynote page
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
	
@register.inclusion_tag('senpai/mymodule_modules.html')
def get_mymodule_modules(user):
	context_dict = {}
	my_module = []
	other_module = []
	# get module_list
	my_enrollment = Enrollment.objects.filter(user=user)
	for e in my_enrollment:
		my_module.append(e.module)

	all_modules = Module.objects.all()
	for m in all_modules:
		if not m in my_module:
			other_module.append(m)
		
	context_dict['user_modules']=my_module
	context_dict['other_modules']=other_module
	context_dict['user']=user
	
	return context_dict