from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # Remove username field, use email as the unique identifier
    username = None
    email = models.EmailField(_('email address'), unique=True)

    # Doctor specific fields
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)
    especialidad = models.CharField(max_length=150, blank=True, null=True)
    ciudad_donde_atiende = models.CharField(max_length=100, blank=True, null=True)
    registro_profesional = models.CharField(max_length=50, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True) # Assuming landline
    numero_de_celular = models.CharField(max_length=20, blank=True, null=True)
    identificacion = models.CharField(max_length=30, blank=True, null=True, unique=True)
    fecha_de_nacimiento = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['primer_nombre', 'primer_apellido'] # Required fields when creating user via createsuperuser

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_set", # Unique related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_set", # Unique related_name
        related_query_name="user",
    )

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.primer_nombre} {self.primer_apellido}".strip()

    def get_short_name(self):
        return self.primer_nombre

class Patient(models.Model):
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patients') # Link patient to doctor
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True, null=True)

    TIPO_ID_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('RC', 'Registro Civil'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
        ('OT', 'Otro'),
    ]
    tipo_de_identificacion = models.CharField(max_length=2, choices=TIPO_ID_CHOICES)
    numero_de_identificacion = models.CharField(max_length=30, unique=True)
    fecha_de_nacimiento = models.DateField()

    ESTADO_CIVIL_CHOICES = [
        ('S', 'Soltero/a'),
        ('C', 'Casado/a'),
        ('U', 'Unión Libre'),
        ('D', 'Divorciado/a'),
        ('V', 'Viudo/a'),
    ]
    estado_civil = models.CharField(max_length=1, choices=ESTADO_CIVIL_CHOICES, blank=True, null=True)
    GENDER_CHOICES = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    ZONA_RESIDENCIA_CHOICES = [('U', 'Urbana'), ('R', 'Rural')]
    zona_residencia = models.CharField(max_length=1, choices=ZONA_RESIDENCIA_CHOICES, blank=True, null=True)
    numero_de_celular = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Medical History
    motivo_consulta = models.TextField(blank=True, null=True)
    alarma = models.TextField(blank=True, null=True) # Consider better field type if structured
    compromiso_sistemico = models.TextField(blank=True, null=True)
    medicacion = models.TextField(blank=True, null=True)
    alergias = models.TextField(blank=True, null=True)
    antecedentes_familiares = models.TextField(blank=True, null=True)
    antecedentes_medicos = models.TextField(blank=True, null=True)

    TIPO_UBICACION_CHOICES = [
        ('H', 'Hogar'),
        ('T', 'Trabajo'),
        ('E', 'Estudio'),
        ('O', 'Otro'),
    ]
    tipo_ubicacion_usuario = models.CharField(max_length=1, choices=TIPO_UBICACION_CHOICES, blank=True, null=True)

    # Add fields for odontogram data later if needed
    # schemaSVG_data = models.JSONField(blank=True, null=True) # Example

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} ({self.numero_de_identificacion})"
