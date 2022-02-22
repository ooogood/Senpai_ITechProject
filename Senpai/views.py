from django.shortcuts import render
from django.http import HttpResponse
## import from models
## import modelForms
from django.shortcuts import redirect
from django.urls import reverse
## import userForms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
## import datetime
from datetime import datetime

# Create your views here.
def mynote(request):
    context_dict = {}
    if request.user.is_authenticated:
        note_list = Note.objects.filter(User=request.user).order_by('Date')[:5]
        context_dict['note'] = note_list
        context_dict['user'] = request.user
    else:
        return render(request,'users/login_error.html')

    response = render(request,'users/mynote.html',context=context_dict}
    return response 
    
