from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Proyecto, Tarea

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'usuario', 'creado']
    list_filter = ['usuario', 'creado']
    search_fields = ['nombre', 'usuario__username']
    autocomplete_fields = ['usuario']

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'proyecto', 'estado', 'fecha_limite']
    list_filter = ['estado', 'fecha_limite']
    search_fields = ['titulo', 'proyecto__nombre']
    autocomplete_fields = ['proyecto']

admin.site.unregister(User)
@admin.register(User)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'groups']

admin.site.site_header = 'Administración de proyectos'
admin.site.site_title = 'Gestión'
admin.site.index_title = 'Usuarios, permisos, proyectos y tareas'
