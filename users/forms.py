from __future__ import absolute_import, unicode_literals
from django import forms
from django.db import models
from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect, get_object_or_404
import re
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import Field, RegexField, Select, CharField
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from .models import Subscriber, Sock
from django.contrib.auth.models import User
#from django.contrib.localflavor import forms


"""
class UStateSelect(Select):
    
    def __init__(self, attrs=None):
        from .us_states import STATE_CHOICES
        super(USStateSelect, self).__init__(attrs, choices=State_Choices)
        
class USPSSelect(Select):
    
    def __init__(self, attrs=None):
        from .us_states import USPS_CHOICES
        super(USPSSelect, self).__init__(attrs, choices=USPS_CHOICES)

"""

class SignUpForm(forms.ModelForm):
    
    verify_password = forms.CharField(max_length=55, widget=forms.PasswordInput(render_value=False))
    #verify_email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['email', 'password']
        
        widgets = {
            'password': forms.PasswordInput(),
        }
        
    def clean_email(self):
        email = self.cleaned_data['email']
        
        
        try:
            User.objects.get(username=email)
        except:
            return email
        raise forms.ValidationError(_("someone already has an account set up with this email! "))
        
        return HttpResponseRedirect('/signup')
        
    def clean(self):
        password = self.cleaned_data['password']
        verify_password = self.cleaned_data['verify_password']
        if password and verify_password and password != verify_password:
            raise forms.ValidationError(_("The passwords do not match."))
        return self.cleaned_data
            
    



class SignInForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['email', 'password']
        
        widgets = {
            'password': forms.PasswordInput(),
        }
        
class SubscriberForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    state = forms.CharField()
    zipcode = forms.CharField()
    class Meta:
        model = Subscriber
        fields = ['street', 'city','customer']
