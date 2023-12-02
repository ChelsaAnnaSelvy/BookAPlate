from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from admin_workbench.models import User, Customer, Restaurant 

class LoginForm(AuthenticationForm):
     # Define a custom widget for the password fields
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Password'})
    )
    class Meta:
        model = User
        fields =['username','password']       

class UserAuthenticationForm(UserCreationForm):
    # Define a custom widget for the password fields
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Re-enter password'})
    )
    class Meta:
        model = User
        fields =['first_name','last_name','email','username','password1','password2']
        labels = {
        'first_name': '',
        'last_name': '',
        'email': '',
        'username': '',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control w-100 py-3 w-100 py-3', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Username'}),
             }

class CustomerRegistrationForm(forms.ModelForm):
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

class RestaurantRegistrationForm(forms.ModelForm):
    class Meta:
        model= Restaurant
        fields='__all__'
        exclude=['status','user','description']
        labels = {
        'phone': '',
        'address': '',
        'place': '',
        'state': '',
        'pancard': '',
        'profile_photo': '',
        'fssai_registration_number':'',
        'license_number':'',
        
        }
        
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control w-100 py-3'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control w-100 py-3'}),
            'state': forms.Select(attrs={'class': 'form-select w-100 py-3'}),
            'place': forms.TextInput(attrs={'placeholder': 'Place', 'class': 'form-control w-100 py-3'}),
            'fssai_registration_number': forms.TextInput(attrs={'placeholder': 'FSSAI Registration Number', 'class': 'form-control w-100 py-3'}),
            'license_number': forms.TextInput(attrs={'placeholder': 'License Number', 'class': 'form-control w-100 py-3'}),
            'profile_photo': forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control w-100 py-3'}),
            'pancard': forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control w-100 py-3'}),
        }