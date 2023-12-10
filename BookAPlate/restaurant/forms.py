from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from admin_workbench.models import FacilityDetails,Gallery,Restaurant
from admin_workbench.forms import ChangePasswordForm

class AboutForm(forms.ModelForm):
    
    class Meta:
        model = Restaurant
        fields =['description']   
        labels ={
            'description': '',
        }    
        widgets = {
            'description':  forms.Textarea(attrs={'class': 'form-control w-100 py-3','rows':10,'cols':50}),
        }

class FacilityDetailsForm(forms.ModelForm):
    class Meta:
        model = FacilityDetails
        fields ='__all__'
        exclude=['restaurant']
        labels ={
            'facility_name': '',
            'facility_number': '',
            'seat_count':'',            
            'seat_arrangement':'',
            

        }    
        widgets = {
            'facility_name': forms.TextInput(attrs={'placeholder': 'Facility Name','class': 'form-select w-100 py-3'}),
            'facility_number': forms.TextInput(attrs={'placeholder': 'Facility Number', 'class': 'form-control w-100 py-3'}),
            'seat_count':forms.NumberInput(attrs={'placeholder': 'Number of Seats', 'class': 'form-control w-100 py-3'}),
            'seat_arrangement':forms.Select(attrs={'class': 'form-select w-100 py-3'}),
            
        }
 
class GalleryDetailsForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields ='__all__'
        exclude=['restaurant']
        labels ={
            'title': '',
            'description': '',
            'category':'',
            'photo' : '',         

        }    
        widgets = {
            'title':forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control w-100 py-3'}),
            'description':forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control w-100 py-3','rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select w-100 py-3'}),
            'photo':  forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control w-100 py-3'}),
            
        }
 
class EditRestaurantAuthenticationForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields =['first_name','email','username']
        exclude=['password1','password2']
        labels = {
        'first_name': '',        
        'email': '',
        'username': '',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control w-100 py-3 w-100 py-3', 'placeholder': 'Name of the Restaurant'}),
            'email': forms.EmailInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Email'}),
            'username': forms.TextInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Username'}),
             }
    

class EditRestaurantRegistrationForm(forms.ModelForm):
    class Meta:
        model= Restaurant
        fields='__all__'
        exclude=['status','user','fssai_registration_number','license_number','pancard']
        labels = {
        'phone': '',
        'address': '',
        'place': '',
        'state': '',        
        'profile_photo': 'PROFILE PHOTO',               
        'description':'',
        
        }
        
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control w-100 py-3'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control w-100 py-3'}),
            'state': forms.Select(attrs={'class': 'form-select w-100 py-3'}),
            'place': forms.TextInput(attrs={'placeholder': 'Place', 'class': 'form-control w-100 py-3'}),
            'profile_photo': forms.ClearableFileInput(attrs={'accept': 'image/*', 'class': 'form-control w-100 py-3'}),
            'description':  forms.Textarea(attrs={'class': 'form-control w-100 py-3'}),
        }
    