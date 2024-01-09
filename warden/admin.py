# from django.contrib import admin
# from .models import Warden
# from django.contrib.auth.models import Group
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin 
# # Register your models here.

# # Register your models here.
# class WardenInline(admin.StackedInline):
#     model = Warden
#     can_delete = False
#     verbose_name_plural = 'WARDENS'
# class Customwar(UserAdmin):
#     inlines = (WardenInline,)
#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         group, created = Group.objects.get_or_create(name='WARDEN')
#         group.user_set.add(obj)
    
# admin.site.unregister(User)
# admin.site.register(User, Customwar)
# admin.site.register(Warden)

from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Warden

class WardenAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'Hostel_name', 'phone')
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('user', 'username', 'email', 'Hostel_name', 'phone')}),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        group, created = Group.objects.get_or_create(name='WARDEN')
        group.user_set.add(obj.user)

admin.site.register(Warden, WardenAdmin)