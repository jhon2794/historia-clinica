from django.db import models
from django.db import models

class Paciente(models.Model):
    # Tipo de documento
    tipo_documento = models.CharField(max_length=5)
   # Número de identificación
    identificacion = models.CharField(max_length=30,unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class HistoriaClinica(models.Model):
    
    paciente = models.OneToOneField(Paciente,on_delete=models.CASCADE)

    fecha_apertura = models.DateField()

    motivo_consulta = models.TextField()

    enfermedad_actual = models.TextField()

    antecedentes = models.TextField()

    diagnostico_inicial = models.TextField()

    def __str__(self):
        return f"Historia #{self.id} - {self.paciente}"  
      
class Evolucion(models.Model):
    historia = models.ForeignKey(
        HistoriaClinica,
        on_delete=models.CASCADE
    )

    fecha = models.DateField()

    motivo_consulta = models.TextField()

    observaciones = models.TextField()

    diagnostico = models.TextField()

    conducta = models.TextField()

    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1
    )

    frecuencia_cardiaca = models.IntegerField()

    frecuencia_respiratoria = models.IntegerField()

    presion_arterial = models.CharField(
        max_length=20
    )

    saturacion = models.IntegerField()

    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    talla = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    def __str__(self):

     return (f"Evolución {self.id} "f"- Historia {self.historia.id}")