from django.db import models
from django.contrib.auth.models import User
from student.models import MaintenanceRequest,Student

# Create your models here.
class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    work = models.CharField(max_length=255,choices = (('Electrical','Electrical'),('Civil','Civil'),('Mechanical','Mechanical'),('Chemical','Chemical'),('Housekeeping','Housekeeping')))
    phone = models.CharField(max_length=255)
    
    
    USERNAME_FIELD = ['username','email']
    REQUIRED_FIELDS = ['email', 'work', 'phone']
    
def __str__(self):
    return self.user.username



from django.db import models

class Feedback(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]  # 1 to 5 star rating
    maintenance_request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES)