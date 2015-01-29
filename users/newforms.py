from django import forms
from django.forms import widgets, Field 
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy
from django.utils.translation import ugettext_lazy as _





my_default_errors = {
       'required': 'This field is required',
       'invalid': 'Someone has already signed up with this email',
    }

Field.default_error_messages = {
    'required': ugettext_lazy("This field is mandatory"),
    'invalid': 'Someone has already signed up with this email',
}



class UserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password'].required = True
        self.fields['verify_password'].required = True
    
    email = forms.CharField(max_length=55, required=True, widget=forms.EmailInput( attrs = {'class': 'form-control','placeholder':'Email',}))
    password = forms.CharField(max_length=55, required=True, widget=forms.PasswordInput(render_value=False, attrs = {'class': 'form-control','placeholder':'Password', }))
    verify_password = forms.CharField(max_length=55, required=True, widget=forms.PasswordInput(render_value=False, attrs = {'class': 'form-control','placeholder':'Re-Enter Password', }))


    def clean_password(self):
        if self.data['password'] != self.data['verify_password']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']


    def clean_email(self):
        value = self.data['email']
        try:
            User.objects.get(username=value)
            raise forms.ValidationError("Someone is already using this email. Please pick another.")
        except User.DoesNotExist:
            return value

    def clean(self, *args, **kwargs):

        if self.data['email'] and self.data['password'] and self.data['verify_password']:

            self.clean_email()
            self.clean_password()
            return super(UserForm, self).clean(*args, **kwargs)
        raise forms.ValidationError('Please Fill Out All Fields')
