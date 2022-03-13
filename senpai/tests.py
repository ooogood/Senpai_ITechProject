from django.test import TestCase
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
from django.contrib.auth.models import User
from populate_senpai import add_user, add_note, add_comment, add_enrollment, add_like, add_module

# Create your tests here.
# test method name should start with 'test_'
class ModelTests(TestCase):
	note_path = 'example_note.pdf'
	def test_all_models(self):
		# self.user = User.objects.create_user(username='testuser', password='123456')
		# login = self.client.login(username='testuser', password='123456')
		
		# test user is_admin
		u = add_user('JoJo')
		up = UserProfile.objects.get(user=u)
		self.assertEquals( up.is_admin, 0 )
		# test module id, slug
		mod1 = add_module('Testing Module')
		mod2 = add_module('TestingModule')
		self.assertEqual(mod1.slug, "testing-module")
		self.assertEqual(mod1.id, 1)
		self.assertEqual(mod2.slug, "testingmodule")
		self.assertEqual(mod2.id, 2)
