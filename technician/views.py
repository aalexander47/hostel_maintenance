from django.shortcuts import render,redirect
from openpyxl import Workbook
from django.contrib.auth.decorators import login_required
from student.models import MaintenanceRequest
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from datetime import datetime
from pytz import timezone


  # Import the HttpRequest object

def is_techician(user):
    return user.groups.filter(name='TECHNICIAN').exists() # Create your views here.

def is_techicianhead(user):
    return user.groups.filter(name='TECHNICIANHEAD').exists()

@login_required(login_url='stafflogin')
@user_passes_test(is_techician)
def techniciandashboard(request):
    # Fetch maintenance requests that match the technician's work type
    technician_work_type = request.user.technician.work  # replace with the actual field name
    maintenance_requests_list = MaintenanceRequest.objects.filter(issue_type=technician_work_type).order_by('-Priority')

    # Get the search keyword from the query string
    keyword = request.GET.get('q')
    if keyword:
        # Filter the maintenance requests by the keyword
        maintenance_requests_list = maintenance_requests_list.filter(name__icontains=keyword)

    # Get the sorting field from the query string
    sort_by = request.GET.get('sort_by')
    if sort_by:
        # Order the maintenance requests by the sorting field
        maintenance_requests_list = maintenance_requests_list.order_by(sort_by)

    # Create a Paginator object
    paginator = Paginator(maintenance_requests_list, 10)  # Show 10 maintenance requests per page

    # Get the page number from the query string
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    maintenance_requests = paginator.get_page(page_number)

    # Pass the Page object to the template
    return render(request, 'technician/techniciandashboard.html', {'maintenance_requests': maintenance_requests})



@login_required(login_url='stafflogin')
@user_passes_test(is_techicianhead)
def technicianhead(request):
    maintenance_requests_list = MaintenanceRequest.objects.all()

    # Get the search keyword from the query string
    keyword = request.GET.get('q')
    if keyword:
        # Filter the maintenance requests by the keyword
        maintenance_requests_list = maintenance_requests_list.filter(name__icontains=keyword)
    elif keyword:
        maintenance_requests_list = maintenance_requests_list.filter(issue_type__icontains=keyword)
    
    elif keyword:
        maintenance_requests_list = maintenance_requests_list.filter(assign_date__icontains=keyword)
    elif keyword:
        maintenance_requests_list = maintenance_requests_list.filter(status__icontains=keyword)
        
    elif keyword:
        maintenance_requests_list = maintenance_requests_list.filter(hostel__icontains=keyword)
        

    # Get the sorting field from the query string
    sort_by = request.GET.get('sort_by')
    if sort_by:
        # Order the maintenance requests by the sorting field
        maintenance_requests_list = maintenance_requests_list.order_by(sort_by)

    # Create a Paginator object
    paginator = Paginator(maintenance_requests_list, 10)  # Show 10 maintenance requests per page

    # Get the page number from the query string
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    maintenance_requests = paginator.get_page(page_number)

    # Pass the Page object to the template
    return render(request, 'technician/technicianhead.html', {'maintenance_requests': maintenance_requests})


def export_to_excel(request):
    wb = Workbook()
    ws = wb.active

    # Fetch the data from the database
    data = MaintenanceRequest.objects.all()

    # Get the field names and write them to the first row
    field_names = [field.name for field in MaintenanceRequest._meta.fields if not field.name.startswith('_')]
    ws.append(field_names)

    for item in data:
        row = []
        for key, value in item.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, datetime):
                    # Convert the datetime to a specific timezone
                    value = value.astimezone(timezone('Asia/Kolkata'))
                    # Remove the timezone information
                    value = value.replace(tzinfo=None)
                    # Format the datetime as a string
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                row.append(value)
        ws.append(row)

    # Create a response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=data.xlsx'
    wb.save(response)

    return response

def update_message(request, request_id):
    message = MaintenanceRequest.objects.get(id=request_id)
    if request.method == 'POST' and MaintenanceRequest.status == 'In-progress' and MaintenanceRequest.technician == request.user:
        new_message = request.POST.get('message')  # Get the new message from the form data
        message.message = new_message
        message.save()
        messages.success(request, 'Message updated successfully!!!!.')
    else:
        messages.error(request,'Only the technician that is set to In-Progress can Edit the message  !!!!')
    return redirect('techniciandashboard')  # Redirect to the dashboard  # Redirect to the dashboard# Redirect to the dashboard  # Redirect to the dashboard