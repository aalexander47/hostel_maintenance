from django import forms
from .models import Student, MaintenanceRequest

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['username', 'password', 'email', 'hostel_name', 'room_no', 'phone','enrollment_no']
        


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['name', 'email', 'mobile_number', 'hostel', 'block_room', 'issue_type', 'sub_issue']


