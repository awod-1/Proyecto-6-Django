from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProyectoListView.as_view(), name='proyectos'),
    path('proyectos/nuevo/', views.ProyectoCreateView.as_view(), name='nuevo_proyecto'),
    path('proyectos/<int:pk>/', views.ProyectoDetailView.as_view(), name='detalle'),
    path('proyectos/<int:pk>/editar/', views.ProyectoUpdateView.as_view(), name='editar_proyecto'),
    path('proyectos/<int:pk>/eliminar/', views.ProyectoDeleteView.as_view(), name='eliminar_proyecto'),
    path('proyectos/<int:proyecto_pk>/tareas/nueva/', views.TareaCreateView.as_view(), name='nueva_tarea'),
    path('tareas/<int:pk>/editar/', views.TareaUpdateView.as_view(), name='editar_tarea'),
    path('tareas/<int:pk>/eliminar/', views.TareaDeleteView.as_view(), name='eliminar_tarea'),
]
