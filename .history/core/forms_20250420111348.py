from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .models import CustomUser, Patient
from django.utils.translation import gettext as _

class DoctorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = [
            'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
            'especialidad', 'ciudad_donde_atiende', 'registro_profesional', 'email',
            'phone', 'numero_de_celular', 'identificacion', 'fecha_de_nacimiento',
            'gender', 'password', 'password2'
        ]
        widgets = {
            'fecha_de_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # Optionally set is_staff or add to 'Doctores' group here if needed
        # user.is_staff = True # Example: Make doctors staff by default?
        if commit:
            user.save()
            # Add user to 'Doctores' group (ensure group exists)
            try:
                doctors_group, created = Group.objects.get_or_create(name='Doctores')
                user.groups.add(doctors_group)
            except Exception as e:
                print(f"Warning: Could not add user to 'Doctores' group. Error: {e}")
                # Handle case where Group model might not be ready or exists
        return user


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
            'tipo_de_identificacion', 'numero_de_identificacion', 'fecha_de_nacimiento',
            'estado_civil', 'gender', 'zona_residencia', 'numero_de_celular',
            'direccion', 'email', 'motivo_consulta', 'alarma', 'compromiso_sistemico',
            'medicacion', 'alergias', 'antecedentes_familiares', 'antecedentes_medicos',
            'tipo_ubicacion_usuario'
        ]
        widgets = {
            'fecha_de_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'motivo_consulta': forms.Textarea(attrs={'rows': 3}),
            'alarma': forms.Textarea(attrs={'rows': 3}),
            'compromiso_sistemico': forms.Textarea(attrs={'rows': 3}),
            'medicacion': forms.Textarea(attrs={'rows': 3}),
            'alergias': forms.Textarea(attrs={'rows': 3}),
            'antecedentes_familiares': forms.Textarea(attrs={'rows': 3}),
            'antecedentes_medicos': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_numero_de_identificacion(self):
        numero_id = self.cleaned_data.get('numero_de_identificacion')
        if Patient.objects.filter(numero_de_identificacion=numero_id).exists():
            raise forms.ValidationError("A patient with this identification number already exists.")
        return numero_id


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
