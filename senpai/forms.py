from django import forms
from django.contrib.auth.models import User
from senpai.models import UserProfile, Module


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    is_admin = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    admin_key = forms.IntegerField(initial=0)

    class Meta:
        model = UserProfile
        fields = ('admin_key',)


class ModuleForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(max_length=32, help_text="Please enter the module name.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Module
        fields = ('name',)

