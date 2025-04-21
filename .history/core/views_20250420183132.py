from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DoctorRegistrationForm, PatientRegistrationForm, CustomLoginForm
from .models import Patient, CustomUser

def register_doctor_view(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend') # Log in the new doctor
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Registration unsuccessful. Please correct the errors below.')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'core/register_doctor.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Redirect if already logged in

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username') # Form uses 'username' for the email field
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome back, {user.get_full_name()}.")
                # Redirect to the URL specified in 'next' parameter or dashboard
                next_url = request.POST.get('next', 'dashboard')
                return redirect(next_url if next_url else 'dashboard') # Fix: Ensure valid URL name or path
            else:
                messages.error(request, "Invalid email or password.")
        else:
             messages.error(request, "Invalid email or password.")
    else:
        form = CustomLoginForm()

    return render(request, 'core/login.html', {'form': form, 'next': request.GET.get('next', '')})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

@login_required
def dashboard_view(request):
    # Ensure the logged-in user is a CustomUser instance
    doctor = request.user
    if not isinstance(doctor, CustomUser):
         # Handle cases where user might not be the expected type (e.g., admin user)
         # Or redirect non-doctors elsewhere
         messages.warning(request, "Access restricted to doctors.")
         return redirect('login')

    context = {
        'doctor_name': doctor.get_full_name()
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def register_patient_view(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.doctor = request.user # Assign the logged-in doctor
            patient.save()
            messages.success(request, f'Patient {patient.primer_nombre} {patient.primer_apellido} registered successfully.')
            # Redirect to patient detail page or back to dashboard?
            return redirect('dashboard') # Redirecting back to dashboard for now
        else:
            messages.error(request, 'Patient registration unsuccessful. Please correct the errors below.')
    else:
        form = PatientRegistrationForm()
    return render(request, 'core/register_patient.html', {'form': form})

# Add views for patient details, editing, odontogram interaction later
