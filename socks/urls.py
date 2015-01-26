from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # Admin URLS
    url(r'^admin/', include(admin.site.urls)),                   
                       
    # BasePage URLS
    url(r'^$', 'socks.views.home', name='home'),
    url(r'signup/', 'socks.views.signup', name='signup'),


    # User URLS
    url(r'signin/', 'users.views.signin', name='signin'),
    url(r'home/', 'users.views.userhome', name='userhome'),
    url(r'logout/', 'users.views.logoutuser', name='logoutuser'),
    url(r'myaccount/', 'users.views.myaccount', name='myaccount'),
    url(r'changeaddress/', 'users.views.change_address_info', name='changeaddress'),
    url(r'changebilling/', 'users.views.change_billing_info', name='changebilling'),
    url(r'changethatshit', 'users.views.change_sock', name='changesock'),
    url(r'deleteuser/', 'users.views.deleteuser', name='deleteuser'),

    # User Signup URLS  
    url(r'thankyou/', 'users.views.thankyou', name='thankyou'),
    url(r'first/', 'users.views.firstchoice', name='firstchoice'),
    url(r'choose/', 'users.views.firstchoice', name='choose'),
    url(r'shippinginfo/', 'users.views.shippinginfo', name='shippinginfo'),
    url(r'billinginfo/', 'users.views.billinginfo', name='billinginfo'),

    # Discounted Signup URL
    url(r'discount20%off1stmonth/', 'socks.presignup_view.signup', name='signup'),

)
