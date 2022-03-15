import hashlib

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.base import View

from senpai import models
from senpai.forms import UserForm, UserProfileForm, ModuleForm
from senpai.models import UserProfile, Module, Note, Enrollment, Comment, Like
## import modelForms
from django.shortcuts import redirect
from django.urls import reverse
## import userForms
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime, time
## helper
import os, math, mimetypes

from senpai.templatetags.senpai_template_tags import get_sorted_notes, get_home_modules, get_comments, get_mynote_notes, \
    get_mymodule_modules
import urllib
from urllib import parse


# Create your views here.
# home page
class HomePage(View):
    @method_decorator(login_required)
    def get(self, request):
        if request.is_ajax():
            context_dict = get_home_modules(request.user, request.GET['search'])
            return render(request, 'senpai/home_modules.html', context=context_dict)
        context_dict = get_home_modules(request.user)
        return render(request, 'senpai/home.html', context=context_dict)


# module page
class ModulePage(View):
    @method_decorator(login_required)
    def get(self, request, module_name_slug):
        context_dict = {}
        try:
            module = Module.objects.get(slug=module_name_slug)
            context_dict['module'] = module
        # context_dict['notes'] and context_dict['note_dict'] will be generated by calling get_sorted_notes in html
        except Module.DoesNotExist:
            context_dict['module'] = None
        # if it is ajax request, only return the note list
        if request.is_ajax():
            sort_type = request.GET['sort_type']
            result_dict = get_sorted_notes(module, sort_type)
            return render(request, 'senpai/notelist.html', context=result_dict)
        context_dict['all_modules'] = Module.objects.all().order_by('name')
        return render(request, 'senpai/module.html', context=context_dict)


@login_required
def upload_note(request, module_name_slug):
    file = request.FILES.get('file', False)
    if file != False:
        module = Module.objects.get(slug=module_name_slug)
        new_note = Note.objects.create(module=module, user=request.user, file=file)
        new_note.save()
    return redirect(reverse('senpai:show_module',
                            kwargs={'module_name_slug': module_name_slug}))


# note page
class NotePage(View):
    @method_decorator(login_required)
    def get(self, request, note_id):
        context_dict = {}
        if request.is_ajax():
            note = Note.objects.get(id=note_id)
            # add a comment to this note
            c = Comment.objects.create(note=note, user=request.user, content=request.GET['txt'])
            c.save()
            result_dict = get_comments(note, request.user)
            return render(request, 'senpai/commentlist.html', context=result_dict)
        try:
            context_dict['note'] = Note.objects.get(id=note_id)
            context_dict['module'] = context_dict['note'].module
            like = Like.objects.filter(note=context_dict['note'])
            context_dict['likes'] = like.count()
            context_dict['liked'] = like.filter(user=request.user).count()
        except Note.DoesNotExist:
            context_dict['module'] = None
            context_dict['note'] = None
            context_dict['likes'] = None
            context_dict['liked'] = None
        return render(request, 'senpai/note.html', context=context_dict)


@login_required
def note_like_clicked(request, note_id):
    context_dict = {}
    note = Note.objects.get(id=note_id)
    liked = Like.objects.filter(note=note).filter(user=request.user).count()
    l = Like.objects.get_or_create(user=request.user, note=note)[0]
    if liked == 0:
        # like
        note.likes += 1
        note.save()
        l.save()
    else:
        # dislike
        note.likes -= 1
        note.save()
        l.delete()
    like = Like.objects.filter(note=note)
    context_dict['likes'] = like.count()
    context_dict['liked'] = like.filter(user=request.user).count()
    return render(request, 'senpai/note_like_info.html', context=context_dict)


@login_required
def note_download(request, note_id):
    note = Note.objects.get(id=note_id)
    if os.path.exists(note.file.path):
        with open(note.file.path, 'rb') as fh:
            mime_type, _ = mimetypes.guess_type(note.file.path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = 'attachment; filename=' + note.file.name
            return response
    raise Http404


# user - my note
class Mynote(View):
    @method_decorator(login_required)
    def get(self, request):
        context_dict = {}
        result_dict = get_mynote_notes(request.user)

        context_dict['notes'] = result_dict['notes']
        context_dict['user'] = request.user
        context_dict['comments'] = result_dict['comments']
        # if it is ajax request, only return the note list
        if request.is_ajax():
            need_del_note = request.GET.get('noteid')
            # there should add delete file lines
            if Note.objects.filter(id=need_del_note).exists():
                file = Note.objects.get(id=need_del_note).file
                file.delete()
                Note.objects.filter(id=need_del_note).delete()
            result_dict = get_mynote_notes(request.user)
            return render(request, 'senpai/mynote_notes.html', context=result_dict)
        response = render(request, 'senpai/mynote.html', context=context_dict)
        return response


# user - mylike
@login_required
def mylike(request):
    context_dict = {}
    if request.user.is_authenticated:
        # get note_list
        like_list = Like.objects.filter(user=request.user)
        note = []
        for likes in like_list:
            note.append(likes.note)
        comment = {}
        for n in like_list:
            comment[n.note.id] = Comment.objects.filter(note=n.note).count()

        context_dict['note'] = like_list
        context_dict['user'] = request.user
        context_dict['comments'] = comment
    else:
        return render(request, 'senpai/login_error.html')
    response = render(request, 'senpai/mylike.html', context=context_dict)
    return response


# user - mymodule
@login_required
def mymodule(request):
    user = request.user
    context_dict = get_mymodule_modules(user)
    if request.is_ajax():
        action_type = request.GET.get('action_type')
        module_id = request.GET.get('module_id')
        this_module = Module.objects.get(id=module_id)
        if action_type == 'select':
            if not Enrollment.objects.filter(module=this_module, user=request.user).exists():
                e = Enrollment.objects.get_or_create(module=this_module, user=request.user)[0]
                e.save()
        if action_type == 'delete':
            if Enrollment.objects.filter(module=this_module, user=request.user).exists():
                Enrollment.objects.filter(module=this_module, user=request.user).delete()
        returned_dict = get_mymodule_modules(user)
        return render(request, 'senpai/mymodule_modules.html', context=returned_dict)
    response = render(request, 'senpai/mymodule.html', context=context_dict)
    return response


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        key = request.POST.get('adminKey', "")
        if user_form.is_valid() and profile_form.is_valid():

            if key != 0:
                keySet = UserProfile.objects.filter(admin_key=key)
                if keySet:
                    profile_form.is_admin = 1
                    # Set key to 0 after used
                    admin_key = UserProfile.objects.get(admin_key=key)
                    admin_key.admin_key = 0
                    admin_key.save()
                else:
                    print("Admin Key error or non-existent, please re-input")

            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'senpai/combineLogReg.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


# login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('senpai:home'))
            else:
                return HttpResponse("Your senpai account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'senpai/combineLogReg.html')


@login_required
def restricted(request):
    return render(request, 'senpai/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('senpai:home'))


@login_required
def generateAdminKey(request):
    """This function generate 10 character long hash"""
    current_user = request.user
    statue = UserProfile.objects.get(user=current_user)
    if statue.admin_key == 0:
        hashCode = hashlib.sha1()
        hashCode.update(str(time.time()))
        statue.admin_key = hashCode.hexdigest()[:-10]
        statue.save()
        key = statue.admin_key
        return hashCode.hexdigest()[:-10]
    else:
        return render(request, 'senpai/generateKey.html', context="Key has been generated.")


@login_required
def module_manage(request):
    # Verify login
    current_user = request.user
    statue = UserProfile.objects.get(user=current_user).is_admin
    if statue == 0:
        return redirect(reverse('senpai:home'))

    if request.method == 'GET':
        Modules = Module.objects.filter()
        response = {
            'modules': Modules,
        }
        return render(request, 'senpai/module-manage.html', response)


@login_required
def addModule(request):
    current_user = request.user
    statue = UserProfile.objects.get(user=current_user).is_admin
    if statue == 0:
        return redirect(reverse('senpai:home'))
    form = ModuleForm()
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/senpai/module-manage/')
        else:
            print(form.errors)
    else:
        form = ModuleForm()

    return render(request, 'senpai/module-manage.html', {'form': form})


@login_required
def delModule(request):
    current_user = request.user
    statue = UserProfile.objects.get(user=current_user).is_admin
    if statue == 0:
        return redirect(reverse('senpai:home'))

    mid = request.GET.get('id')
    try:
        obj = models.Module.objects.get(id=mid)
    except Exception as e:
        print('---delete book get error %s' % (e))
        return HttpResponse('---The book id is error')
    if obj:
        obj.delete()
        return HttpResponseRedirect('/senpai/module-manage/')

    return HttpResponse("---The module id is error")
