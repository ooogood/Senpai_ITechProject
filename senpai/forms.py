from django import forms
from django.contrib.auth.models import User
from senpai.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('is_admin', 'admin_key')


# class AdminKeyForm(forms.ModelForm):
#    class Meta:
#        model = UserProfile
#        fields = ('adminKey')
