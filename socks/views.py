from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.contrib.auth.models import User
#from users.forms import SignUpForm, SignInForm
from users.newforms import UserForm

import mailchimp
from mailchimp import utils


def home(request):

    title = 'Sockcess | Sock Subscriptions'


    #form = SignUpForm(request.POST or None)
    form = UserForm(request.POST or None)
    
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
                        
                        try:
                            list = mailchimp.utils.get_connection().get_list_by_id('4d3d1b0805')
                            list.subscribe(emai, {'EMAIL': emai})
                        except:
                            title=emai
                            
                        return HttpResponseRedirect('/thankyou')
                    
                    
                    else:
                        #user exists but account has been disabled
                        return HttpResponseRedirect('/signin')
                else:
                    #credentials are wrong or user does not exist
                    messages.success(request,"Sorry, something is not right with your credentials. Make sure your passwords match")
                    return HttpResponseRedirect('/signup')
        messages.success(request,"Sorry, something is not right with your credentials. Make sure your passwords match")
        return HttpResponseRedirect('/signup')
        
    return render_to_response('index.html',
                              locals(),
                              context_instance=RequestContext(request))





def signup(request):

    my_default_errors = {
        'required': 'This field is required',
        'invalid': 'Someone has already signed up with this email',
    }

    title = 'Sign Up'
    form = UserForm(request.POST or None)


    if form.is_valid():
        usern = form.cleaned_data['email']
        emai = usern
        passw = form.cleaned_data['password']

        if usern and emai and passw:
            user = User.objects.create_user(username = usern,
                                            email = emai,
                                            password = passw)
            
            try:
                list = mailchimp.utils.get_connection().get_list_by_id('4d3d1b0805')
                list.subscribe(emai, {'EMAIL': emai})
            except:
                title=emai
            
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
                messages.error(request,"Oops! Looks like there was something wrong with your credentials. Please re-enter them here")
                return HttpResponseRedirect('/signup')
    
    #messages.error(request,"Oops! Looks like there was something wrong with your credentials. Please re-enter them here")
        
    
    return render_to_response('onlysignup.html',
                              locals(),
                              context_instance=RequestContext(request))






"""
    form.fields['email'].widget.attrs = {'class': 'form-control','placeholder':'Email'}
    form.fields['password'].widget.attrs = {'class': 'form-control','placeholder':'Password'}
    form.fields['verify_password'].widget.attrs = {'class': 'form-control','placeholder':'Re-Enter Password'}
    #form.fields['verify_email'].widget.attrs = {'class': 'form-control','placeholder':'Re-Enter Email'}
"""