from django import forms
from django.core.exceptions import ValidationError

class EmailForm(forms.Form):
    correo = forms.EmailField(error_messages={
        'required': 'Ingresa tu correo electrónico.'
    })
