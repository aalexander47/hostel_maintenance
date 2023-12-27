from django.urls import include, path
from  . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
  
  path('',views.main ,name='main'),
  path('wardenlogin/',views.wardenlogin,name='wardenlogin'),
  path('wardenregister/', views.wardenregister, name='wardenregister'),
  path('wardendashboard/', views.wardendashboard, name='wardendashboard'),
  path('warden_view_problems/', views.warden_view_problems, name='warden_view_problems'),
  path('warden_view_pending/', views.warden_view_pending, name='warden_view_pending'),
  path('warden_view_ongoing/', views.warden_view_ongoing, name='warden_view_ongoing'),
  path('warden_view_completed/', views.warden_view_completed, name='warden_view_completed'),
  path('warden_view_students/', views.warden_view_students, name='warden_view_students'),
  path('warden_view_technicians/', views.warden_view_technicians, name='warden_view_technicians'),
    
]