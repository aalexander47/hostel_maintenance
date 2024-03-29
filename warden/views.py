from django.conf import settings
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
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from student.forms import StudentRegistrationForm
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse










def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def is_technician(user):
    return user.groups.filter(name='TECHNICIAN').exists()

def is_warden(user):
    return user.groups.filter(name='WARDEN').exists()

def is_technicianhead(user):
    return user.groups.filter(name='TECHNICIANHEAD').exists()

# Create your views here.
def main(request):
    # trigger_refresh = True
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request, 'warden/main.html') #{'trigger_refresh':trigger_refresh}


@login_required(login_url='stafflogin')
@user_passes_test(is_warden)
def student_approve(request):
    return render(request, 'warden/approve.html')

@login_required
def afterlogin(request):
    if is_student(request.user):
        try:
            student = Student.objects.get(user_id=request.user.id)
            if not student.approved:
                return redirect('student_approve')
            else:
                return redirect('student/studentdashboard')
        except Student.DoesNotExist:
            return render(request, 'student/studentregistration.html')
    elif is_technician(request.user):
        return redirect('technician/techniciandashboard')
    elif is_technicianhead(request.user):
        return redirect('technician/technicianhead')
    else:
        is_warden(request.user)
        return redirect('wardendashboard')
    
    
@login_required
def profile(request):
    return render(request,'warden/profile.html')



@login_required(login_url='stafflogin')
@user_passes_test(is_warden)
def wardendashboard(request):
    monthly_requests = MaintenanceRequest.objects.annotate(month=TruncMonth('assign_date')).values('month').annotate(count=Count('id')).values('month', 'count').order_by('month')
    monthly_requests = list(monthly_requests)
    for item in monthly_requests:
        item['month'] = item['month'].isoformat()  # Convert date to ISO 8601 string
    dict = {
        'total_problems': MaintenanceRequest.objects.all().count(),
        'pending_problems': MaintenanceRequest.objects.filter(status='pending').count(),
        'in_progress_problems': MaintenanceRequest.objects.filter(status='In-progress').count(),
        'completed_problems': MaintenanceRequest.objects.filter(status='completed').count(),
        'monthly_requests': json.dumps(list(monthly_requests), cls=DjangoJSONEncoder),
    }
    return render(request, 'warden/warden-dashboard.html' ,{'dict':dict})

def logout_view(request):
    if is_student(request.user):
        student = Student.objects.get(user_id=request.user.id)
        if not student.approved:
            logout(request)
            return redirect('studentlogin')
        else:
            logout(request)
            return redirect('studentlogin')

    elif is_technician(request.user):
        logout(request)
        return redirect('stafflogin')
    elif is_technician(request.user):
        logout(request)
        return redirect('stafflogin')
    else:
        is_warden(request.user)
        logout(request)
        return redirect('stafflogin')


@login_required(login_url='stafflogin')
@user_passes_test(is_warden)
def warden_view_problems(request):
    
    maintenance_requests_list = MaintenanceRequest.objects.all().order_by('-assign_date')

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

@login_required(login_url='stafflogin')
@user_passes_test(is_warden)
def warden_view_pending(request):
    maintenance_requests_list = MaintenanceRequest.objects.filter(status='pending').order_by('-assign_date')

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
   


@login_required(login_url='stafflogin')
@user_passes_test(is_warden)
def warden_view_completed(request):
    maintenance_requests_list = MaintenanceRequest.objects.filter(status='completed').order_by('-assign_date')

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
 


@login_required(login_url='stafflogin')
@user_passes_test(is_warden)
def warden_view_students(request):
    students = Student.objects.all().filter(approved=True)
     

    # Get the search keyword from the query string
    keyword = request.GET.get('q')
    if keyword:
        # Filter the maintenance requests by the keyword
        students = students.filter(username__icontains=keyword) 

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

@login_required(login_url='stafflogin')
@user_passes_test(is_warden)
def warden_view_technicians(request):
    trigger_refresh = True
    technician = Technician.objects.all()

    # Get the search keyword from the query string
    keyword = request.GET.get('q')
    if keyword:
        # Filter the maintenance requests by the keyword
        technician = technician.filter(username__icontains=keyword) 
        
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


@login_required(login_url='stafflogin')
@user_passes_test(is_warden)
def warden_view_ongoing(request):
    maintenance_requests_list = MaintenanceRequest.objects.filter(status='In-progress').order_by('-assign_date')

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

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['currentPassword']
        new_password = request.POST['newPassword']
        user = User.objects.get(username=request.user.username)
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully')
            if user.groups.filter(name='STUDENT').exists():
                return redirect('studentlogin')
            elif user.groups.filter(name='TECHNICIAN').exists():
                return redirect('stafflogin')
            else:
                return redirect('stafflogin')
        else:
            messages.error(request, 'Current password is incorrect')
    return render(request, 'profile.html')


@login_required(login_url='stafflogin')
@user_passes_test(is_warden)
def approve_students(request):
    students_list = Student.objects.filter(approved=False)  # Get all unapproved students
    paginator = Paginator(students_list, 10)  # Show 10 students per page

    page_number = request.GET.get('page')
    students = paginator.get_page(page_number)

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        email = request.POST.get('email')
        action = request.POST.get('action')

        if student_id and action:
            student = Student.objects.get(id=student_id)
            

            if action == 'approve':
                student.approved = True
                student.save()
                messages.success(request, f'Student {student.username} has been approved.')
                send_mail(
                'Account Approved !!',
                'Your Account has been approved  \n \n\n\n\n\n\n\n \t this is a generated email || please do not reply \n\n\n\n\t\t\t\t   @fromsupportteam .',
                settings.EMAIL_HOST_USER,
                email,  # Wrap email in a list
                fail_silently=False,
            )
            elif action == 'delete':
                student.delete()
                messages.success(request, f'Student {student.username} has been deleted.')

        return redirect('approve_students')  # Redirect back to the same page

    # Create a form instance for each student
    forms = [StudentRegistrationForm(instance=student) for student in students]

    return render(request, 'warden/approve-students.html', {'forms': forms, 'students': students})


def staff_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['Role']

        user = authenticate(request, username=username, password=password,groups=role)

        if user is not None:
            try:
                group = Group.objects.get(name=role.upper())
                if group in user.groups.all():
                    login(request, user)
                    if role == 'WARDEN':
                        return redirect('wardendashboard')
                    elif role == 'TECHNICIAN':
                        return redirect('techniciandashboard')
                    else:
                        return render(request, 'warden/staff_login.html', {'error': 'Invalid role for this user.'})
                else:
                    # User is not in the expected group
                    return render(request, 'warden/staff_login.html', {'error': 'Invalid role for this user.'})
            except Group.DoesNotExist:
                # Group does not exist
                return render(request, 'warden/staff_login.html', {'error': 'Invalid role.'})
        else:
            # Invalid login
            return render(request, 'warden/staff_login.html', {'error': 'Invalid username or password.'})

    return render(request, 'warden/staff_login.html')