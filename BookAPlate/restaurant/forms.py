from django import forms
from admin_workbench.models import FacilityDetails,Gallery,Restaurant

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
            'position' : '',
            'seat_arrangement':'',
            'floor_number':'',

        }    
        widgets = {
            'facility_name': forms.Select(attrs={'class': 'form-select w-100 py-3'}),
            'facility_number': forms.TextInput(attrs={'placeholder': 'Facility Number', 'class': 'form-control w-100 py-3'}),
            'seat_count':forms.NumberInput(attrs={'placeholder': 'Number of Seats', 'class': 'form-control w-100 py-3'}),
            'position' : forms.Select(attrs={'class': 'form-select w-100 py-3'}),
            'seat_arrangement':forms.Select(attrs={'class': 'form-select w-100 py-3'}),
            'floor_number':forms.Select(attrs={'class': 'form-select w-100 py-3'}),
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
 