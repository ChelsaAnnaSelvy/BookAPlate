from django import forms
from django.contrib.auth.models import User
from admin_workbench.forms import ChangePasswordForm
from admin_workbench.models import Customer,Feedback
 

class UserForm(forms.ModelForm):   
    class Meta:
        model = User
        fields =['first_name','last_name','email']
        labels = {
        'first_name': '',
        'last_name': '',
        'email': '',
       
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control w-100 py-3 w-100 py-3', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Email'}),
           
             }

class EditCustomerForm(forms.ModelForm):
    class Meta:
        model= Customer
        fields='__all__'
        exclude=['status','user']
        labels = {
        'phone': '',
        'address': '',
        'place': '',
        'state': '',
        'id_proof': '',
        'profile_photo': '',
        
        }
        
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control w-100 py-3'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control w-100 py-3'}),
            'state': forms.Select(attrs={'class': 'form-select w-100 py-3'}),
            'place': forms.TextInput(attrs={'placeholder': 'Place', 'class': 'form-control w-100 py-3'}),
            'profile_photo': forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control w-100 py-3'}),
            'id_proof': forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control w-100 py-3'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model= Feedback
        fields=['message']
        labels={
            'message':'' ,           
            
        }
        widgets = {
            'message':  forms.Textarea(attrs={'class': 'form-control w-100 py-3','rows':10,'cols':50}),
        }