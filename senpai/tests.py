from django.test import TestCase
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like

# Create your tests here.
class ModuleModelTests(TestCase):
	def test_slug(self):
		mod = Module(name="Testing Module")
		mod.save()
		self.assertEqual(mod.slug, "testing-module")
		self.assertEqual(mod.id, 1)