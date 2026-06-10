from django.contrib import admin
from .models import Paciente, HistoriaClinica, Evolucion

admin.site.register(Paciente)
admin.site.register(HistoriaClinica)
admin.site.register(Evolucion)