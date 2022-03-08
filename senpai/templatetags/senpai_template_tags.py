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