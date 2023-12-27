from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User, Group
from . forms import TechnicianRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from student.models import MaintenanceRequest
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import logout



from django.http import HttpRequest  # Import the HttpRequest object

def is_techician(user):
    return user.groups.filter(name='TECHNICIAN').exists() # Create your views here.

def technicianlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        work = request.POST.get('work')
        user = authenticate(request, username=username, password=password, work=work)
        if user is not None:
            login(request, user)
            return redirect('techniciandashboard')

    return render(request, 'technician/technicianlogin.html')

def technicianregister(request):
    if request.method == 'POST':
                form = TechnicianRegistrationForm(request.POST)
                if form.is_valid():
                    user = User.objects.create_user(
                        username=form.cleaned_data.get('username'),
                        password=form.cleaned_data.get('password'),
                        
                    )
                    student = form.save(commit=False)
                    student.user = user
                    student.save()
                    my_technican_group = Group.objects.get_or_create(name='TECHNICIAN')
                    my_technican_group[0].user_set.add(user)
                    messages.success(request, 'Technician Registered Successfully')
                else:
                    messages.error(request, 'Technician Registration Failed')   
                    
                    
                return redirect('technicianlogin')
            
    return render(request, 'technician/technicianregister.html')

@login_required(login_url='technicianlogin')
@user_passes_test(is_techician)
def techniciandashboard(request):
    # Fetch maintenance requests that match the technician's work type
    technician_work_type = request.user.technician.work  # replace with the actual field name
    maintenance_requests_list = MaintenanceRequest.objects.filter(issue_type=technician_work_type)

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




