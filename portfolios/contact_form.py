from django import forms

class ContactForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    correo = forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea)
    asunto = forms.CharField(max_length=100)
