from django.shortcuts import render
from app.forms import *
# Create your views here.

def Register(request):
    ufo = UserForm()
    pfo = ProfileForm()
    data = {'ufo':ufo, 'pfo': pfo}
    return render(request, 'Register.html', data)
