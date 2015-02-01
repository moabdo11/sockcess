from __future__ import absolute_import, unicode_literals
from django import forms
from django.db import models
from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect, get_object_or_404
import re
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import Field, RegexField, Select, CharField
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy
from django.utils.translation import ugettext_lazy as _
from .models import Subscriber, Sock
from django.contrib.auth.models import User
from django.forms import widgets, Field

#from django.contrib.localflavor import forms




my_default_errors = {
       'required': 'This field is required',
       'invalid': 'Someone has already signed up with this email',
    }

Field.default_error_messages = {
    'required': ugettext_lazy("This field is mandatory"),
    'invalid': 'Someone has already signed up with this email',
}


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['verify_password'].required = True



    email = forms.CharField(max_length=55, required=True, widget=forms.EmailInput( attrs = {'class': 'form-control','placeholder':'Email', 'error_messages': my_default_errors,}))
    password = forms.CharField(max_length=55, required=True, widget=forms.PasswordInput(render_value=False, attrs = {'class': 'form-control','placeholder':'Re-Enter Password', 'error_messages': my_default_errors,}))
    verify_password = forms.CharField(max_length=55, required=True, widget=forms.PasswordInput(render_value=False, attrs = {'class': 'form-control','placeholder':'Re-Enter Password', 'error_messages': my_default_errors,}), )
    #verify_email = forms.EmailField()
          
    class Meta:
        model = User
        fields = ['email', 'password']
    
    #widgets = {
     #       'email': forms.EmailInput( attrs = {'class': 'form-control','placeholder':'Email', 'error_messages': my_default_errors,} ),
     #       'password': forms.PasswordInput( attrs = {'class': 'form-control','placeholder':'Re-Enter Password', 'error_messages': my_default_errors,}),
     #   }    
        
        
    def clean_email(self):
        email = self.cleaned_data['email']
        
        
        try:
            User.objects.get(username=email)
        except:
            return email
        raise forms.ValidationError(_("someone already has an account set up with this email! "))
        
        return HttpResponseRedirect('/signup')
        
    def clean(self):
        if self.cleaned_data['password']:
            password = self.cleaned_data['password']
        else:
            raise forms.ValidationError(_("Please enter your email!"))
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
        fields = ['street', 'city','state','zipcode','customer']
