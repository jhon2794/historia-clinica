from django.shortcuts import render ,redirect 
from django.contrib import messages
from .models import Paciente , HistoriaClinica , Evolucion

def inicio(request):
    return render(request, 'pacientes/inicio.html')

def lista_pacientes(request):
    # 🔹 Trae todos los pacientes de la base de datos
    # SQL equivalente: SELECT * FROM paciente;
    pacientes = Paciente.objects.all()
    # detectar rol
    rol = None

    if request.user.groups.filter(name="medico").exists():
        rol = "medico"
    elif request.user.groups.filter(name="enfermero").exists():
        rol = "enfermero"
    elif request.user.groups.filter(name="admin").exists():
        rol = "admin"

    # 🔹 Envía los datos al template HTML
    # 'pacientes' será la variable disponible en el HTML
    return render(request, "pacientes/lista_pacientes.html", {
    "rol": rol
})

from django.shortcuts import render, redirect
from .models import Paciente

def crear_paciente(request):

    if request.method == "POST":

        tipo_documento = request.POST["tipo_documento"]
        identificacion = request.POST["identificacion"]
        nombre = request.POST["nombre"]
        apellido = request.POST["apellido"]
        fecha_nacimiento = request.POST["fecha_nacimiento"]
        sexo = request.POST["sexo"]

        Paciente.objects.create(
            tipo_documento=tipo_documento,
            identificacion=identificacion,
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            creado_por=request.user
        )

        return redirect("lista_pacientes")

    return render(request, "pacientes/crear_paciente.html")

def editar_paciente(request, id):

    # Busca el paciente por id
    paciente = Paciente.objects.get(id=id)

    # Si enviaron el formulario
    if request.method == 'POST':

        # Actualiza los datos
        paciente.tipo_documento = request.POST['tipo_documento']
        paciente.identificacion = request.POST['identificacion']
        paciente.nombre = request.POST['nombre']
        paciente.apellido = request.POST['apellido']
        paciente.fecha_nacimiento = request.POST['fecha_nacimiento']
        paciente.sexo = request.POST['sexo']

        actualizado_por = request.user

        # Guarda cambios
        paciente.save()

        # Regresa al listado
        return redirect('lista_pacientes')

    # Muestra el formulario con datos existentes
    return render(
        request,
        'pacientes/editar_paciente.html',
        {'paciente': paciente}
    )

def eliminar_paciente(request, id):

    # Busca el paciente por id
    paciente = Paciente.objects.get(id=id)

    # Elimina el registro
    paciente.delete()

    # Regresa al listado
    return redirect('lista_pacientes')
def lista_historias(request):

    # Trae todas las historias clínicas
    historias = HistoriaClinica.objects.all()

    # Envía las historias al HTML
    return render(
        request,
        'pacientes/lista_historias.html',
        {'historias': historias}
    )

def crear_historia(request):
   

    if request.method == 'POST':
        

        paciente = Paciente.objects.get(
            id=request.POST['paciente']
        )
           
         
        if HistoriaClinica.objects.filter(
            paciente=paciente
        ).exists():

            messages.error(
                request,
                "Ya existe una historia clínica asociada a este paciente."
            )

            return redirect('lista_historias')
        
        # Crear historia
        HistoriaClinica.objects.create(

            fecha_apertura=request.POST['fecha_apertura'],

            paciente=paciente,

            motivo_consulta=request.POST['motivo_consulta'],

            enfermedad_actual=request.POST['enfermedad_actual'],

            antecedentes=request.POST['antecedentes'],

            diagnostico_inicial=request.POST['diagnostico_inicial']

        )

        return redirect('lista_historias')

    # Lista de pacientes disponibles
    pacientes = []

    # Recorremos todos los pacientes
    for paciente in Paciente.objects.all():

    # Si NO tiene historia clínica
     if not HistoriaClinica.objects.filter(paciente=paciente).exists():

        # Lo agregamos a la lista
        pacientes.append(paciente)

    return render(
        request,
        'pacientes/crear_historia.html',
        {'pacientes': pacientes}
    )


# Editar una historia clínica existente
def editar_historia(request, id):

    # Busca la historia por id
    historia = HistoriaClinica.objects.get(id=id)

    # Si enviaron el formulario
    if request.method == 'POST':

        # Busca el paciente seleccionado
        paciente = Paciente.objects.get(
            id=request.POST['paciente']
        )

        # Actualiza los datos
        historia.fecha_apertura = request.POST['fecha_apertura']
        historia.paciente = paciente
        historia.motivo_consulta = request.POST['motivo_consulta']
        historia.enfermedad_actual = request.POST['enfermedad_actual']
        historia.antecedentes = request.POST['antecedentes']
        historia.diagnostico_inicial = request.POST['diagnostico_inicial']

        # Guarda los cambios
        historia.save()

        # Regresa al listado
        return redirect('lista_historias')

    # Lista de pacientes para el combo
    pacientes = Paciente.objects.all()

    # Muestra el formulario con datos precargados
    return render(
        request,
        'pacientes/editar_historia.html',
        {
            'historia': historia,
            'pacientes': pacientes
        }
    )

# Elimina una historia clínica
def eliminar_historia(request, id):

    # Busca la historia por id
    historia = HistoriaClinica.objects.get(id=id)

    # Elimina el registro
    historia.delete()

    # Regresa al listado
    return redirect('lista_historias')
def lista_evoluciones(request, historia_id):

    # Buscar la historia clínica
    historia = HistoriaClinica.objects.get(
        id=historia_id
    )

    # Traer las evoluciones de esa historia
    evoluciones = Evolucion.objects.filter(
        historia=historia
    )

    # Enviar datos al HTML
    return render(
        request,
        'pacientes/lista_evoluciones.html',
        {
            'historia': historia,
            'evoluciones': evoluciones
        }
    )
def crear_evolucion(request, historia_id):

    # Buscar la historia clínica
    historia = HistoriaClinica.objects.get(
        id=historia_id
    )

    # Si enviaron el formulario
    if request.method == 'POST':

        # Crear evolución
        Evolucion.objects.create(

            # Historia asociada
            historia=historia,

            # Datos de la evolución
            fecha=request.POST['fecha'],

            motivo_consulta=request.POST['motivo_consulta'],

            observaciones=request.POST['observaciones'],

            diagnostico=request.POST['diagnostico'],

            conducta=request.POST['conducta'],

            temperatura=request.POST['temperatura'],

            frecuencia_cardiaca=request.POST['frecuencia_cardiaca'],

            frecuencia_respiratoria=request.POST['frecuencia_respiratoria'],

            presion_arterial=request.POST['presion_arterial'],

            saturacion=request.POST['saturacion'],

            peso=request.POST['peso'],

            talla=request.POST['talla']
        )

        # Volver al listado de evoluciones
        return redirect(
            'lista_evoluciones',
            historia_id=historia.id
        )

    # Mostrar formulario
    return render(
        request,
        'pacientes/crear_evolucion.html',
        {
            'historia': historia
        }
    )
def editar_evolucion(request, evolucion_id):

    evolucion = Evolucion.objects.get(id=evolucion_id)

    if request.method == 'POST':

        evolucion.fecha = request.POST['fecha']
        evolucion.motivo_consulta = request.POST['motivo_consulta']
        evolucion.observaciones = request.POST['observaciones']
        evolucion.diagnostico = request.POST['diagnostico']
        evolucion.conducta = request.POST['conducta']
        evolucion.temperatura = request.POST['temperatura']
        evolucion.frecuencia_cardiaca = request.POST['frecuencia_cardiaca']
        evolucion.frecuencia_respiratoria = request.POST['frecuencia_respiratoria']
        evolucion.presion_arterial = request.POST['presion_arterial']
        evolucion.saturacion = request.POST['saturacion']
        evolucion.peso = request.POST['peso']
        evolucion.talla = request.POST['talla']

        evolucion.save()

        return redirect(
            'lista_evoluciones',
            historia_id=evolucion.historia.id
        )

    return render(
        request,
        'pacientes/editar_evolucion.html',
        {'evolucion': evolucion}
    )
    
def eliminar_evolucion(request, evolucion_id):

    evolucion = Evolucion.objects.get(id=evolucion_id)

    historia_id = evolucion.historia.id

    evolucion.delete()

    return redirect(
        'lista_evoluciones',
        historia_id=historia_id
    )    
