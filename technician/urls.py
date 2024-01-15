from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [

    path('techniciandashboard/', views.techniciandashboard, name='techniciandashboard'),
]
