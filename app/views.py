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



def cus_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)

        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            data = {'msg':'*invalid username and password'}
            return render(request, 'login.html', data)
    return render(request, 'login.html')


@login_required
def cus_logout(request):
    logout(request)
    # return render(request,'login.html' )
    return HttpResponseRedirect(reverse('cus_login'))

@login_required
def profile_dis(request):
    un = request.session.get('username')
    uo = User.objects.get(username = un)
    po = Profile.objects.get(username = uo)
    data = {'uo':uo, 'po':po}
    return render(request,'profile_dis.html',data )

@login_required
def change(request):
    if request.method == 'POST':
        pw = request.POST['pw']
        username = request.session.get('username')
        UO = User.objects.get(username = username)
        UO.set_password(pw)
        UO.save()
        #to display details

        un = request.session.get('username')
        uo = User.objects.get(username = un)
        po = Profile.objects.get(username = uo)

        data = {'msg': " Password changes Successfully ",'uo':uo, 'po':po}
        return render(request,'profile_dis.html',data )
        # return HttpResponseRedirect(reverse('profile_dis'))
    return render(request,'change.html') 

def forgot(request):
    if request.method == 'POST':
        un = request.POST['un']
        pw = request.POST['pw']
        LUO = User.objects.filter(username = un)
        if LUO:
            uo = LUO[0]
            uo.set_password(pw)
            uo.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            d = {'msg': '*User name not available'}
            return render(request, 'forgot.html', d)
    return render(request, 'forgot.html')
