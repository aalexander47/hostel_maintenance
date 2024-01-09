from django.contrib.auth.models import User
from django.db import models

class Warden(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    Hostel_name = models.CharField(max_length=255,choices =(('SOE Wing Hostel (D Block)','SOE Wing Hostel (D Block)'),('SOE Wing Hostel ( E Block)','SOE Wing Hostel ( E Block)'),('SOE Wing Hostel (F Block)','SOE Wing Hostel (F Block)'),('Institute of Design ','Institute of Design '),('SOE Wing Hostel (D  Block)','SOE Wing Hostel (D  Block)'),('New Staff Quarters  No 1','New Staff Quarters  No 1'),('New Staff Quarters  No 2','New Staff Quarters  No 2'),('Boat Club','Boat Club'),('Raj','Raj'),('Sangeet Kala Academy','Sangeet Kala Academy'),('Gurukul C Block','Gurukul C Block'),('Institute of Design  No 1','Institute of Design  No 1'),('Institute of Design  No 2','Institute of Design  No 2'),('Anuja 1','Anuja 1'),('Anuja 2','Anuja 2'),('Anuja 3','Anuja 3'),('Anuja 4','Anuja 4'),('Nalini Pride','Nalini Pride'),('Vitthal Krupa','Vitthal Krupa'),('Anuja 5','Anuja 5'),('Anuja 6','Anuja 6'),('Shakuntala','Shakuntala'),('Shree Aangan','Shree Aangan'),('Vaishnavi Pride','Vaishnavi Pride'),('Vaishnavi Complex','Vaishnavi Complex')))
    phone = models.CharField(max_length=255)
    
    USERNAME_FIELD = ['username','email']
    REQUIRED_FIELDS = ['email', 'Hostel_name', 'phone']
    
def __str__(self):
    return self.user.username