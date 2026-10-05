from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .forms import RegistroForm, ProyectoForm, TareaForm
from .models import Proyecto, Tarea

class RegistroView(SuccessMessageMixin, CreateView):
    form_class = RegistroForm
    template_name = 'gestion/form.html'
    success_url = reverse_lazy('login')
    success_message = 'Cuenta creada. Ya puedes iniciar sesión.'
    extra_context = {'titulo': 'Crear cuenta'}

class ProyectosPropiosMixin(LoginRequiredMixin):
    model = Proyecto
    def get_queryset(self):
        return Proyecto.objects.filter(usuario=self.request.user)

class ProyectoListView(ProyectosPropiosMixin, ListView):
    template_name = 'gestion/proyectos.html'
    context_object_name = 'proyectos'
    def get_queryset(self):
        return super().get_queryset().annotate(total_tareas=Count('tareas'))

class ProyectoDetailView(ProyectosPropiosMixin, DetailView):
    template_name = 'gestion/detalle.html'
    context_object_name = 'proyecto'

class ProyectoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'gestion/form.html'
    success_url = reverse_lazy('proyectos')
    success_message = 'Proyecto creado.'
    extra_context = {'titulo': 'Nuevo proyecto'}
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class ProyectoUpdateView(ProyectosPropiosMixin, SuccessMessageMixin, UpdateView):
    form_class = ProyectoForm
    template_name = 'gestion/form.html'
    success_message = 'Proyecto actualizado.'
    extra_context = {'titulo': 'Editar proyecto'}
    def get_success_url(self):
        return reverse('detalle', args=[self.object.pk])

class ProyectoDeleteView(ProyectosPropiosMixin, DeleteView):
    template_name = 'gestion/confirmar.html'
    success_url = reverse_lazy('proyectos')

class TareasPropiasMixin(LoginRequiredMixin):
    model = Tarea
    def get_queryset(self):
        return Tarea.objects.filter(proyecto__usuario=self.request.user).select_related('proyecto')
    def get_success_url(self):
        return reverse('detalle', args=[self.object.proyecto_id])

class TareaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'gestion/form.html'
    success_message = 'Tarea creada.'
    extra_context = {'titulo': 'Nueva tarea'}
    def get_proyecto(self):
        return get_object_or_404(Proyecto, pk=self.kwargs['proyecto_pk'], usuario=self.request.user)
    def get(self, request, *args, **kwargs):
        self.get_proyecto()
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        form.instance.proyecto = self.get_proyecto()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('detalle', args=[self.object.proyecto_id])

class TareaUpdateView(TareasPropiasMixin, SuccessMessageMixin, UpdateView):
    form_class = TareaForm
    template_name = 'gestion/form.html'
    success_message = 'Tarea actualizada.'
    extra_context = {'titulo': 'Editar tarea'}

class TareaDeleteView(TareasPropiasMixin, DeleteView):
    template_name = 'gestion/confirmar.html'
