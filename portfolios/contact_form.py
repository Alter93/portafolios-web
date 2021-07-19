from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100, error_messages={
        'required': 'Ingresa tu nombre completo.'
    })
    correo = forms.EmailField(error_messages={
        'required': 'Ingresa tu correo electrónico.'
    })
    mensaje = forms.CharField(widget=forms.Textarea, error_messages={
        'required': 'Escribe tu mensaje en el espacio en blanco.'
    })
    asunto = forms.CharField(max_length=100)
