from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('technicianlogin/',LoginView.as_view(template_name='technician/technicianlogin.html') , name='technicianlogin'),
    path('logout/',views.logout, name='logout'),
    path('technicianregister/', views.technicianregister, name='technicianregister'),
    path('techniciandashboard/', views.techniciandashboard, name='techniciandashboard'),
]
