import datetime

from django import forms
from django.core.exceptions import ValidationError

class BuscarForm(forms.Form):
    nombre = forms.CharField(max_length=100, error_messages={
        'required': 'Ingresa tu nombre completo.'
    })
    correo = forms.EmailField(error_messages={
        'required': 'Ingresa una direccion de correo electrónico.'
    })
    fecha_nacimiento = forms.DateField(error_messages={
        'required': 'Selecciona una fecha de nacimiento.',
        'invalid': 'Selecciona una fecha de nacimiento válida.'
    })
    objetivo = forms.CharField(max_length=100)
    dinero = forms.DecimalField(max_digits=12, error_messages={
        'required': 'Ingresa la cantidad de dinero que piensas invertir.'
    })
    tiempo = forms.CharField(max_length=2, error_messages={
        'required': 'Selecciona un plazo para la inversion.'
    })
    riesgo = forms.DecimalField(max_digits=1, error_messages={
        'required': 'Selecciona un nivel de riesgo.'
    })
    tipo_portafolio = forms.CharField(max_length=100, error_messages={
        'required': 'Escoge un tipo de portafolio.'
    })
    tyc = forms.CharField(max_length=2, error_messages={
        'required': 'Por favor acepta los términos y condiciones.'
    })

    def clean_objetivo(self):
            data = self.cleaned_data['objetivo']
            if "Seleccionar" in data:
                raise ValidationError("Selecciona algún objetivo para tu inversión.")

            # Always return a value to use as the new cleaned data, even if
            # this method didn't change it.
            return data
