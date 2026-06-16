from django.shortcuts import render ,redirect ,  get_object_or_404
from django.contrib import messages
from .models import Paciente , HistoriaClinica , Evolucion
from django.contrib.auth.decorators import login_required
from decimal import Decimal
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

        if Paciente.objects.filter(
         identificacion=request.POST['identificacion']).exists():

         messages.error(request,"Ya existe un paciente registrado con esa identificación.")

         return render(request,'pacientes/crear_paciente.html',
            {'request': request})

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
     if Paciente.objects.filter(identificacion=request.POST['identificacion']).exclude(id=paciente.id).exists():

         messages.error(request,"Ya existe un paciente registrado con esa identificación.")

         return render(request,
            'pacientes/editar_paciente.html',
            {'paciente': paciente}
            )

        # Actualiza los datos
     paciente.tipo_documento = request.POST['tipo_documento']
     paciente.identificacion = request.POST['identificacion']
     paciente.nombre = request.POST['nombre']
     paciente.apellido = request.POST['apellido']
     paciente.fecha_nacimiento = request.POST['fecha_nacimiento']
     paciente.sexo = request.POST['sexo']
     paciente.actualizado_por = request.user

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
    identificacion = request.GET.get('identificacion')

    if identificacion:
     historias = historias.filter(paciente__identificacion__icontains=identificacion)

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
        historia.actualizado_por=request.user


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

    try:

        temperatura = float(
            request.POST['temperatura']
        )

        frecuencia_cardiaca = int(
            request.POST['frecuencia_cardiaca']
        )

        frecuencia_respiratoria = int(
            request.POST['frecuencia_respiratoria']
        )

        saturacion = int(
            request.POST['saturacion']
        )

        peso = float(
            request.POST['peso']
        )

        talla = float(
            request.POST['talla']
        )

    except ValueError:

        messages.error(
            request,
            "Uno o más valores numéricos son inválidos."
        )

        return render(
            request , 
            'pacientes/crear_evolucion.html',
            {'historia': historia})

    if temperatura < 30 or temperatura > 45:

        messages.error(
            request,
            "La temperatura debe estar entre 30 y 45 °C."
        )

        return render(
            request , 
            'pacientes/crear_evolucion.html',
            {'historia': historia})

    if frecuencia_cardiaca < 20 or frecuencia_cardiaca > 250:

        messages.error(
            request,
            "La frecuencia cardíaca debe estar entre 20 y 250."
        )

        return render(
            request , 
            'pacientes/crear_evolucion.html',
            {'historia': historia})

    if frecuencia_respiratoria < 5 or frecuencia_respiratoria > 80:

        messages.error(
            request,
            "La frecuencia respiratoria debe estar entre 5 y 80."
        )

        return render(
            request , 
            'pacientes/crear_evolucion.html',
            {'historia': historia})

    if saturacion < 0 or saturacion > 100:

        messages.error(
            request,
            "La saturación debe estar entre 0 y 100."
        )

        return render(
            request , 'pacientes/crear_evolucion.html',
            {'historia': historia})

    if peso < 1 or peso > 500:

        messages.error(
            request,
            "El peso debe estar entre 1 y 500 kg."
        )

        return render(
            request , 'pacientes/crear_evolucion.html',
            {'historia': historia})
        

    if talla < 0.30 or talla > 3:

        messages.error(
            request,
            "La talla debe estar entre 0.30 y 3 metros."
        )

        return render(
            request , 'pacientes/crear_evolucion.html',
            {'historia': historia})
    # Crear evolución
    Evolucion.objects.create(

        historia=historia,

        fecha=request.POST['fecha'],

        motivo_consulta=request.POST['motivo_consulta'],

        observaciones=request.POST['observaciones'],

        diagnostico=request.POST['diagnostico'],

        conducta=request.POST['conducta'],

        temperatura=temperatura,

        frecuencia_cardiaca=frecuencia_cardiaca,

        frecuencia_respiratoria=frecuencia_respiratoria,

        presion_arterial=request.POST['presion_arterial'],

        saturacion=saturacion,

        peso=peso,

        talla=talla,

        profesional=request.user,
        )

    return redirect(
        'lista_evoluciones',
        historia_id=historia.id)

 return render(request,'pacientes/crear_evolucion.html',{'historia': historia})
@login_required
def editar_evolucion(request, evolucion_id):

    evolucion = get_object_or_404(
        Evolucion,
        id=evolucion_id
    )

    if request.method == 'POST':

        try:

            temperatura = Decimal(
                request.POST['temperatura']
            )

            frecuencia_cardiaca = int(
                request.POST['frecuencia_cardiaca']
            )

            frecuencia_respiratoria = int(
                request.POST['frecuencia_respiratoria']
            )

            saturacion = int(
                request.POST['saturacion']
            )

            peso = Decimal(
                request.POST['peso']
            )

            talla = Decimal(
                request.POST['talla']
            )

        except ValueError:

            messages.error(
                request,
                "Los datos numéricos ingresados no son válidos."
            )

            return render(
                request,
                'pacientes/editar_evolucion.html',
                {
                    'evolucion': evolucion
                }
            )

        # VALIDACIONES

        if temperatura < 30 or temperatura > 45:

            messages.error(
                request,
                "La temperatura debe estar entre 30 y 45 °C."
            )

            return render(
                request,
                'pacientes/editar_evolucion.html',
                {
                    'evolucion': evolucion
                }
            )

        if frecuencia_cardiaca < 20 or frecuencia_cardiaca > 250:

            messages.error(
                request,
                "La frecuencia cardíaca debe estar entre 20 y 250 lpm."
            )

            return render(
                request,
                'pacientes/editar_evolucion.html',
                {
                    'evolucion': evolucion
                }
            )

        if frecuencia_respiratoria < 5 or frecuencia_respiratoria > 80:

            messages.error(
                request,
                "La frecuencia respiratoria debe estar entre 5 y 80 rpm."
            )

            return render(
                request,
                'pacientes/editar_evolucion.html',
                {
                    'evolucion': evolucion
                }
            )

        if saturacion < 0 or saturacion > 100:

            messages.error(
                request,
                "La saturación debe estar entre 0 y 100%."
            )

            return render(
                request,
                'pacientes/editar_evolucion.html',
                {
                    'evolucion': evolucion
                }
            )

        if peso < 1 or peso > 500:

            messages.error(
                request,
                "El peso debe estar entre 1 y 500 kg."
            )

            return render(
                request,
                'pacientes/editar_evolucion.html',
                {
                    'evolucion': evolucion
                }
            )

        if talla < Decimal('0.30') or talla > Decimal('3.00'):

            messages.error(
                request,
                "La talla debe estar entre 0.30 y 3 metros."
            )

            return render(
                request,
                'pacientes/editar_evolucion.html',
                {
                    'evolucion': evolucion
                }
            )

        # ACTUALIZAR DATOS

        evolucion.fecha = request.POST['fecha']

        evolucion.motivo_consulta = request.POST['motivo_consulta']

        evolucion.observaciones = request.POST['observaciones']

        evolucion.diagnostico = request.POST['diagnostico']

        evolucion.conducta = request.POST['conducta']

        evolucion.temperatura = temperatura

        evolucion.frecuencia_cardiaca = frecuencia_cardiaca

        evolucion.frecuencia_respiratoria = frecuencia_respiratoria

        evolucion.presion_arterial = request.POST['presion_arterial']

        evolucion.saturacion = saturacion

        evolucion.peso = peso

        evolucion.talla = talla

        evolucion.actualizado_por = request.user

        evolucion.save()

        return redirect(
            'lista_evoluciones',
            historia_id=evolucion.historia.id
        )

    return render(
        request,
        'pacientes/editar_evolucion.html',
        {
            'evolucion': evolucion
        }
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
@login_required
def ver_evolucion(request, evolucion_id):

    evolucion = get_object_or_404(
    Evolucion,
    id=evolucion_id)

    return render(request,'pacientes/ver_evolucion.html',{'evolucion': evolucion})






