from django.urls import path
from . import views
from django.contrib.auth.forms import UserCreationForm
from .models import User, PCBuild
from django import forms
from django.forms import ModelForm
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class PCBuildForm(forms.ModelForm):
    class Meta:
        model = PCBuild
        fields = ['Name','CPU', 'GPU', 'Motherboard', 'RAM', 'PSU', 'SSD_Storage', 'HDD_Storage', 'Case', 'CPU_Cooler']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter PC Build Name'}),
            'cpu': forms.Select(attrs={'class': 'form-control'}),
            'gpu': forms.Select(attrs={'class': 'form-control'}),
            'motherboard': forms.Select(attrs={'class': 'form-control'}),
            'ram': forms.Select(attrs={'class': 'form-control'}),
            'psu': forms.Select(attrs={'class': 'form-control'}),
            'ssd_storage': forms.Select(attrs={'class': 'form-control'}),
            'hdd_storage': forms.Select(attrs={'class': 'form-control'}),
            'case': forms.Select(attrs={'class': 'form-control'}),
            'cpu_cooler': forms.Select(attrs={'class': 'form-control'}),
        }