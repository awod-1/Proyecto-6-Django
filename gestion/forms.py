from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Proyecto, Tarea

class RegistroForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico', required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 4})}

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'estado', 'fecha_limite']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'fecha_limite': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
