
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Q

from .models import Student
from .forms import StudentForm

def staff_check(user):
    return user.is_authenticated and user.is_staff

# ORIGINAL MODULE 06 REGISTRATION
def student_registration(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        contact_no = request.POST.get('contact_no')

        Student.objects.create(
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            contact_no=contact_no
        )

        return redirect('registration_success')

    return render(request, 'registration/registration.html')


def registration_success(request):
    return render(request, 'registration/success.html')


# ACTIVITY 3: STUDENT DIRECTORY
@user_passes_test(staff_check, login_url='login')
def student_list(request):
    query = request.GET.get('q', '').strip()

    students = Student.objects.all().order_by(
        'last_name', 'first_name'
    )

    if query:
        students = students.filter(
            Q(student_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

    return render(
        request,
        'registration/student_list.html',
        {
            'students': students,
            'query': query,
        }
    )


# ACTIVITY 4: STUDENT DETAIL
@user_passes_test(staff_check, login_url='login')
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)

    return render(
        request,
        'registration/student_detail.html',
        {'student': student}
    )


# ACTIVITY 5: CREATE STUDENT
@user_passes_test(staff_check, login_url='login')
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save()
            messages.success(
                request,
                'Student registered successfully!'
            )
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(
        request,
        'registration/student_form.html',
        {'form': form, 'title': 'Register New Student'}
    )


# ACTIVITY 5: UPDATE STUDENT
@user_passes_test(staff_check, login_url='login')
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Student information updated successfully!'
            )
            return redirect('student_list')

    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'registration/student_form.html',
        {'form': form, 'title': 'Update Student'}
    )


# ACTIVITY 6: SAFE DELETE
@user_passes_test(staff_check, login_url='login')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')

    return render(
        request,
        'registration/student_confirm_delete.html',
        {'student': student}
    )

# ACTIVITY 6: STAFF DASHBOARD
def staff_check(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(staff_check, login_url='login')
def staff_dashboard(request):
    return render(
        request,
        'registration/dashboard.html'
    )