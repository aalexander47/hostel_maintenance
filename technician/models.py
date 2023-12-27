from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    work = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    
    
    USERNAME_FIELD = ['username','email']
    REQUIRED_FIELDS = ['email', 'work', 'phone']
    
def __str__(self):
    return self.user