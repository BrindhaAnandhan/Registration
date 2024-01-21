from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse 
# Create your views here.

def Register(request):

    if request.method == 'POST' and request.FILES:
        ufd = UserForm(request.POST)
        pfd = ProfileForm(request.POST, request.FILES)
        if ufd.is_valid() and pfd.is_valid():

            #This is for userform module
            mufd = ufd.save(commit=False)
            password = ufd.cleaned_data['password']
            mufd.set_password(password)
            mufd.save()


            #This is for profile module
            mpfd = pfd.save(commit=False)
            mpfd.username = mufd
            mpfd.save() 

            return HttpResponse('Registration Done')
        else:
            return HttpResponse('Not Done')
    else:
        ufo = UserForm()
        pfo = ProfileForm()
        data = {'ufo':ufo, 'pfo': pfo}
        return render(request, 'Register.html', data)
