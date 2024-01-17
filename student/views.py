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
from django.contrib import messages
from warden.models import Warden
from student.models import Student
from technician.models import Feedback
from django.views.decorators.csrf import csrf_exempt



def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def is_technician(user):
    return user.groups.filter(name='TECHNICIAN').exists()

def is_technicianhead(user):
    return user.groups.filter(name='TECHNICIANHEAD').exists()

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
            messages.success(request, 'Student Registered Successfully')
        return redirect('studentregister')
    return render(request, 'student/studentregister.html')

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def studentdashboard(request):
    return render(request,'student/studentdashboard.html')



@user_passes_test(is_technicianhead)
@csrf_exempt
def toggle_priority(request, pk):
    req = MaintenanceRequest.objects.get(pk=pk)
    req.Priority = not req.Priority
    req.save()
    if req.Priority:
        messages.success(request, 'Priority set to high ')
    else:
        messages.success(request, 'Priority set to normal ')
    return JsonResponse({'success': True})


from django.http import JsonResponse

@login_required(login_url='stafflogin')
@user_passes_test(is_technician)
def update_status(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, id=request_id)
    if maintenance_request.status == 'pending':
        maintenance_request.status = 'In-progress'
        maintenance_request.technician = request.user
    elif maintenance_request.status == 'In-progress':
        if request.user == maintenance_request.technician:
            maintenance_request.status = 'completed'
            if maintenance_request.completion_date is None:
                maintenance_request.completion_date = timezone.now()
                maintenance_request.Duration = maintenance_request.completion_date - maintenance_request.assign_date
            # If Priority is True, set it to False
            if maintenance_request.Priority:
                maintenance_request.Priority = False

            maintenance_request.save()  # Don't forget to save the changes

            messages.success(request, 'Maintenance request completed successfully')
            # Get student's email
            email = maintenance_request.email
            hostel = maintenance_request.hostel
            room = maintenance_request.block_room
            assign_date = maintenance_request.assign_date

            send_mail(
                'Maintenance Request Completed',
                'Your maintenance request has been completed that was submitted on {} ,\nHostel-Name :{} \nRoom-Block :{} \n \n\n\n\n\n\n\n \t this is a generated email || please do not reply \n\n\n\n\t\t\t\t   @fromsupportteam .'.format(assign_date,hostel, room),
                settings.EMAIL_HOST_USER,
                [email],  # Wrap email in a list
                fail_silently=False,
            )
        else:
           messages.error(request, 'Only the technican who set the status to In-progress can set it to completed')
    elif maintenance_request.status == 'completed':
        if request.user == maintenance_request.technician:
            maintenance_request.status = 'completed'
            if maintenance_request.completion_date is None:
                maintenance_request.completion_date = timezone.now()                
        else:
            messages.error(request, 'Only the technican who set the status to In-progress can set it to completed')
    maintenance_request.save()
    return JsonResponse({'new_status': maintenance_request.status})

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
@user_passes_test(is_student)
def complaints_view(request):
    complaints = MaintenanceRequest.objects.filter(Student=request.user.student).order_by('-assign_date')

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



@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def success(request):
    return render(request,'student/success.html')




@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def maintainance(request):
    form = MaintenanceForm()
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            student = request.user.student
            today_min = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_max = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
            maintenance_requests_today = MaintenanceRequest.objects.filter(Student=student, assign_date__range=(today_min, today_max)).count()

            if maintenance_requests_today >=3:
                # The student has already made 3 maintenance requests today
                messages.error(request, 'You have already made 3 maintenance requests today. Please try again tomorrow.')
                return render(request, 'student/maintenance.html')
            maintenance_request = form.save(commit=False)
            maintenance_request.assign_date = timezone.now()
           
            maintenance_request.Student = student
            maintenance_request.save()
            technicians = Technician.objects.filter(work=maintenance_request.issue_type)
            emails = [technician.email for technician in technicians]

            # Get the warden with the same hostel name and add their email to the list of recipient emails
            try:
                warden = Warden.objects.get(Hostel_name=maintenance_request.hostel)
                emails.append(warden.email)
            except Warden.DoesNotExist:
                pass

            # Add the sender's email to the list of recipient emails
            emails.append(request.user.email)

            send_mail(
                'New Maintenance Request',
                'A new maintenance request of type {} has been submitted by {} \nPhone_no:{}\nHostel:{}\nRoom -block:{} \n\n\n\n\n\n\n \t\t\t this is a generated email || please do not reply \n\n\n\n\t\t\t\t   @fromsupportteam .'.format(maintenance_request.issue_type,maintenance_request.name,maintenance_request.mobile_number, maintenance_request.hostel, maintenance_request.block_room),
                settings.EMAIL_HOST_USER,
                emails,
                fail_silently=False,
            )

            return redirect('success')
        else:
            print('Invalid form')
    else:
        form = MaintenanceForm()
    return render(request, 'student/maintenance.html', {'form': form})



def feedback_view(request):
    if request.method == 'POST':
        report = request.POST.get('report')
        rating = request.POST.get('rating')
        maintenance_request_id = request.POST.get('maintenance_request_id')
        student_id = request.POST.get('student_id')
        maintenance_request = MaintenanceRequest.objects.get(id=maintenance_request_id)
        student = Student.objects.get(id=student_id)
        
        if Feedback.objects.filter(maintenance_request=maintenance_request, student=student).exists():
            messages.error(request, 'You have already submitted feedback for this maintenance request.')
            return redirect('feedback_view')
        
        Feedback.objects.create(maintenance_request=maintenance_request, student=student, report=report, rating=rating)

        # Get the technician's email based on the maintenance_request
        email = [maintenance_request.technician.email] 
        try:    
            warden = Warden.objects.get(Hostel_name=maintenance_request.hostel)
            email.append(warden.email)    
        except Warden.DoesNotExist:
            pass

        # Send the email
        send_mail(
            'New Feedback Submitted',
            'A new feedback has been submitted for a maintenance {} request by {} for {}'.format(maintenance_request.issue_type,student.user.username,maintenance_request.technician.username),
            settings.EMAIL_HOST_USER,
            email,  # Send to both technician and warden
            fail_silently=False,
        )
        
        messages.success(request, 'Feedback submitted successfully')

    # Exclude MaintenanceRequest objects that already have a Feedback object associated with them
    feedback_view = MaintenanceRequest.objects.filter(Student=request.user.student, status='completed').exclude(feedback__isnull=False).order_by('-completion_date')



    return render(request, 'student/Feedback.html', {'feedback_view': feedback_view})