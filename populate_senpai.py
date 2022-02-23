import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
						'senpai_itech_project.settings')
import django
django.setup()
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
from django.contrib.auth.models import User

def populate():
	user_module = [
	{'uname': 'Joseph',
	'module':['Programming', 'Software Engineering', 'Cyber Security'],
	},
	{'uname': 'Jin',
	'module':['Programming', 'Internet Technology', 'Computer System'],
	},
	{'uname': 'Marco',
	'module':['Computer Network', 'Human Computer Interface', 'Computer System'],
	},
	{'uname': 'Xiaowei',
	'module':['Artificial Intelligence', 'Big Data', 'Digital Forensics'],
	},
	]

	# If you want to add more data, add them to the dictionaries above.
	for um in user_module:
		u = add_user( um['uname'], 0 )
		for ms in um['module']:
			m = add_module(ms)
			add_enrollment(m, u)
	# Print out all data we have added.
	for u in User.objects.all():
		print(f'User: {u}')
	for m in Module.objects.all():
		print(f'Module: {m}')

def add_user(uname, r):
	email= uname + '@fakemail.com'
	pw = uname + 'isnumber1!'
	u = User.objects.get_or_create(username=uname, email=email)[0]
	u.set_password(pw)
	u.save()
	up = UserProfile.objects.get_or_create(user=u, role=r)[0]
	up.save()
	return u
def add_module(name):
	# django will auto generate id
	m = Module.objects.get_or_create(name=name)[0]
	m.save()
	return m
def add_note(mod, user, title):
	# django will auto generate id
	# date will be auto generated
	# file can be empty for testing. Make sure to change it back when deploying.
	n = Module.objects.get_or_create(module=mod, user=user, title=title)[0]
	n.save()
	return n
def add_enrollment(module, user):
	e = Enrollment.objects.get_or_create(module=module, user=user)[0]
	e.save()
	return e
def add_comment(note, user, content):
	# django will auto generate id
	c = Comment.objects.get_or_create(note=note, user=user, content=content)[0]
	c.save()
	return c
def add_like(user, note):
	# django will auto generate id
	l = Like.objects.get_or_create(user=user, note=note)[0]
	l.save()
	return l

# Start execution here!
if __name__ == '__main__':
	print('Starting Senpai population script...')
	populate()
