from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from users.models import User
from student_data.models import Insurance
from django.shortcuts import get_object_or_404

# def login_page(request):
#     return render(request, 'users/login.html')

# def register_page(request):
#     return render(request, 'users/register.html')

def profile_page(request):
    insurance = Insurance.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        # Update student's own profile fields
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.surname = request.POST.get('surname', request.user.surname)
        request.user.patronymic = request.POST.get('patronymic', request.user.patronymic)
        request.user.passport_number = request.POST.get('passport_number', request.user.passport_number)
        request.user.citizenship = request.POST.get('citizenship', request.user.citizenship)
        request.user.address = request.POST.get('address', request.user.address)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.phone_number = request.POST.get('phone_number', request.user.phone_number)
        request.user.save()

        # Update or create insurance
        paid = request.POST.get('insurance_paid')
        application_status = request.POST.get('application_status', '')
        insurance_company = request.POST.get('insurance_company', '')
        policy_number = request.POST.get('policy_number', '')

        if insurance:
            insurance.application_status = application_status
            insurance.insurance_company = insurance_company
            insurance.policy_number = policy_number
            insurance.insurance_fee = 'paid' if paid else ''
            insurance.save()
        else:
            Insurance.objects.create(
                user=request.user,
                insurance_fee='paid' if paid else '',
                application_status=application_status,
                insurance_company=insurance_company,
                policy_number=policy_number,
            )
        
        # Refresh insurance after update
        insurance = Insurance.objects.filter(user=request.user).first()

    return render(request, 'users/profile.html', {
        "show_search": True,
        "student": request.user,
        "insurance": insurance,
    })



#кот пипсика ниже1!!!

def register_page(request):
    if request.method == 'POST':
        # Данные придут с такими именами полей:
        # surname, first_name, patronymic, email, phone_number и т.д.
        data = request.POST
        
        # Создаем пользователя вручную
        user = User.objects.create_user(
            email=data.get('email'),
            password=data.get('password'),
            first_name=data.get('first_name'),
            surname=data.get('surname'),
            patronymic=data.get('patronymic'),
            phone_number=data.get('phone_number'),
            address=data.get('address'),
            passport_number=data.get('passport_number'),
            citizenship=data.get('citizenship'),
            role='student')  # по умолчанию
        login(request, user)
        return redirect('home')
    return render(request, 'users/register.html')


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Авторизуем через email (твой USERNAME_FIELD)
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('/')  # или куда нужно
            else:
                form.add_error(None, "Неверный email или пароль")
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

def admin_all_students_page(request):
    # Only admins should access this view
    if not request.user.is_authenticated or not getattr(request.user, 'is_admin', False):
        return redirect('login')
    
    students = User.objects.filter(role='student').select_related().prefetch_related()
    
    # Build a list with student data and related insurance info
    students_data = []
    for student in students:
        insurance = Insurance.objects.filter(user=student).first()
        students_data.append({
            'student': student,
            'insurance': insurance,
        })
    
    return render(request, 'users/all_students.html', {
        'students_data': students_data,
    })


def student_detail_admin(request, id_user):
    # Only admins should access this view
    if not request.user.is_authenticated or not getattr(request.user, 'is_admin', False):
        return redirect('login')

    student = get_object_or_404(User, id_user=id_user)
    insurance = Insurance.objects.filter(user=student).first()

    if request.method == 'POST':
        # Update basic student fields (minimal validation)
        student.first_name = request.POST.get('first_name', student.first_name)
        student.surname = request.POST.get('surname', student.surname)
        student.patronymic = request.POST.get('patronymic', student.patronymic)
        student.passport_number = request.POST.get('passport_number', student.passport_number)
        student.citizenship = request.POST.get('citizenship', student.citizenship)
        student.address = request.POST.get('address', student.address)
        student.email = request.POST.get('email', student.email)
        student.phone_number = request.POST.get('phone_number', student.phone_number)
        student.institute = request.POST.get('institute', student.institute)
        student.group = request.POST.get('group', student.group)
        student.course = request.POST.get('course', student.course)
        student.save()

        # Update or create insurance
        paid = request.POST.get('insurance_paid')
        application_status = request.POST.get('application_status', '')
        insurance_company = request.POST.get('insurance_company', '')
        policy_number = request.POST.get('policy_number', '')

        if insurance:
            insurance.application_status = application_status
            insurance.insurance_company = insurance_company
            insurance.policy_number = policy_number
            # store a simple indicator in insurance_fee when paid checkbox is present
            insurance.insurance_fee = 'paid' if paid else ''
            insurance.save()
        else:
            Insurance.objects.create(
                user=student,
                insurance_fee='paid' if paid else '',
                application_status=application_status,
                insurance_company=insurance_company,
                policy_number=policy_number,
            )

        return redirect('student_detail', id_user=student.id_user)

    return render(request, 'users/student_detail_admin.html', {
        'student': student,
        'insurance': insurance,
    })