from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # User model has already had fields:
    #   username, email, password, ...
    role = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Module(models.Model):
    NAME_MAX_LENGTH = 32
    id = models.AutoField(primary_key=True)
    # the name has to be unique for generating unique Module page url
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Module, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class Note(models.Model):
    TITLE_MAX_LENGTH = 32

    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    date = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    # file can be blank for testing for now
    file = models.FileField(upload_to='notes', blank=True)
    def __str__(self):
        return self.title
		

class Enrollment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    COMMENT_MAX_LENGTH = 65535

    id = models.AutoField(primary_key=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=COMMENT_MAX_LENGTH)

    def __str__(self):
        return self.content

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)