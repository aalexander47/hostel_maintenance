from django.urls import path
from . import views

urlpatterns = [

    path('techniciandashboard/', views.techniciandashboard, name='techniciandashboard'),
    path('technicianhead/', views.technicianhead, name='technicianhead'),
    path('export_to_excel/', views.export_to_excel, name='export_to_excel'),
    path('update_message/<int:request_id>/', views.update_message, name='update_message'),
    
]
