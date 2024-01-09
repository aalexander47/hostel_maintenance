from django.contrib import admin
from .models import Student,MaintenanceRequest


# Register your models here.
admin.site.register(Student)

admin.site.site_header = "Hostel Maintenance Management System"
admin.site.register(MaintenanceRequest)
