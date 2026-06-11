from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    # 🔹 Cuando entras a /pacientes/
    # ejecuta la función lista_pacientes
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    # Formulario para crear pacientes
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:id>/', views.editar_paciente,name='editar_paciente'),
    path('pacientes/eliminar/<int:id>/', views.eliminar_paciente, name='eliminar_paciente'),
    path('historias/', views.lista_historias, name='lista_historias'),
    path('historias/ver/<int:id>/', views.ver_historia, name='ver_historia'),
    path('historias/crear/', views.crear_historia, name='crear_historia'),
    path('historias/crear/<int:id>/', views.crear_historia, name='crear_historia_paciente'),
    path('historias/editar/<int:id>/', views.editar_historia, name='editar_historia'),
    path('historias/eliminar/<int:id>/',views.eliminar_historia,name='eliminar_historia'),
    # Lista las evoluciones de una historia clínica
    path('evoluciones/<int:historia_id>/',views.lista_evoluciones,name='lista_evoluciones'),
    # Crear evolución para una historia
    path('evoluciones/crear/<int:historia_id>/',views.crear_evolucion,name='crear_evolucion'),
    # Editar evolución
    path('evoluciones/editar/<int:evolucion_id>/',views.editar_evolucion,name='editar_evolucion'),
    # Eliminar evolución
    path('evoluciones/eliminar/<int:evolucion_id>/',views.eliminar_evolucion,name='eliminar_evolucion'),
]