from django.shortcuts import render
from django.urls import reverse
from app.forms import *
from django.http import HttpResponse, HttpResponseRedirect 
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from app.models import *
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

            #to send mail

            send_mail('Registration Confirmation',
                     "Thank you for Registring ",
                     "brindhaanand@gmail.com",
                     [mufd.email],
                     fail_silently = True)
            
            #registration 

            username = ufd.cleaned_data['username']
            password = ufd.cleaned_data['password']
            AUO=authenticate(username=username,password=password)

            if AUO and AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Invalid Credentials')

        else:
            return HttpResponse('Not Done')
    else:
        ufo = UserForm()
        pfo = ProfileForm()
        data = {'ufo':ufo, 'pfo': pfo}
        return render(request, 'Register.html', data)

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')



def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)

        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Credentials')
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile_dis(request):
    un = request.session.get('username')
    uo = User.objects.get(username = un)
    po = Profile.objects.get(username = uo)
    data = {'uo':uo, 'po':po}
    return render(request,'profile_dis.html',data )

