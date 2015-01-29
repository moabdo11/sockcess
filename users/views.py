from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Subscriber, Sock, Order
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.core.context_processors import csrf
from .forms import SubscriberForm, SignInForm
import stripe, time, datetime, json
from dateutil.relativedelta import *
from datetime import *



"""

This document is split into 3 sections: USER SIGNUP FUNCTIONS, USER ACCOUNT FUNCTIONS, and CHANGE USER ACCOUNT FUNCTION


"""

####################################### USER SIGNUP FUNCTIONS #########################################################


def thankyou(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/signin')
    else:
        title = 'Thanks For Signing Up'

    return render_to_response('thankyou.html',
                              locals(),
                              context_instance=RequestContext(request))


def firstchoice(request):
    
    c = {}
    c.update(csrf(request))
    title='choose your destiny'

    #Get sock objects for user to pick from
    
    business = Sock.objects.filter(style='business').latest('id')
    pleasure = Sock.objects.filter(style = 'pleasure').latest('id')


    #user info
    email = request.user.username
    custid = request.user.id
    if request.POST:
        #get selected sock
        selection = request.POST.get('selection')
        #store selected sock in session
        request.session['sock_pick'] = selection
        return HttpResponseRedirect('/shippinginfo')
 
    return render_to_response('firstchoice.html',
                              locals(),
                              context_instance=RequestContext(request))


def shippinginfo(request):

    try:
        request.session['sock_pick']
    except:
        return HttpResponseRedirect('/first')
    
    c = {}
    c.update(csrf(request))
    title='Sock Destination'
    pk = request.user.id
    c = User.objects.get(pk = pk)
    form = SubscriberForm(request.POST or None)

    if Subscriber.objects.filter(customer = request.user):
        old_subscriber = Subscriber.objects.filter(customer = request.user)
        old_subscriber.delete()

    form.fields['first_name'].widget.attrs = {'class': 'form-control','placeholder':'First Name'}
    form.fields['last_name'].widget.attrs = {'class': 'form-control','placeholder':'Last Name'}
    form.fields['street'].widget.attrs = {'class': 'form-control','placeholder':'Street'}
    form.fields['city'].widget.attrs = {'class': 'form-control','placeholder':'City'}
    form.fields['state'].widget.attrs = {'class': 'form-control','placeholder':'State'}
    form.fields['zipcode'].widget.attrs = {'class': 'form-control','placeholder':'Zipcode'}

    if request.POST:
        if request.session['sock_pick'] == 'random':
            sock_genre = 'random'
            sock_style = 'random'
        else:
            sock = Sock.objects.get(sub_style = request.session['sock_pick'])
            sock_genre = sock.style
            sock_style = sock.sub_style
        pk = request.user.id
        customer = User.objects.get(pk = pk)
        first_name = request.POST.get('first_name',)
        last_name = request.POST.get('last_name',)
        street = request.POST.get('street',)
        city = request.POST.get('city',)
        state = request.POST.get('state',)
        zipcode = request.POST.get('zipcode',)

        if first_name and last_name and customer and street and city and state and zipcode:
            customer.first_name = first_name
            customer.last_name = last_name
            customer.save()
                
            subscriber = Subscriber.objects.create(customer = customer,
                                             first_name = first_name,
                                             last_name = last_name,
                                             street = street,
                                             city = city,
                                             state = state,
                                             zipcode = zipcode,
                                             sock_genre = sock_genre,
                                             sock_style = sock_style,)
            subscriber.save()

            return HttpResponseRedirect('/billinginfo')

    return render_to_response('shipping.html',
                              locals(),
                              context_instance=RequestContext(request))


def billinginfo(request):
    
    c = {}
    c.update(csrf(request))
    title = 'Subscribe Now'
    email = request.user.username
    sub_style = request.session['sock_pick']
    #sock = Address.objects.get(sock_style = sub_style)

    if request.POST:
        stripe.api_key = "sk_live_honqsfBszGpd3pFfSXCpdYCT"

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']
        
        if request.session['discount'] == True:
            # Create a Customer with Discount
            customer = stripe.Customer.create(
            card=token,
            plan="baseplan",
            email=email,
            coupon="presignup",
            )
        else:
            # Create a Customer
            customer = stripe.Customer.create(
            card=token,
            plan="baseplan",
            email=email
            )
        
        # Create an Order
        pk = request.user.id
        cust = User.objects.get(pk = pk)
        subscriber = Subscriber.objects.get(customer = cust)
        
        if subscriber:
            subscriber.stripe_id = customer.id
            subscriber.save()
            #ts = time.time()
            order = Order.objects.create(
                                        customer = cust,
                                        first_name = subscriber.first_name,
                                        last_name = subscriber.last_name,
                                        email = request.user.username,
                                        street = subscriber.street,
                                        city = subscriber.city,
                                        state = subscriber.state,
                                        zipcode = subscriber.zipcode,
                                        sock_style = request.session['sock_pick'],
                                       
                                        #timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            )

            order.save()
            messages.success(request, "Word. We got you.")
            
        return HttpResponseRedirect('/home')

    return render_to_response('billinginfo.html',
                              locals(),
                              context_instance=RequestContext(request))


####################################### USER ACCOUNT FUNCTIONS #########################################################


def userhome(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/signin')
    else:
        print request
        email = request.user.username
        
        custid = request.user.id
        user = User.objects.get(pk = custid)
        address = Subscriber.objects.get(customer = user)
        
        if address.sock_style == 'random':
            rando = 'random'
        else:
            img = Sock.objects.get(sub_style = address.sock_style)
        title = 'May The Socks Be With You'



        if 'sock_pick' in request.session:
            style = request.session['sock_pick']
            address = Subscriber.objects.get(customer = custid)
            sock = address.sock_style
            
        

        return render_to_response('home.html',
                                  locals(),
                                  context_instance=RequestContext(request))


def logoutuser(request):
    logout(request)

    return HttpResponseRedirect('/')


def signin(request):
    
    c = {}
    c.update(csrf(request))
    signin_form = SignInForm(request.POST or None)
    title = 'Sign In'
    signin_form.fields['email'].widget.attrs = {'class': 'form-control','placeholder':'Email'}
    signin_form.fields['password'].widget.attrs = {'class': 'form-control','placeholder':'Password'}

    if request.POST:
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect('/home')
                # ensure user exists in stripe           

            else:
                #user exists but account has been disabled
                user.is_active = True
                user.save()
               
                return HttpResponseRedirect('/shippinginfo')
        else:
            #credentials are wrong or user does not exist
            messages.error(request, "we do not recognize that user/pass combo ho")

            return HttpResponseRedirect('/signin')

    return render_to_response('signin.html',
                              locals(),
                              context_instance=RequestContext(request))


def myaccount(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/signin')
    else:
        
        title = 'My Account'
        #messages.success(request, 'welcome to your account settings.')


    return render_to_response('myaccount.html',
                             locals(),
                             context_instance=RequestContext(request))


####################################### USER CHANGE-ACCOUNT FUNCTIONS #########################################################

def change_address_info(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/signin')
    else:
        title = 'Change Shipping Address'
        c = {}
        c.update(csrf(request))
        # current user info
        pk = request.user.id
        user = User.objects.get(pk = pk)
        address = Subscriber.objects.get(customer = pk)
        
        first_name = address.first_name
        last_name = address.last_name
        street = address.street
        city = address.city
        state = address.state
        zipcode = address.zipcode
        
        
        # form
        form = SubscriberForm(request.POST or None)
        form.fields['first_name'].widget.attrs = {'class': 'form-control','required': 'True','placeholder': 'New First Name'}
        form.fields['last_name'].widget.attrs = {'class': 'form-control','required': 'True','placeholder': 'New Last Name'}
        form.fields['street'].widget.attrs = {'class': 'form-control','required': 'True','placeholder': 'New Street Address'}
        form.fields['city'].widget.attrs = {'class': 'form-control','required': 'True','placeholder': 'New City'}
        form.fields['state'].widget.attrs = {'class': 'form-control','required': 'True','placeholder': 'New State'}
        form.fields['zipcode'].widget.attrs = {'class': 'form-control','required': 'True','placeholder': 'New Zipcode'}
        
        
        if request.POST:
            new_first_name = request.POST.get('first_name',)
            new_last_name = request.POST.get('last_name',)
            new_street = request.POST.get('street',)
            new_city = request.POST.get('city',)
            new_state = request.POST.get('state',)
            new_zipcode = request.POST.get('zipcode',)
            
            if new_first_name and new_last_name and user and new_street and new_city and new_state and new_zipcode:
                    user.first_name = new_first_name
                    user.last_name = new_last_name
                    user.save()
                    
                    address.first_name = new_first_name
                    address.last_name = new_last_name
                    address.street = new_street
                    address.state = new_state
                    address.zipcode = new_zipcode
                    address.save()
                    
                    messages.success(request, "we've updated the address we will be sending socks to")
                    return HttpResponseRedirect('/home')
                
            messages.error(request,"please fill in all fields")
            return HttpResponseRedirect('/changeaddress')


    return render_to_response('changeaddress.html',
                              locals(),
                              context_instance=RequestContext(request))


def change_billing_info(request):
    
    title = 'Change How You Pay'
    email = request.user.username
    c = {}
    c.update(csrf(request))

    
    if request.POST:
        
        try:
            user = User.objects.get(email=email)
        except:
            user = User.objects.filter(email = email)[0]
        subscriber = Subscriber.objects.get(customer=user)
        stripe_id = subscriber.stripe_id
        stripe.api_key = "sk_live_honqsfBszGpd3pFfSXCpdYCT"
        token = request.POST['stripeToken']
        customer = stripe.Customer.retrieve(stripe_id)
        
        customer.card=token
        customer.save()
        
        messages.success(request, "we've updated the card we will be billing from now on")
        return HttpResponseRedirect('/home')
    
    return render_to_response('changebillinginfo.html',
                              locals(),
                              context_instance=RequestContext(request))


def change_sock(request):
    
    c = {}
    c.update(csrf(request))
    title = 'Time For A Change'
    email = request.user.username
    business = Sock.objects.filter(style = 'business').latest('id')
    pleasure = Sock.objects.filter(style = 'pleasure').latest('id')
    
    if request.POST:
        
        sock_style = request.POST.get('selection')
        user = User.objects.get(email = email)
        addr = Subscriber.objects.get(customer = user)
        
        if sock_style == 'random':
            addr.sock_genre = 'random'
            addr.sock_style = 'random'
        else:    
            s = Sock.objects.get(sub_style = sock_style)
            addr.sock_genre = s.style
            addr.sock_style = s.sub_style
            
        addr.save()
        messages.success(request, "We will begin delivering your new style next month!")
        
        return HttpResponseRedirect('/home')
        
            
        
    return render_to_response('changesockselection.html',
                              locals(),
                              context_instance=RequestContext(request))


def deleteuser(request):
    
    c = {}
    c.update(csrf(request))
    title="Are You Sure?"
    if request.POST:
        choice = request.POST.get('choice')
        message = choice
        pk = request.user.id
        u = User.objects.get(pk = pk)

        if choice == 'yes':
            #try:
            info = Subscriber.objects.get(customer = u)
            #except:
                #info = Order.objects.filter(email = request.user.username)
             #   nada = 'nada'
            stripe_id  = info.stripe_id
            stripe.api_key = "sk_live_honqsfBszGpd3pFfSXCpdYCT"

            cu = stripe.Customer.retrieve(stripe_id)
            cu.delete()
            user = User.objects.get(pk = request.user.id)
            user.delete()
            messages.success(request,"Sorry to lose you. We feel bad for your feet.")
            #user.is_active=False
            #user.save()

            return HttpResponseRedirect('/logout')
        else:
            return HttpResponseRedirect('/myaccount')


        HttpResponseRedirect('/home')
    return render_to_response('deleteuser.html',
                              locals(),
                              context_instance=RequestContext(request))    


#######################################################################################################################################
#   UNUSED FUNCTIONS


"""

           # Retrieve subscription and change next billing date to the first of the month
            
=======




#############################################################################################################################################
#####                                 CURRENTLY UNUSED CODE SNIPPETS                         #######


            # Retrieve subscription and change next billing date to the first of the month

            c = stripe.Customer.retrieve(customer.id)
            s = c.subscriptions
            sub_id = s.data[0].id
            subscription = c.subscriptions.retrieve(sub_id)

            #set date value (first of next month)
            import calendar
            import dateutil

            from dateutil.relativedelta import *
            from datetime import *
=======

            import time

            today = datetime.today()
            d = today+relativedelta(months=+1,day=1,hour=10)
            d = time.mktime(d.timetuple())
            #date = date.strftime("%Y-%m-%d %H:%M:%S")
            
            subscription.trial_end(date)



            """