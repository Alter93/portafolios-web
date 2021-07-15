from datetime import date
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .contact_form import ContactForm
from .buscar_form import BuscarForm
from .models import Usuario, Comentario, UsuarioPortafolio, Portafolio

# Create your views here.
def home(request):
    return render(request, 'homepage.html', {})

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
            return render(request, 'ayuda.html', {"success": "Mensaje enviado!"})
        else:
            return render(request, 'ayuda.html', {"error": form.errors})

    else:
        return render(request, 'ayuda.html', {})

def buscar(request):
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
            metrica = "beta_std_dev"
            if (dinero > 50000):
                cantidad_acciones = 9
            if (dinero > 125000):
                cantidad_acciones = 15

            portafolio = Portafolio.objects.order_by('fecha').filter(
                dinero = cantidad_acciones,
                riesgo = form.cleaned_data.get('riesgo'),
                tiempo = form.cleaned_data.get('tiempo'),
                metrica = metrica
            )[0]
            
            print(portafolio.archivo)

            usuario_port = UsuarioPortafolio(
                usuario = usuario,
                fecha_visita=date.today(),
                riesgo=form.cleaned_data.get('riesgo'),
                tiempo=form.cleaned_data.get('tiempo'),
                dinero=dinero,
                objetivo=form.cleaned_data.get('objetivo'),
                portafolio=portafolio
            )

            usuario_port.save()
            return render(request, 'buscando.html', { "id": usuario_port.id })
        else:
            return render(request, 'buscar.html', {"error": form.errors})

    else:
        return render(request, 'buscar.html', {})

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
            return render(request, 'contacto.html', {"success": "Mensaje enviado!"})
        else:
            return render(request, 'contacto.html', {"error": form.errors})

    else:
        return render(request, 'contacto.html', {})
