from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    Role = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Module(models.Model):
    NAME_MAX_LENGTH = 32

    ID = models.IntegerField(default=0, unique=True)
    Name = models.CharField(max_length=NAME_MAX_LENGTH)

    def __str__(self):
        return self.name


class Note(models.Model):
    TITLE_MAX_LENGTH = 32
    FILENAME_MAX_LENGTH = 128

    ID = models.IntegerField(default=0, unique=True)
    Module = models.ForeignKey(Module, on_delete=models.CASCADE)
    User = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Title = models.CharField(max_length=TITLE_MAX_LENGTH)
    Date = models.DateField(auto_now=True)
    Likes = models.IntegerField(default=0)
    FileName = models.CharField(max_length=FILENAME_MAX_LENGTH)

    def __str__(self):
        return self.title

class Enrolment(models.Model):
    Module = models.ForeignKey(Module, on_delete=models.CASCADE)
    User = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class Comment(models.Model):
    COMMENT_MAX_LENGTH = 65535

    ID = models.IntegerField(default=0, unique=True)
    Note = models.ForeignKey(Note, on_delete=models.CASCADE)
    User = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Date = models.DateField(auto_now=True)
    Content = models.CharField(max_length=COMMENT_MAX_LENGTH)

    def __str__(self):
        return self.content

class Like(models.Model):
    User = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Note = models.ForeignKey(Note, on_delete=models.CASCADE)