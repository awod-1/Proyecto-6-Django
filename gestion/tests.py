from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from .models import Proyecto, Tarea
from .forms import ProyectoForm, TareaForm

class GestionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_user('paula', password='ClaveSegura427!')
        cls.otro = User.objects.create_user('otro', password='OtraClave427!')
        cls.proyecto = Proyecto.objects.create(usuario=cls.usuario, nombre='Trabajo')
        cls.tarea = Tarea.objects.create(proyecto=cls.proyecto, titulo='Preparar informe')

    def setUp(self):
        self.client.force_login(self.usuario)

    def test_modelos_y_relaciones(self):
        self.assertEqual(str(self.proyecto), 'Trabajo')
        self.assertEqual(str(self.tarea), 'Preparar informe')
        self.assertEqual(self.usuario.proyectos.count(), 1)
        self.assertEqual(self.proyecto.tareas.count(), 1)

    def test_validacion_modelos(self):
        for obj in [Proyecto(usuario=self.usuario, nombre='  '), Tarea(proyecto=self.proyecto, titulo='  ')]:
            with self.assertRaises(ValidationError):
                obj.full_clean()

    def test_validacion_formularios(self):
        self.assertFalse(ProyectoForm(data={'nombre':'  '}).is_valid())
        self.assertFalse(TareaForm(data={'titulo':'Tarea', 'estado':'inventado'}).is_valid())
        self.assertFalse(TareaForm(data={'titulo':'Tarea', 'estado':'pendiente', 'fecha_limite':'invalida'}).is_valid())

    def test_anonimo_redirigido(self):
        self.client.logout()
        for name, args in [('proyectos', []), ('detalle', [self.proyecto.pk]), ('nuevo_proyecto', []), ('editar_tarea', [self.tarea.pk]), ('nueva_tarea', [self.proyecto.pk])]:
            self.assertEqual(self.client.get(reverse(name,args=args)).status_code,302)

    def test_lista_y_detalle(self):
        Proyecto.objects.create(usuario=self.otro,nombre='Secreto')
        response=self.client.get(reverse('proyectos'))
        self.assertContains(response,'Trabajo')
        self.assertNotContains(response,'Secreto')
        self.assertContains(self.client.get(reverse('detalle',args=[self.proyecto.pk])),'Preparar informe')

    def test_crud_proyecto(self):
        self.assertEqual(self.client.post(reverse('nuevo_proyecto'),{'nombre':'Nuevo','descripcion':'Prueba','usuario':self.otro.pk}).status_code,302)
        obj=Proyecto.objects.get(nombre='Nuevo')
        self.assertEqual(obj.usuario,self.usuario)
        self.client.post(reverse('editar_proyecto',args=[obj.pk]),{'nombre':'Editado','descripcion':''})
        obj.refresh_from_db(); self.assertEqual(obj.nombre,'Editado')
        self.client.get(reverse('eliminar_proyecto',args=[obj.pk]))
        self.assertTrue(Proyecto.objects.filter(pk=obj.pk).exists())
        self.client.post(reverse('eliminar_proyecto',args=[obj.pk]))
        self.assertFalse(Proyecto.objects.filter(pk=obj.pk).exists())

    def test_crud_tarea(self):
        self.client.post(reverse('nueva_tarea',args=[self.proyecto.pk]),{'titulo':'Nueva','estado':'pendiente','fecha_limite':'2026-12-20'})
        obj=Tarea.objects.get(titulo='Nueva')
        self.client.post(reverse('editar_tarea',args=[obj.pk]),{'titulo':'Lista','estado':'completada','fecha_limite':''})
        obj.refresh_from_db(); self.assertEqual(obj.estado,'completada')
        self.client.post(reverse('eliminar_tarea',args=[obj.pk]))
        self.assertFalse(Tarea.objects.filter(pk=obj.pk).exists())

    def test_acceso_ajeno_denegado(self):
        self.client.force_login(self.otro)
        for name,pk in [('detalle',self.proyecto.pk),('editar_proyecto',self.proyecto.pk),('eliminar_proyecto',self.proyecto.pk),('editar_tarea',self.tarea.pk),('eliminar_tarea',self.tarea.pk),('nueva_tarea',self.proyecto.pk)]:
            url=reverse(name,args=[pk])
            self.assertEqual(self.client.get(url).status_code,404)
            self.assertEqual(self.client.post(url,{'nombre':'Intrusión','titulo':'Intrusión','estado':'pendiente'}).status_code,405 if name == 'detalle' else 404)
        self.proyecto.refresh_from_db(); self.assertEqual(self.proyecto.nombre,'Trabajo')

    def test_eliminacion_en_cascada(self):
        self.proyecto.delete()
        self.assertFalse(Tarea.objects.filter(pk=self.tarea.pk).exists())

    def test_registro_login_logout(self):
        self.client.logout()
        response=self.client.post(reverse('registro'),{'username':'nueva','email':'nueva@example.com','password1':'MiClaveFuerte427!','password2':'MiClaveFuerte427!'})
        self.assertRedirects(response,reverse('login'))
        self.assertTrue(User.objects.get(username='nueva').check_password('MiClaveFuerte427!'))
        self.assertRedirects(self.client.post(reverse('login'),{'username':'nueva','password':'MiClaveFuerte427!'}),reverse('proyectos'))
        self.assertEqual(self.client.get(reverse('logout')).status_code,405)
        self.assertRedirects(self.client.post(reverse('logout')),reverse('login'))

    def test_registro_invalido(self):
        self.client.logout()
        response=self.client.post(reverse('registro'),{'username':'nueva','email':'invalido','password1':'123','password2':'456'})
        self.assertEqual(response.status_code,200)
        self.assertFalse(User.objects.filter(username='nueva').exists())

    def test_csrf(self):
        client=Client(enforce_csrf_checks=True)
        client.force_login(self.usuario)
        self.assertEqual(client.post(reverse('nuevo_proyecto'),{'nombre':'Sin token'}).status_code,403)
        self.assertEqual(client.post(reverse('logout')).status_code,403)

    def test_admin(self):
        self.assertEqual(self.client.get(reverse('admin:index')).status_code,302)
        admin=User.objects.create_superuser('admin',email='admin@example.com',password='AdminSegura427!')
        self.client.force_login(admin)
        for name in ['admin:index','admin:gestion_proyecto_changelist','admin:gestion_tarea_changelist','admin:auth_user_changelist']:
            self.assertEqual(self.client.get(reverse(name)).status_code,200)
