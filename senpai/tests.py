from django.test import TestCase
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
from django.contrib.auth.models import User

# Create your tests here.
class ModuleModelTests(TestCase):
	def test_id_slug(self):
		mod1 = Module(name="Testing Module")
		mod1.save()
		mod2 = Module(name="TestingModule")
		mod2.save()
		self.assertEqual(mod1.slug, "testing-module")
		self.assertEqual(mod1.id, 1)
		self.assertEqual(mod2.slug, "testingmodule")
		self.assertEqual(mod2.id, 2)

class NoteModelTests(TestCase):
	def notetest(self):
		self.user = User.objects.create_user(username='testuser', password='123456')
		login = self.client.login(username='testuser', password='123456')
		print(login)
		self.assertEqual(self.user.username, 'estuser')