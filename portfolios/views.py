from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'homepage.html', {})

def acerca(request):
    return render(request, 'acerca.html', {})

def ayuda(request):
    return render(request, 'ayuda.html', {})

def buscar(request):
    return render(request, 'buscar.html', {})

def contacto(request):
    return render(request, 'contacto.html', {})
