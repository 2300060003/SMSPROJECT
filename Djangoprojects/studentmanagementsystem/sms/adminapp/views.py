from django.shortcuts import render


# Create your views here.
def projecthomepage(request):
    return render(request,'adminapp/ProjectHomePage.html')

def printpagecall(request):
    return render(request,'adminapp/printer.html')

def printpagelogic(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        print(f'User input: {user_input}')
    a1= {'user_input':user_input}
    return render(request,'adminapp/printer.html',a1)

def exceptionpagecall(request):
    return render(request, 'adminapp/ExceptionExample.html')

def exceptionpagelogic(request):
    if request.method == "POST":
        user_input = request.POST['user_input']
        result = None
        error_message = None
        try:
            num = int(user_input)
            result = 10 / num
        except Exception as e:
            error_message = str(e)
        return render(request, 'adminapp/ExceptionExample.html', {'result': result, 'error': error_message})
    return render(request, 'adminapp/ExceptionExample.html')


import random
import string
def randompagecall(request):
    return render(request,'adminapp/randomexample.html')
def randomlogic(request):
    if request.method == "POST":
        number1 = int(request.POST['number1'])
        ran = ''.join(random.sample(string.ascii_uppercase + string.digits, k=number1))
    a1 = {'ran':ran}
    return render(request,'adminapp/randomexample.html',a1)

def calculatorpagecall(request):
    return render(request,'adminapp/calculator.html')

def calculatorlogic(request):
    result = None
    if request.method == 'POST':
        num1 = float(request.POST.get('num1'))
        num2 = float(request.POST.get('num2'))
        operation = request.POST.get('operation')

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            result = num1 / num2 if num2 != 0 else 'Infinity'

    return render(request, 'adminapp/calculator.html', {'result': result})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_task')
    else:
        form = TaskForm()
    tasks = Task.objects.all()
    return render(request, 'adminapp/add_task.html', {'form': form, 'tasks': tasks})

def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('add_task')

from datetime import datetime, timedelta
from django.shortcuts import render


def daytimepagecall(request):
    return render(request, 'adminapp/datetime.html')


def daytimepagelogic(request):
    if request.method == 'POST':
        number1 = int(request.POST['date1'])
        x = datetime.now()
        ran = x + timedelta(days=number1)
        a1 = {'ran': ran}
        return render(request, 'adminapp/datetime.html', a1)
    else:
        return render(request, 'adminapp/datetime.html')  # Handle non-POST requests


from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render
def UserRegisterPageCall(request):
    return render(request, 'adminapp/UserRegisterPage.html')

def UserRegisterLogic(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        print(username)
        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'OOPS! Username already taken.')
                return render(request, 'adminapp/UserRegisterPage.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'OOPS! Email already registered.')
                return render(request, 'adminapp/UserRegisterPage.html')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=pass1,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
                user.save()
                messages.info(request, 'Account created Successfully!')
                return redirect('projecthomepage')
        else:
            messages.info(request, 'Passwords do not match.')
            return render(request, 'adminapp/UserRegisterPage.html')
    else:
        return render(request, 'adminapp/UserRegisterPage.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def UserLoginPageCall(request):
    return render(request, 'adminapp/UserLoginPage.html')

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def UserLoginLogic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request,user)
            if len(username) == 10:
                # Redirect to StudentHomePage
                messages.success(request, 'Login successful as student!')
                return redirect('studentapp:StudentHomePage')  # Replace with your student homepage URL name
            elif len(username) == 4:
                # Redirect to FacultyHomePage
                messages.success(request, 'Login successful as faculty!')
                return redirect('facultyapp:FacultyHomePage')  # Replace with your faculty homepage URL name
            else:
                # Invalid username length
                messages.error(request, 'Username length does not match student or faculty criteria.')
                return render(request, 'adminapp/UserLoginPage.html')
        else:
            # If authentication fails
            messages.error(request, 'Invalid username or password.')
            return render(request, 'adminapp/UserLoginPage.html')
    else:
        return render(request, 'adminapp/UserLoginPage.html')

def logout(request):
    auth.logout(request)
    return redirect('projecthomepage')

#from .forms import StudentForm
#from .models import StudentList

#def add_student(request):
    #if request.method == 'POST':
        #form = StudentForm(request.POST)
        #if form.is_valid():
            #form.save()
            #return redirect('student_list')
    #else:
        #form = StudentForm()
    #return render(request, 'facultyapp/add_student.html', {'form': form})

from django.contrib.auth.models import User
from .models import StudentList
from .forms import StudentForm
from django.shortcuts import redirect, render
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            register_number = form.cleaned_data['Register_Number']
            try:
                user = User.objects.get(username=register_number)
                student.user = user  # Assign the matching User to the student
            except User.DoesNotExist:
                form.add_error('Register_Number', 'No user found with this Register Number')
                return render(request, 'adminapp/add_student.html', {'form': form})
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'adminapp/add_student.html', {'form': form})

def student_list(request):
    students = StudentList.objects.all()
    return render(request, 'adminapp/student_list.html', {'students': students})

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Feedback

@csrf_protect
def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        description = request.POST['description']

        feedback = Feedback(name=name, email=email, phone=phone, description=description)
        feedback.save()

        return redirect('feedback_success')  # Redirect to a success page or another view
    return render(request, 'adminapp/feedback.html')

def feedback_success(request):
    return render(request, 'adminapp/feedback_success.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def contact_list(request):
    query = request.GET.get('q')
    contacts = Contact.objects.all()
    if query:
        contacts = contacts.filter(name__icontains=query) | contacts.filter(email__icontains=query)
    return render(request, 'adminapp/contact_list.html', {'contacts': contacts})

def contact_add(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            # Send email
            send_mail(
                'New Contact Added',
                f'Contact Details:\nName: {contact.name}\nEmail: {contact.email}\nPhone: {contact.phone_number}\nAddress: {contact.address}',
                settings.DEFAULT_FROM_EMAIL,
                [request.POST.get('email_address')],  # Assuming you have an email field in your form
            )
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'adminapp/contact_form.html', {'form': form})

def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return redirect('contact_list')