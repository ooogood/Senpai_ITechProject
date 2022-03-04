import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
						'senpai_itech_project.settings')
import django
django.setup()
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
from django.contrib.auth.models import User
from django.core.files import File

def populate():
	Joseph_notes = [
	{'mod' : 'Programming', 'title' : 'Jotest_note1'},
	{'mod' : 'Programming', 'title' : 'Jotest_note2'},
	{'mod' : 'Software Engineering', 'title' : 'Jotest_note3'},
	{'mod' : 'Software Engineering', 'title' : 'Jotest_note4'},
	{'mod' : 'Cyber Security', 'title' : 'Jotest_note5'},
	{'mod' : 'Cyber Security', 'title' : 'Jotest_note6'},
	{'mod' : 'Cyber Security', 'title' : 'Jotest_note7'},
	]
	
	Jin_notes = [
	{'mod' : 'Programming', 'title' : 'Jitest_note1'},
	{'mod' : 'Programming', 'title' : 'Jitest_note2'},
	{'mod' : 'Internet Technology', 'title' : 'Jitest_note3'},
	{'mod' : 'Internet Technology', 'title' : 'Jitest_note4'},
	{'mod' : 'Internet Technology', 'title' : 'Jitest_note5'},
	{'mod' : 'Computer System', 'title' : 'Jitest_note6'},
	{'mod' : 'Computer System', 'title' : 'Jitest_note7'},
	{'mod' : 'Computer System', 'title' : 'Jitest_note8'},
	{'mod' : 'Computer System', 'title' : 'Jitest_note9'},
	{'mod' : 'Computer System', 'title' : 'Jitest_note10'},
	]
	
	Marco_notes = []
	Xiaowei_notes = []
	
	user_module = [
	{'uname': 'Joseph',
	'module':['Programming', 'Software Engineering', 'Cyber Security'],
	'notes':Joseph_notes,
	},
	{'uname': 'Jin',
	'module':['Programming', 'Internet Technology', 'Computer System'],
	'notes':Jin_notes,
	},
	{'uname': 'Marco',
	'module':['Computer Network', 'Human Computer Interface', 'Computer System'],
	'notes':Marco_notes,
	},
	{'uname': 'Xiaowei',
	'module':['Artificial Intelligence', 'Big Data', 'Digital Forensics'],
	'notes':Xiaowei_notes,
	},
	]
	
	# create and write a temperary example note file
	note_path = 'example_note.txt'
	example_note = open( note_path, 'w+' )
	example_note.write('Example note Example note\nExample Example \nnote note\nExample Example \nnote note\nExample Example \nnote note\nExample Example \nnote note\nExample Example \nnote note\nExample Example \nnote note\nExample Example \nnote note')
	example_note.close()
	
	# If you want to add more data, add them to the dictionaries above.
	i=1 # this line is used for add comments
	for um in user_module:
		u = add_user( um['uname'], 0 )
		for ms in um['module']:
			m = add_module(ms)
			add_enrollment(m, u)
			# note and comment add tests
			for ns in um['notes']:
				if ns['mod'] == m.name:
					n = add_note(m,u,ns['title'],note_path)
					for j in range(0,i+1):
						add_comment(n,u,'hello!'+str(i+j))
				i=i+1

	# delete temperary file
	os.remove(note_path)
		
	# Print out all data we have added.
	for u in User.objects.all():
		print(f'User: {u}')
        
	for m in Module.objects.all():
		print(f'Module: {m}')
    
	for n in Note.objects.all():
		print(f'Note: {n}')
		print(Comment.objects.filter(note=n).count())
	
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
def add_note(mod, user, title, note_path):
	# django will auto generate id
	# date will be auto generated
	n = Note.objects.get_or_create(module=mod, user=user, title=title)[0]
	# all note are associated to pdf/Design Specification.pdf for now
	fhandle = open( note_path, 'rb' )
	if fhandle:
		fcontent = File(fhandle)
		n.file.save((title+'.txt'), fcontent)
	fhandle.close()
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
