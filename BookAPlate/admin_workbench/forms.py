from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class ChangePasswordForm(PasswordChangeForm):
    # Define a custom widget for the password fields
    old_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Current Password'})
    )
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control w-100 py-3', 'placeholder': 'Confirm Password'})
    )
    class Meta:
        model=User
        