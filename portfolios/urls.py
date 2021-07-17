from django.urls import path
from portfolios import views

urlpatterns = [
    path('', views.home, name='home'),
    path('acerca', views.acerca, name='acerca'),
    path('ayuda', views.ayuda, name='ayuda'),
    path('buscar', views.buscar, name='buscar'),
    path('contacto', views.contacto, name='contacto'),
    path('portafolio/<str:id>', views.portafolio, name='portafolio'),
]
