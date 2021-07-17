from django import forms

class BuscarForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    correo = forms.EmailField()
    fecha_nacimiento = forms.DateField()
    objetivo = forms.CharField(max_length=100)
    dinero = forms.DecimalField(max_digits=12)
    tiempo = forms.CharField(max_length=2)
    riesgo = forms.DecimalField(max_digits=1)
    metrica = forms.CharField(max_length=100)
