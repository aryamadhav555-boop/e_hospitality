
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import get_user_model




def home(request):
    return render(request, "home.html")


User = get_user_model()


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        # Create user properly (hashes password automatically)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        # Auto login
        login(request, user)

        # Redirect based on role
        if role == "PATIENT":
            return redirect("patient_dashboard")
        elif role == "DOCTOR":
            return redirect("doctor_dashboard")
        else:
            return redirect("home")

    return render(request, "accounts/register.html")


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'ADMIN':
                return redirect('/admin/')
            elif user.role == 'DOCTOR':
                return redirect('/doctors/dashboard/')
            elif user.role == 'PATIENT':
                return redirect('/patients/dashboard/')

    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')