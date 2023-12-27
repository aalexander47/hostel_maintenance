from django.shortcuts import render,redirect,get_object_or_404
from technician.models import Technician
from django.utils import timezone
from .forms import StudentRegistrationForm,MaintenanceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from .models import MaintenanceRequest
from django.core.mail import send_mail
from django.conf import settings



def is_student(user):
    return user.groups.filter(name='STUDENT').exists()
def studentlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('studentdashboard')  # replace 'home' with the name of your home view
       
    return render(request, 'student/studentlogin.html')

def studentregister(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            student = form.save(commit=False)
            student.user = user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return redirect('studentlogin')
    return render(request, 'student/studentregister.html')

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def studentdashboard(request):
    return render(request,'student/studentdashboard.html')





@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def maintainance(request):
    form = MaintenanceForm()
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.assign_date = timezone.now()
            student = request.user.student
            maintenance_request.Student = student
            maintenance_request.save()

            technicians = Technician.objects.filter(work=maintenance_request.issue_type)
            emails = [technician.email for technician in technicians]

            # # Add the sender's email to the list of recipient emails
            emails.append(request.user.email)

            send_mail(
                'New Maintenance Request',
                'A new maintenance request of type {} has been submitted. \n Hostel : {} \n Room -block: {} \n\n\n\n\n\n\n \t\t\t this is a generated email || please do not reply \n\n\n\n\t\t\t\t   @fromsupportteam .'.format(maintenance_request.issue_type, maintenance_request.hostel, maintenance_request.block_room),
                settings.EMAIL_HOST_USER,
                emails,
                fail_silently=False,
            )

            return redirect('studentdashboard')
        else:
            print('Invalid form')
    else:
        form = MaintenanceForm()
    return render(request, 'student/maintenance.html', {'form': form})
@login_required(login_url='technicianlogin')
def update_status(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, id=request_id)
    if maintenance_request.status == 'pending':
        maintenance_request.status = 'In-progress'
    elif maintenance_request.status == 'In-progress':
        maintenance_request.status = 'completed'
    elif maintenance_request.status == 'completed':
        maintenance_request.status = 'completed'
        maintenance_request.completion_date = timezone.now()
    maintenance_request.save()
    return JsonResponse({'new_status': maintenance_request.status})
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def get_user_profile(request):
    user = request.user
    data = {
        'name': user.username,
        'email': user.email,
        # Add more fields as needed
    }
    return JsonResponse(data)


from .models import MaintenanceRequest
from django.core.paginator import Paginator
@login_required(login_url='studentlogin')
def complaints_view(request):
    complaints = MaintenanceRequest.objects.filter(Student=request.user.student)

    # Get the search keyword from the query string
    keyword = request.GET.get('q')
    if keyword:
        # Filter the maintenance requests by the keyword
        complaints = complaints.filter(issue_type__icontains=keyword) 

    # Get the sorting field from the query string
    sort_by = request.GET.get('sort_by')
    if sort_by:
        # Order the maintenance requests by the sorting field
        complaints = complaints.order_by(sort_by) 

    # Create a Paginator object
    paginator = Paginator(complaints, 10)  # Show 10 maintenance requests per page

    # Get the page number from the query string
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    complaints = paginator.get_page(page_number)
   
    return render(request, 'student/complaints_view.html', {'complaints': complaints})
