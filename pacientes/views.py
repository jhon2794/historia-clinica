from django.shortcuts import render ,redirect ,  get_object_or_404
from django.contrib import messages
from .models import Paciente , HistoriaClinica , Evolucion
from django.contrib.auth.decorators import login_required
@login_required
def inicio(request):
    return render(request, 'pacientes/inicio.html')
@login_required
def lista_pacientes(request):
    # 🔹 Trae todos los pacientes de la base de datos
    # SQL equivalente: SELECT * FROM paciente;
    pacientes = Paciente.objects.all()
    identificacion = request.GET.get('identificacion')

    if identificacion:
        pacientes = pacientes.filter(
            identificacion__icontains=identificacion
        )
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
    return render(request, "pacientes/lista_pacientes.html", {"pacientes": pacientes,"rol": rol})
@login_required
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

    return render(request, "pacientes/crear_paciente.html" )

@login_required
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
    return render(request, "pacientes/editar_paciente.html", {"paciente": paciente})

@login_required
def eliminar_paciente(request, id):

    # Busca el paciente por id
    paciente = Paciente.objects.get(id=id)

    # Elimina el registro
    paciente.delete()

    # Regresa al listado
    return redirect('lista_pacientes')

@login_required
def lista_historias(request):

    # Trae todas las historias clínicas
    historias = HistoriaClinica.objects.all()

    # Envía las historias al HTML
    return render(
        request,
        'pacientes/lista_historias.html',
        {'historias': historias}
    )
@login_required
def ver_historia(request, id):
    historia = HistoriaClinica.objects.get(id=id)
    return render(request, "pacientes/ver_historia.html", {"historia": historia})
@login_required
def crear_historia(request, id=None):

    paciente = None

    # Si viene desde la lista de pacientes
    if id:
        paciente = get_object_or_404(
            Paciente,
            id=id
        )

        print("PACIENTE:", paciente)

    if request.method == 'POST':

        # Si NO vino paciente por URL
        if not paciente:

            paciente = get_object_or_404(
                Paciente,
                id=request.POST['paciente']
            )

        # Validar que no exista otra historia
        if HistoriaClinica.objects.filter(
            paciente=paciente
        ).exists():

            messages.error(
                request,
                "Ya existe una historia clínica asociada a este paciente."
            )

            return redirect('lista_historias')

        # Crear historia clínica
        HistoriaClinica.objects.create(

            fecha_apertura=request.POST['fecha_apertura'],

            paciente=paciente,

            motivo_consulta=request.POST['motivo_consulta'],

            enfermedad_actual=request.POST['enfermedad_actual'],

            antecedentes=request.POST['antecedentes'],

            diagnostico_inicial=request.POST['diagnostico_inicial'],

            creado_por=request.user

        )

        messages.success(
            request,
            "Historia clínica creada correctamente."
        )

        return redirect('lista_historias')

    # Solo cargar pacientes sin historia
    pacientes = []

    if not paciente:

        for p in Paciente.objects.all():

            if not HistoriaClinica.objects.filter(
                paciente=p
            ).exists():

                pacientes.append(p)

    return render(request,'pacientes/crear_historia.html',{'paciente': paciente,'pacientes': pacientes})
@login_required
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
        actualizado_por=request.user


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
@login_required
# Elimina una historia clínica
def eliminar_historia(request, id):

    # Busca la historia por id
    historia = HistoriaClinica.objects.get(id=id)

    # Elimina el registro
    historia.delete()

    # Regresa al listado
    return redirect('lista_historias')
@login_required
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
@login_required
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

            talla=request.POST['talla'],
            profesional=request.user,
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
@login_required
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
        actualizado_por=request.user

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
@login_required
def eliminar_evolucion(request, evolucion_id):

    evolucion = Evolucion.objects.get(id=evolucion_id)

    historia_id = evolucion.historia.id

    evolucion.delete()

    return redirect(
        'lista_evoluciones',
        historia_id=historia_id
    )    
