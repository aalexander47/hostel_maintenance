from django.urls import  path
from django.contrib.auth.views import LoginView,LogoutView
from . import views

urlpatterns = [
    path('studentlogin/',LoginView.as_view(template_name='student/studentlogin.html'),name='studentlogin'),
    path('studentregister/', views.studentregister, name='studentregister'),
    path('studentdashboard/', views.studentdashboard, name='studentdashboard'),
    path('maintainance/', views.maintainance, name='maintainance'),
    path('complaints_view/', views.complaints_view, name='complaints_view'),
    path('feedback_view/',views.feedback_view,name='feedback_view'),
    path('success', views.success, name='success'),
    
    path('toggle_priority/<int:pk>/', views.toggle_priority, name='toggle_priority'),
    path('update_status/<int:request_id>/', views.update_status, name='update_status'),
    path('get_user_profile/', views.get_user_profile, name='get_user_profile')
]
