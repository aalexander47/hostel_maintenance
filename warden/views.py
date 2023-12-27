from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from student.models import Student,MaintenanceRequest
from technician.models import Technician
from django.core.paginator import Paginator













def is_technician(user):
    return user.groups.filter(name='TECHNICIAN').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()
# Create your views here.
def main(request):
    # trigger_refresh = True
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request, 'warden/main.html') #{'trigger_refresh':trigger_refresh}

def afterlogin(request):
    if is_student(request.user):
        return redirect('studentlogin')
    elif is_technician(request.user):
        return redirect('technicianlogin')
    else:
        return redirect('wardendashboard')
    

def profile(request):
    return render(request,'warden/profile.html')

# def logout(request):
#     return redirect('main')

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def is_technician(user):
    return user.groups.filter(name='TECHNICIAN').exists()


@login_required
def afterlogin(request):
    if is_student(request.user):
        return redirect('student/studentdashboard')
    elif is_technician(request.user):
        return redirect('technician/techniciandashboard')
    return redirect('wardendashboard')


def wardenregister(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']  # Define the variable "email"
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
            else:
                user = User.objects.create_superuser(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Account created for ' + username + '!')
                return redirect('wardenlogin')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'warden/warden_register.html')

def wardenlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('wardendashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request,'warden/warden-login.html')

@login_required(login_url='wardenlogin')
def wardendashboard(request):
    trigger_refresh = True
    return render(request, 'warden/warden-dashboard.html' ,{'trigger_refresh':trigger_refresh})

def logout_view(request):
    logout(request)
    return redirect('main') 


@login_required(login_url='wardenlogin')
def warden_view_problems(request):
    
    maintenance_requests_list = MaintenanceRequest.objects.all()

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

    return render(request, 'warden/warden-view_problems.html', {'maintenance_requests': maintenance_requests} )

@login_required(login_url='wardenlogin')
def warden_view_pending(request):
    maintenance_requests_list = MaintenanceRequest.objects.filter(status='pending')

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
    
    return render(request, 'warden/warden-view_pending.html', {'maintenance_requests': maintenance_requests} )
   


@login_required(login_url='wardenlogin')
def warden_view_completed(request):
    maintenance_requests_list = MaintenanceRequest.objects.filter(status='completed')

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
    
    return render(request, 'warden/warden-view_completed.html', {'maintenance_requests': maintenance_requests} )
 


@login_required(login_url='wardenlogin')
def warden_view_students(request):
    students = Student.objects.all()
     

    # Get the search keyword from the query string
    keyword = request.GET.get('q')
    if keyword:
        # Filter the maintenance requests by the keyword
        students = students.filter(name__icontains=keyword) 

    # Get the sorting field from the query string
    sort_by = request.GET.get('sort_by')
    if sort_by:
        # Order the maintenance requests by the sorting field
        students = students.order_by(sort_by) 

    # Create a Paginator object
    paginator = Paginator(students, 10)  # Show 10 maintenance requests per page

    # Get the page number from the query string
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    students = paginator.get_page(page_number)
    return render(request, 'warden/warden-view_students.html', {'students': students} )

@login_required(login_url='wardenlogin')
def warden_view_technicians(request):
    trigger_refresh = True
    technician = Technician.objects.all()

    # Get the search keyword from the query string
    keyword = request.GET.get('q')
    if keyword:
        # Filter the maintenance requests by the keyword
        technician = technician.filter(name__icontains=keyword) 
        
    elif keyword:
        technician = technician.filter(work__icontains=keyword)

    # Get the sorting field from the query string
    sort_by = request.GET.get('sort_by')
    if sort_by:
        # Order the maintenance requests by the sorting field
        technician = technician.order_by(sort_by)

    # Create a Paginator object
    paginator = Paginator(technician, 10)  # Show 10 maintenance requests per page

    # Get the page number from the query string
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    technician = paginator.get_page(page_number)
    return render(request, 'warden/warden-view_technician.html', {'technician': technician,'trigger_refresh':trigger_refresh} )


@login_required(login_url='wardenlogin')
def warden_view_ongoing(request):
    maintenance_requests_list = MaintenanceRequest.objects.filter(status='ongoing')

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
    return render(request, 'warden/warden-view_ongoing.html', {'maintenance_requests': maintenance_requests} )

