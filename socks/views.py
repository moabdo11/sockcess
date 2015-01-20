from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from users.forms import SignUpForm, SignInForm

def home(request):

    title = 'Sockcess | Sock Subscriptions'


    form = SignUpForm(request.POST or None)

    form.fields['email'].widget.attrs = {'class': 'form-control','placeholder':'Email'}
    form.fields['password'].widget.attrs = {'class': 'form-control','placeholder':'Password'}
    form.fields['verify_password'].widget.attrs = {'class': 'form-control','placeholder':'Re-Enter Password'}
    #form.fields['verify_email'].widget.attrs = {'class': 'form-control','placeholder':'Re-Enter Email'}

    if request.POST:
        if form.is_valid():
            usern = form.cleaned_data['email']
            emai = usern
            passw = form.cleaned_data['password']

            if usern and emai and passw:
                user = User.objects.create_user(username = usern,
                                            email = emai,
                                            password = passw)
                user.save()

                user = authenticate(username=usern, password=passw)

                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/thankyou')
                    else:
                        #user exists but account has been disabled
                        return HttpResponseRedirect('/signin')
                else:
                    #credentials are wrong or user does not exist
                    return HttpResponseRedirect('/signup')
        else:
            return HttpResponseRedirect('/signup')
        
    return render_to_response('index.html',
                              locals(),
                              context_instance=RequestContext(request))





def signup(request):

    title = 'Sign Up'
    form = SignUpForm(request.POST or None)

    form.fields['email'].widget.attrs = {'class': 'form-control','placeholder':'Email'}
    form.fields['password'].widget.attrs = {'class': 'form-control','placeholder':'Password'}
    form.fields['verify_password'].widget.attrs = {'class': 'form-control','placeholder':'Re-Enter Password'}
    #form.fields['verify_email'].widget.attrs = {'class': 'form-control','placeholder':'Re-Enter Email'}

    if form.is_valid():
        usern = form.cleaned_data['email']
        emai = usern
        passw = form.cleaned_data['password']

        if usern and emai and passw:
            user = User.objects.create_user(username = usern,
                                            email = emai,
                                            password = passw)
            user.save()

            user = authenticate(username=usern, password=passw)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/thankyou')
                else:
                    #user exists but account has been disabled
                    return HttpResponseRedirect('/faq')
            else:
                #credentials are wrong or user does not exist
                messages.success(request,"Oops! Looks like there was something wrong with your credentials. Please re-enter them here")
                return HttpResponseRedirect('/signup')
        
    return render_to_response('onlysignup.html',
                              locals(),
                              context_instance=RequestContext(request))




def about(request):
    
    title = 'About | SockCess'
    
    return render_to_response('about.html',
                              locals(),
                              context_instance=RequestContext(request))
