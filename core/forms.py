from django.urls import path
from . import views
from django.contrib.auth.forms import UserCreationForm
from .models import User, PCBuild, Address
from django import forms
from django.forms import ModelForm
from django import forms


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']
        


class PCBuildForm(forms.ModelForm):
    class Meta:
        model = PCBuild
        fields = ['Name','CPU', 'GPU', 'Motherboard', 'RAM', 'PSU', 'SSD_Storage', 'HDD_Storage', 'Case', 'CPU_Cooler']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control address-input', 'placeholder': 'Enter PC Build Name'}),
            'CPU': forms.Select(attrs={'class': 'form-control'}),
            'GPU': forms.Select(attrs={'class': 'form-control'}),
            'Motherboard': forms.Select(attrs={'class': 'form-control'}),
            'RAM': forms.Select(attrs={'class': 'form-control'}),
            'PSU': forms.Select(attrs={'class': 'form-control'}),
            'SSD_Storage': forms.Select(attrs={'class': 'form-control'}),
            'HDD_Storage': forms.Select(attrs={'class': 'form-control'}),
            'Case': forms.Select(attrs={'class': 'form-control'}),
            'CPU_Cooler': forms.Select(attrs={'class': 'form-control'}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['line1', 'line2', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'line1': forms.TextInput(attrs={
                'class': 'address-input',
                'placeholder': 'Line 1',
                'autocomplete': 'address-line1'
            }),
            'line2': forms.TextInput(attrs={
                'class': 'address-input',
                'placeholder': 'Line 2 (Optional)',
                'autocomplete': 'address-line2'
            }),
            'city': forms.TextInput(attrs={
                'class': 'address-input',
                'placeholder': 'City',
                'autocomplete': 'address-level2'
            }),
            'state': forms.TextInput(attrs={
                'class': 'address-input',
                'placeholder': 'State/Province',
                'autocomplete': 'address-level1'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'address-input',
                'placeholder': 'Postal Code',
                'autocomplete': 'postal-code'
            }),
            'country': forms.TextInput(attrs={
                'class': 'address-input',
                'placeholder': 'Country',
                'autocomplete': 'country-name'
            }),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'bio']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'profile-input',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'profile-input',
                'placeholder': 'Email Address'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'profile-input',
                'placeholder': 'Tell us about yourself...',
                'rows': 3
            }),
        }