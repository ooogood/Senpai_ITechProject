from django.test import TestCase,Client
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
from django.contrib.auth.models import User
from django.core.files import File
from django.urls import reverse
from datetime import datetime

from senpai.templatetags.senpai_template_tags import gen_admin_key


# Create your tests here.
# test method name should start with 'test_'
# to login in the test, write: self.client.login(username, password)
class ModelTests(TestCase):
    def test_models_all_default_auto_values(self):
        # test user is_admin
        u = add_user('JoJo')
        up = UserProfile.objects.get(user=u)
        self.assertEquals(up.is_admin, 0)
        self.assertEquals(up.admin_key, None)
        # test module id, slug
        mod1 = add_module('Testing Module')
        mod2 = add_module('TestingModule')
        self.assertEqual(mod1.slug, "testing-module")
        self.assertEqual(mod1.id, 1)
        self.assertEqual(mod2.slug, "testingmodule")
        self.assertEqual(mod2.id, 2)
    # test note id, date, likes
        note1 = add_note(mod1,u,'testnote','example_note.pdf')
        note2 = add_note(mod2,u,'testnote2','example_note.pdf')
        date = datetime.now()
        self.assertEqual(note1.id, 1)
        self.assertEqual(note2.id, 2)
        self.assertEqual(note1.date.isocalendar(), date.isocalendar())
        self.assertEqual(note2.date.isocalendar(), date.isocalendar())
        self.assertEqual(note1.likes, 0)
        self.assertEqual(note2.likes, 0)
        
        add_like(u,note1)
        self.assertEqual(note1.likes, 1)
        self.assertEqual(note2.likes, 0)

    # test comment id, date
        comment1 = add_comment(note1,u,'Good')
        comment2 = add_comment(note1,u,'Good!')
        date = datetime.now()
        self.assertEqual(comment1.id, 1)
        self.assertEqual(comment2.id, 2)
        self.assertEqual(note1.date.isocalendar(), date.isocalendar())
        self.assertEqual(note2.date.isocalendar(), date.isocalendar())
	
class PageAvailabilityTest(TestCase):
	#test user can get access to home
	def test_home(self):
		
		#if not logged in, user would be redirect
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,302)
		
		#else, they can get access to home
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,200)
		
	#test user can get access to module page
	def test_module(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		
		response = self.client.get(reverse('senpai:show_module',kwargs={'module_name_slug':mod1.slug}))
		self.assertEqual(response.status_code,200)
	
	#test user can get access to note page	
	def test_note(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		note1 = add_note(mod1,u,'testnote','example_note.pdf')
		url = reverse('senpai:show_note',kwargs={'note_id':note1.id})
		
		response = self.client.get(url)
		self.assertEqual(response.status_code,200)
	
	#test user can get access to mynote page	
	def test_mynote(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		
		response = self.client.get(reverse('senpai:mynote'))
		self.assertEqual(response.status_code,200)
	
	#test user can get access to mymodule page		
	def test_mymodule(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		
		response = self.client.get(reverse('senpai:mymodule'))
		self.assertEqual(response.status_code,200)
	
	#test user can get access to mylike page
	def test_mylike(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		
		response = self.client.get(reverse('senpai:mylike'))
		self.assertEqual(response.status_code,200)

	def test_generatekey(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		# test if non admin can access admin generation page
		response = self.client.get(reverse('senpai:genAdminKey'))
		self.assertEqual(response.status_code,302)
		up = UserProfile.objects.get(user=u)
		up.is_admin = 1
		up.save()
		# test if admin can access admin generation page
		response = self.client.get(reverse('senpai:genAdminKey'))
		self.assertEqual(response.status_code,200)
		
	def test_module_manage(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		# test if non admin can access module management page
		response = self.client.get(reverse('senpai:moduleManage'))
		self.assertEqual(response.status_code,302)
		up = UserProfile.objects.get(user=u)
		up.is_admin = 1
		up.save()
		# test if admin can access module management page
		response = self.client.get(reverse('senpai:moduleManage'))
		self.assertEqual(response.status_code,200)

class PageUseAblilityTest(TestCase):
	# test home page has module list
	def test_homepage_module_appears(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		mod2 = add_module('Testing Module2')
		add_enrollment(mod2,u)
		
		# both module should appears, mod1 is in other_modules, mod2 is in my_modules
		response = self.client.get(reverse('senpai:home'))
		self.assertContains(response,mod1.name)
		self.assertContains(response,mod2.name)
		self.assertIn(mod1,response.context['other_modules'])
		self.assertIn(mod2,response.context['my_modules'])
		
	# test module page has note list	
	def test_module_page_note_appears(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		n = add_note(mod1,u,'test_note','example_note.pdf')
		
		# context should have note object and the title of the note should on the page.
		response = self.client.get(reverse('senpai:show_module',kwargs={'module_name_slug':mod1.slug}))
		self.assertContains(response,n.title)
		self.assertIn(n,response.context['notes'])
	
	# test note page can see comments and likes		
	def test_notepage_comments_and_likes(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		n = add_note(mod1,u,'test_note','example_note.pdf')
		Comment = 'Good note!'
		response = self.client.get(reverse('senpai:show_note',kwargs={'note_id':n.id}))
		
		# user has not like or comment this note 
		self.assertEqual(response.context['likes'],0)
		self.assertEqual(response.context['liked'],0)
		self.assertNotContains(response,Comment)
		
		add_like(u, n)
		add_comment(n,u,Comment)
		
		# user has liked and commented this note 
		response = self.client.get(reverse('senpai:show_note',kwargs={'note_id':n.id}))
		self.assertEqual(response.context['likes'],1)
		self.assertEqual(response.context['liked'],1)
		self.assertContains(response,Comment)
	
	# test mynote page has user's note and do not has other's note
	def test_my_note_note_list(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		u2 = add_user('Dio')
		mod1 = add_module('Testing Module')
		n = add_note(mod1,u,'test_note1','example_note.pdf')
		n2 = add_note(mod1,u2,'test_note2','example_note.pdf')
		
		response = self.client.get(reverse('senpai:mynote'))
		self.assertContains(response,n.title)
		self.assertNotContains(response,n2.title)
		self.assertIn(n,response.context['notes'])
		self.assertNotIn(n2,response.context['notes'])
		
	# test mymodule page has all modules,  mod1 is in other_modules, mod2 is in my_modules
	def test_my_module_module_list(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		mod2 = add_module('Testing Module2')
		add_enrollment(mod2,u)
		
		response = self.client.get(reverse('senpai:mymodule'))
		self.assertContains(response,mod1.name)
		self.assertContains(response,mod2.name)
		self.assertIn(mod1,response.context['other_modules'])
		self.assertIn(mod2,response.context['user_modules'])
	
	# test mylike page has liked notes and no unliked notes
	def test_my_like_liked_note_list(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		n = add_note(mod1,u,'test_note','example_note.pdf')
		
		# User has not liked note, note should not in this page
		response = self.client.get(reverse('senpai:mylike'))
		self.assertNotContains(response,n.title)
		
		like = add_like(u,n)
		
		# User liked note, note should in this page
		response = self.client.get(reverse('senpai:mylike'))
		self.assertContains(response,n.title)
	
	# test sign in, sign up, and logout functions.
	def test_sign_inup_and_logout(self):
		# Users has not logged in should be redirect
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,302)
		
		# A signed-up user should be auto logged in
		self.client.post(reverse('senpai:signinup'),{'username': 'testuser', 'password':'1', 'email':'sb@1.com', 'type':'signup'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,200)
		
		# If user logged out, he can not get access to home page
		self.client.get(reverse('senpai:logout'))
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,302)
		
		# And if he logged in, he can get access to home page
		self.client.post(reverse('senpai:signinup'),{'username': 'testuser', 'password':'1', 'type':'signin'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,200)
	
	# test if an admin can signed with admin-key.
	def test_admin_signup(self):
		u = add_user('JoJo',1)
		up = UserProfile.objects.get(user=u)
		self.client.post(reverse('senpai:signinup'),{'username': 'admintest', 'password':'1', 'email':'sb@1.com', 'admin_key':up.admin_key, 'type':'signup'}, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
		
		# signed up successful
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,200)
		
		# check admin status
		admin = User.objects.get(username = 'admintest')
		adminp = UserProfile.objects.get(user=admin)
		self.assertEqual(adminp.is_admin,1)
	
	# test any module added is in module management page
	def test_module_management_module_list(self):
		u = add_user('JoJo',1)
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		modname = 'Testing Module'
		
		response = self.client.get(reverse('senpai:moduleManage'))
		self.assertNotContains(response,modname)
		
		mod1 = add_module('Testing Module')
		response = self.client.get(reverse('senpai:moduleManage'))
		self.assertContains(response,modname)
		
		
		
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
    if is_admin == 1:
        gen_admin_key( up )
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
