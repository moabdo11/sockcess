from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.contrib.auth.models import User









def signup(request):

    title = 'Discounted Sign Up'
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
                    
                    try:
                        list = mailchimp.utils.get_connection().get_list_by_id('4d3d1b0805')
                        list.subscribe(emai, {'EMAIL': emai})
                    except:
                        title=emai
                    
                    return HttpResponseRedirect('/thankyou')
                else:
                    #user exists but account has been disabled
                    return HttpResponseRedirect('/faq')
            else:
                #credentials are wrong or user does not exist
                messages.success(request,"Oops! Looks like there was something wrong with your credentials. Please re-enter them here")
                return HttpResponseRedirect('/signup')
        
    return render_to_response('presignup.html',
                              locals(),
                              context_instance=RequestContext(request))
