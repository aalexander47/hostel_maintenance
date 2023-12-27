from django.db import models
from django.contrib.auth.models  import User



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hostel_name = models.CharField(max_length=255)
    room_no = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=255)

    
    USERNAME_FIELD = ['username','email']
    REQUIRED_FIELDS = ['email', 'hostel_name', 'room_no', 'phone']

    def __str__(self):
        return self.user
    
    
    
class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('In-progress', 'In-progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending')
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=20)
    hostel = models.CharField(max_length=200)
    block_room = models.CharField(max_length=200)
    issue_type = models.CharField(max_length=200)
    sub_issue = models.CharField(max_length=200)
    other_text = models.TextField(blank=True, null=True)
    assign_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)

    
    
    


    

    
    