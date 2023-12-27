from django import forms
from .models import Technician


class TechnicianRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    
    class Meta:
        model = Technician
        fields = ['username', 'password', 'email', 'work', 'phone']
    