from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

class Proyecto(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proyectos')
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']

    def clean(self):
        super().clean()
        self.nombre = self.nombre.strip()
        if not self.nombre:
            raise ValidationError({'nombre': 'Escribe un nombre válido.'})

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        PROGRESO = 'progreso', 'En progreso'
        COMPLETADA = 'completada', 'Completada'

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_limite = models.DateField(null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['estado', 'fecha_limite', '-creado']

    def clean(self):
        super().clean()
        self.titulo = self.titulo.strip()
        if not self.titulo:
            raise ValidationError({'titulo': 'Escribe un título válido.'})

    def __str__(self):
        return self.titulo
