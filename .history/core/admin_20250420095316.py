from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Patient

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Use email instead of username in admin list/forms
    list_display = ('email', 'primer_nombre', 'primer_apellido', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('email', 'primer_nombre', 'primer_apellido')
    ordering = ('email',)
    # Define fieldsets for the admin change form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'fecha_de_nacimiento', 'gender', 'identificacion', 'phone', 'numero_de_celular')}),
        ('Professional info', {'fields': ('especialidad', 'ciudad_donde_atiende', 'registro_profesional')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'primer_nombre', 'primer_apellido'), # Add fields for user creation
        }),
    )
    # Remove username from default UserAdmin settings
    readonly_fields = ('last_login', 'date_joined')


class PatientAdmin(admin.ModelAdmin):
    list_display = ('primer_nombre', 'primer_apellido', 'numero_de_identificacion', 'doctor', 'created_at')
    list_filter = ('doctor', 'gender', 'estado_civil', 'zona_residencia')
    search_fields = ('primer_nombre', 'primer_apellido', 'numero_de_identificacion', 'email', 'doctor__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información Personal', {'fields': ('doctor', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'tipo_de_identificacion', 'numero_de_identificacion', 'fecha_de_nacimiento', 'estado_civil', 'gender')}),
        ('Información de Contacto', {'fields': ('zona_residencia', 'numero_de_celular', 'direccion', 'email', 'tipo_ubicacion_usuario')}),
        ('Historia Médica', {'fields': ('motivo_consulta', 'alarma', 'compromiso_sistemico', 'medicacion', 'alergias', 'antecedentes_familiares', 'antecedentes_medicos')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Patient, PatientAdmin)
