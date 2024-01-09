# from django.contrib import admin
# from .models import Technician
# from django.contrib.auth.models import Group
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin 
# # Register your models here.


# class TechnicianInline(admin.StackedInline):
#     model = Technician
#     can_delete = False
#     verbose_name_plural = 'Technicians'
# class Customtech(UserAdmin):
#     inlines = (TechnicianInline,)
#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         group, created = Group.objects.get_or_create(name='TECHNICIAN')
#         group.user_set.add(obj)
    
# admin.site.unregister(User)
# admin.site.register(User, Customtech)
# admin.site.register(Technician)


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import Technician

class TechnicianInline(admin.StackedInline):
    model = Technician
    can_delete = False
    verbose_name_plural = 'Technicians'

class Customtech(UserAdmin):
    inlines = (TechnicianInline,)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        group, created = Group.objects.get_or_create(name='TECHNICIAN')
        group.user_set.add(obj)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = form.instance
            instance.save()
        formset.save_m2m()

admin.site.unregister(User)
admin.site.register(User, Customtech)
admin.site.register(Technician)