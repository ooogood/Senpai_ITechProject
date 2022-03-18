from django import forms
from django.contrib.auth.models import User
from senpai.models import UserProfile, Module


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'register component username'}), label='Username *')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'register component password', 'autocomplete':'new-password'}), label='Password *')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'register component email'}), label='Email Address *')

    class Meta:
        model = User
        help_texts = {
            'username': None,
        }
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    is_admin = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    admin_key = forms.CharField(widget=forms.TextInput(attrs={'class':'register component key'}), max_length=32, initial=None, required=False, label='Sign Up for Admin?')

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
