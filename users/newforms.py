from django import forms
from django.forms import widgets, Field 
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
        self.fields['email'].required=True
    
    
    
    email = forms.CharField(max_length=55, required=True, widget=forms.EmailInput( attrs = {'class': 'form-control','placeholder':'Email', 'error_messages': my_default_errors,}))
    password = forms.CharField(max_length=55, required=True, widget=forms.PasswordInput(render_value=False, attrs = {'class': 'form-control','placeholder':'Re-Enter Password', 'error_messages': my_default_errors,}))
    verify_password = forms.CharField(max_length=55, required=True, widget=forms.PasswordInput(render_value=False, attrs = {'class': 'form-control','placeholder':'Re-Enter Password', 'error_messages': my_default_errors,}), )


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