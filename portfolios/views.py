from datetime import date

from django.http import Http404
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .portafolio_helper import PortafolioHelper
from .contact_form import ContactForm
from .buscar_form import BuscarForm
from .email_form import EmailForm
from .models import Usuario, Comentario, UsuarioPortafolio, Portafolio

# Create your views here.
def home(request):
    return render(request, 'homepage.html', { "success": None})

def enviar_mail(request, id = 0):
    try:
        usuario_port = UsuarioPortafolio.objects.get(uuid_string=id)
    except UsuarioPortafolio.DoesNotExist:
        raise Http404("El portafolio no existe.")

    form = EmailForm(request.POST)

    if form.is_valid():
        port = PortafolioHelper(
            filename = usuario_port.portafolio.archivo,
            date = str(usuario_port.portafolio.fecha),
            time = usuario_port.tiempo
        )
        simbolos = port.cargar_simbolos()
        metricas = simbolos[-1]
        metricas["std"] = metricas["std"] * -100
        metricas["return"] = metricas["return"] * 100
        riesgo = {1:"Bajo",2:"Medio",3:"Alto"}
        ganancia = float(usuario_port.dinero) * metricas["return"] / 100
        contenido = render_to_string(
            'email_portafolio.html', {
                "simbolos": simbolos[:-1],
                "metricas": metricas,
                "dinero": usuario_port.dinero,
                "tiempo": usuario_port.tiempo[0],
                "riesgo": riesgo[usuario_port.riesgo],
                "ganancia" : ganancia,
                "email": usuario_port.usuario.correo,
                "id":id
        })
        subject = 'Tu portafolio - ALTEC.dev'
        message = contenido
        email_from = "info@altec.dev"
        recipient_list = [form.cleaned_data.get('correo'),]
        send_mail( subject, message, email_from, recipient_list , html_message=contenido)
    return render(request, 'homepage.html', {"success": "Portafolio enviado!"})

def portafolio(request, id = None):
    try:
        usuario_port = UsuarioPortafolio.objects.get(uuid_string=id)
    except UsuarioPortafolio.DoesNotExist:
        raise Http404("El portafolio no existe.")
    port = PortafolioHelper(
        filename = usuario_port.portafolio.archivo,
        date = str(usuario_port.portafolio.fecha),
        time = usuario_port.tiempo
    )
    market, prices = port.crear_listas()
    simbolos = port.cargar_simbolos()
    metricas = simbolos[-1]
    metricas["std"] = metricas["std"] * -100
    metricas["return"] = metricas["return"] * 100
    riesgo = {1:"Bajo",2:"Medio",3:"Alto"}
    ganancia = float(usuario_port.dinero) * metricas["return"] / 100
    return render(
        request,
        'portafolio.html', {
            "market_x": market[0],
            "market_y": market[1],
            "prices_x": prices[0],
            "prices_y": prices[1],
            "simbolos": simbolos[:-1],
            "metricas": metricas,
            "dinero": usuario_port.dinero,
            "tiempo": usuario_port.tiempo[0],
            "riesgo": riesgo[usuario_port.riesgo],
            "ganancia" : ganancia,
            "email": usuario_port.usuario.correo,
            "id":id
    })

def acerca(request):
    return render(request, 'acerca.html', {})

def ayuda(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ## Insertar mensaje a BD
            try:
                usuario = Usuario.objects.get(correo=form.cleaned_data.get('correo'))
                usuario.nombre = form.cleaned_data.get('nombre')
            except Usuario.DoesNotExist:
                usuario = Usuario(
                    nombre=form.cleaned_data.get('nombre'),
                    correo=form.cleaned_data.get('correo')
                )

            usuario.save()

            comentario = Comentario(
                asunto=form.cleaned_data.get('asunto'),
                mensaje=form.cleaned_data.get('mensaje'),
                fecha=date.today(),
                usuario=usuario
            )
            comentario.save()
            return render(request, 'ayuda.html', {"success": "Mensaje enviado!","error":None})
        else:
            errores = []
            for value in form.errors.as_data().values():
                errores.append(value[0].message)
            return render(request, 'ayuda.html', {"error": errores, "success":None})

    else:
        return render(request, 'ayuda.html', {"error":None, "success":None})

def buscar(request):
    years = list(range(1920, date.today().year - 18))
    years.sort(reverse=True)

    if request.method == 'POST':
        form = BuscarForm(request.POST)
        if form.is_valid():
            ## Buscar portafolio correspondiente
            ## ---------
            try:
                usuario = Usuario.objects.get(correo=form.cleaned_data.get('correo'))
                usuario.nombre = form.cleaned_data.get('nombre')
                usuario.fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
            except Usuario.DoesNotExist:
                usuario = Usuario(
                    nombre=form.cleaned_data.get('nombre'),
                    correo=form.cleaned_data.get('correo'),
                    fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento'),
                )
            usuario.save()
            dinero = form.cleaned_data.get('dinero')
            cantidad_acciones = 5
            metrica = form.cleaned_data.get('metrica')
            if (dinero > 50000):
                cantidad_acciones = 9
            if (dinero > 125000):
                cantidad_acciones = 15

            portafolio = Portafolio.objects.order_by('-fecha').filter(
                dinero = cantidad_acciones,
                riesgo = form.cleaned_data.get('riesgo'),
                tiempo = form.cleaned_data.get('tiempo'),
                metrica = metrica
            )[0]

            print(portafolio.archivo)
            unique_id = get_random_string(length=32)

            usuario_port = UsuarioPortafolio(
                usuario = usuario,
                fecha_visita=date.today(),
                riesgo=form.cleaned_data.get('riesgo'),
                tiempo=form.cleaned_data.get('tiempo'),
                dinero=dinero,
                uuid_string = unique_id,
                objetivo=form.cleaned_data.get('objetivo'),
                metrica=form.cleaned_data.get('metrica'),
                portafolio=portafolio
            )

            usuario_port.save()
            return render(request, 'buscando.html', { "id": usuario_port.uuid_string })
        else:
            errores = []
            for value in form.errors.as_data().values():
                errores.append(value[0].message)
            return render(request, 'buscar.html', {"error": errores, "success":None, "years": years})

    else:
        return render(request, 'buscar.html', {"error":None, "success":None, "years": years})

def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ## Insertar mensaje a BD
            try:
                usuario = Usuario.objects.get(correo=form.cleaned_data.get('correo'))
            except Usuario.DoesNotExist:
                usuario = Usuario(
                    nombre=form.cleaned_data.get('nombre'),
                    correo=form.cleaned_data.get('correo')
                )
                usuario.save()

            comentario = Comentario(
                asunto=form.cleaned_data.get('asunto'),
                mensaje=form.cleaned_data.get('mensaje'),
                fecha=date.today(),
                usuario=usuario
            )
            comentario.save()
            return render(request, 'contacto.html', {"success": "Mensaje enviado!","error":None})
        else:
            errores = []
            for value in form.errors.as_data().values():
                errores.append(value[0].message)
            return render(request, 'contacto.html', {"error": errores, "success":None})

    else:
        return render(request, 'contacto.html', {"error":None, "success":None})
