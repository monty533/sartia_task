from .models import Users
from django.forms import ModelForm
from django import forms
import re
from django.utils import timezone

class DateInput(forms.DateInput):
    input_type = 'date'

class SignUpForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control','maxlength':10}),min_length=6)
    class Meta:
        model = Users
        fields = ['email','name','contact_no','password','gender','dob']
        widgets = {
            'dob': DateInput(attrs={'id': 'txtDate'})
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if re.search(r'\d', name):
            raise forms.ValidationError("Numbers are not allowed only use characters")
        if len(name) > 60:
            raise forms.ValidationError("Length should be less than 60 characters")
        return name
    
    def clean_contact_no(self):
        contact_no = self.cleaned_data.get('contact_no')
        if len(str(contact_no)) > 10:
            raise forms.ValidationError("Length should be less than 10 digit")

        return contact_no
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) > 10:
            raise forms.ValidationError("Password Length should be less than 10")
        return password
    
    def clean_dob(self):
        selected_date = self.cleaned_data.get('dob')
        if selected_date and selected_date > timezone.now().date():
            raise forms.ValidationError("Future date is not allowed.")
        return selected_date
    
    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        if email:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(pattern, email):
                pass
            else:
                return forms.ValidationError('Invalid email')
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
