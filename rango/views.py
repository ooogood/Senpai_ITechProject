from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect

# Create your views here.
def mynote(request)
    context_dict = {}
    if request.user.is_authenticated:
        note_list = Note.objects.filter(User=request.user).order_by('Date')[:5]
        context_dict['note'] = note_list
    else:
        return render(request,'users/login_error.html')
    
    
    
    response = render(request,'users/mynote.html',context=context_dict}
    return response