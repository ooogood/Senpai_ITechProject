from django.test import TestCase,Client
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
from django.contrib.auth.models import User
from django.core.files import File
from django.urls import reverse

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

    # test comment id, date
	
class PageAvailabilityTest(TestCase):
	#test user can get access to home
	def test_home(self):
		u = add_user('TestUser')
		u.set_password('1')
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,302)
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,200)
		
	def test_module(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		response = self.client.get(reverse('senpai:show_module',kwargs={'module_name_slug':mod1.slug}))
		self.assertEqual(response.status_code,200)
		
	def test_note(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		note1 = add_note(mod1,u,'testnote','example_note.pdf')
		url = reverse('senpai:show_note',kwargs={'note_id':note1.id})
		response = self.client.get(url)
		self.assertEqual(response.status_code,200)
		
	def test_mynote(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		response = self.client.get(reverse('senpai:mynote'))
		self.assertEqual(response.status_code,200)
		
	def test_mymodule(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		response = self.client.get(reverse('senpai:mymodule'))
		self.assertEqual(response.status_code,200)
		
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
	
	def test_homepage_module_appears(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		mod2 = add_module('Testing Module2')
		add_enrollment(mod2,u)
		
		response = self.client.get(reverse('senpai:home'))
		self.assertContains(response,mod1.name)
		self.assertContains(response,mod2.name)
		self.assertIn(mod1,response.context['other_modules'])
		self.assertIn(mod2,response.context['my_modules'])
		
	def test_module_page_note_appears(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		n = add_note(mod1,u,'test_note','example_note.pdf')
		
		response = self.client.get(reverse('senpai:show_module',kwargs={'module_name_slug':mod1.slug}))
		self.assertContains(response,n.title)
		self.assertIn(n,response.context['notes'])
		
	def test_notepage_comments_and_likes(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		n = add_note(mod1,u,'test_note','example_note.pdf')
		Comment = 'Good note!'
		response = self.client.get(reverse('senpai:show_note',kwargs={'note_id':n.id}))
		
		self.assertEqual(response.context['likes'],0)
		self.assertEqual(response.context['liked'],0)
		self.assertNotContains(response,Comment)
		
		add_like(u, n)
		add_comment(n,u,Comment)
		
		response = self.client.get(reverse('senpai:show_note',kwargs={'note_id':n.id}))
		self.assertEqual(response.context['likes'],1)
		self.assertEqual(response.context['liked'],1)
		self.assertContains(response,Comment)
		
	def test_my_note_note_list(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		n = add_note(mod1,u,'test_note','example_note.pdf')
		
		response = self.client.get(reverse('senpai:mynote'))
		self.assertContains(response,n.title)
		self.assertIn(n,response.context['notes'])
		
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
		
	def test_my_like_liked_note_list(self):
		u = add_user('JoJo')
		self.client.login(username='JoJo', password='JoJoisnumber1!')
		mod1 = add_module('Testing Module')
		n = add_note(mod1,u,'test_note','example_note.pdf')
		
		response = self.client.get(reverse('senpai:mylike'))
		self.assertNotContains(response,n.title)
		
		like = add_like(u,n)
		
		response = self.client.get(reverse('senpai:mylike'))
		self.assertContains(response,n.title)
		
	def test_sign_inup_and_logout(self):
		self.client.post(reverse('senpai:signinup'),{'username': 'admintest', 'password':'1', 'email':'sb@1.com', 'signup_form':'submit'})
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,200)
		
		self.client.get(reverse('senpai:logout'))
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,302)
		
		self.client.post(reverse('senpai:signinup'),{'username': 'admintest', 'password':'1', 'signin_form':'submit'})
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,200)
	
	def test_admin_signup(self):
		u = add_user('JoJo',1)
		up = UserProfile.objects.get(user=u)
		self.client.post(reverse('senpai:signinup'),{'username': 'admintest', 'password':'1', 'email':'sb@1.com', 'admin_key':up.admin_key, 'signup_form':'submit'})
		response = self.client.get(reverse('senpai:home'))
		self.assertEqual(response.status_code,200)
		
		admin = User.objects.get(username = 'admintest')
		adminp = UserProfile.objects.get(user=admin)
		self.assertEqual(adminp.is_admin,1)
		
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
