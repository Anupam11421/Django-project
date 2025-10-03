from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user:
                login(request, user)
                profile = user.profile
                if profile.user_type == 'patient':
                    return redirect('patient_dashboard')
                else:
                    return redirect('doctor_dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            profile = user.profile
            if profile.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def patient_dashboard(request):
    profile = request.user.profile
    return render(request, 'accounts/patient_dashboard.html', {'profile': profile})

@login_required
def doctor_dashboard(request):
    profile = request.user.profile
    return render(request, 'accounts/doctor_dashboard.html', {'profile': profile})
