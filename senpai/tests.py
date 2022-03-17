from django.test import TestCase,Client
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
from django.contrib.auth.models import User
from django.core.files import File


# Create your tests here.
# test method name should start with 'test_'
# to login in the test, write: self.client.login(username, password)
class ModelTests(TestCase):
    def test_models_all_default_auto_values(self):
        # test user is_admin
        u = add_user('JoJo')
        up = UserProfile.objects.get(user=u)
        self.assertEquals(up.is_admin, 0)
        self.assertEquals(up.admin_key, 0)
        # test module id, slug
        mod1 = add_module('Testing Module')
        mod2 = add_module('TestingModule')
        self.assertEqual(mod1.slug, "testing-module")
        self.assertEqual(mod1.id, 1)
        self.assertEqual(mod2.slug, "testingmodule")
        self.assertEqual(mod2.id, 2)
    # test note id, date, likes

    # test comment id, date
	
class RunningTest(TestCase):
	#test user can get access to home
	def test_home(self):
		u = add_user('TestUser')
		u.set_password('1')
		response = self.client.get('/senpai/')
		self.assertEqual(response.status_code,302)
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		response = self.client.get('/senpai/')
		self.assertEqual(response.status_code,200)
		
	def test_module(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		response = self.client.get('/senpai/module/testing-module/')
		self.assertEqual(response.status_code,200)
		
	def test_note(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		note1 = add_note(mod1,u,'testnote','example_note.pdf')
		url = '/senpai/note/'+str(note1.id)+'/'
		print(url)
		response = self.client.get(url)
		self.assertEqual(response.status_code,200)
		
	def test_mynote(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		response = self.client.get('/senpai/mynote/')
		self.assertEqual(response.status_code,200)
		
	def test_mymodule(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		response = self.client.get('/senpai/mymodule/')
		self.assertEqual(response.status_code,200)
		
	def test_mylike(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		response = self.client.get('/senpai/mylike/')
		self.assertEqual(response.status_code,200)

	def test_generatekey(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		response = self.client.get('/senpai/generateKey/')
		self.assertEqual(response.status_code,302)
		up = UserProfile.objects.get(user=u)
		up.is_admin = 1
		up.save()
		response = self.client.get('/senpai/generateKey/')
		self.assertEqual(response.status_code,200)
		
	def test_module_manage(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		response = self.client.get('/senpai/module-manage/')
		self.assertEqual(response.status_code,302)
		up = UserProfile.objects.get(user=u)
		up.is_admin = 1
		up.save()
		response = self.client.get('/senpai/module-manage/')
		self.assertEqual(response.status_code,200)
	
'''
 helper functions: add model objects
'''


def add_user(uname, is_admin=0):
    email = uname + '@fakemail.com'
    pw = uname + 'isnumber1!'
    u = User.objects.get_or_create(username=uname, email=email)[0]
    u.set_password(pw)
    u.save()
    up = UserProfile.objects.get_or_create(user=u)[0]
    up.is_admin = is_admin
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
    fhandle = open(note_path, 'rb')
    if fhandle:
        fcontent = File(fhandle)
        n.file.save((title + '.pdf'), fcontent)
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
    note.likes = note.likes + 1
    note.save()
    l.save()
    return l
