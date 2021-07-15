from django.db import models
from django.forms import ModelForm

# Create your models here.
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(unique = True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "usuarios"

class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    asunto = models.CharField(max_length=100)
    mensaje = models.CharField(max_length=2000)
    class Meta:
        db_table = "comentarios"

class Portafolio(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    tiempo = models.CharField(max_length=2)
    riesgo = models.DecimalField(max_digits=1,decimal_places=0)
    dinero = models.DecimalField(max_digits=12,decimal_places=0)
    metrica = models.CharField(max_length=25)
    archivo = models.CharField(max_length=105)
    class Meta:
        db_table = "portafolios"

class UsuarioPortafolio(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    objetivo = models.CharField(max_length=100)
    dinero = models.DecimalField(max_digits=12,decimal_places=0)
    tiempo = models.CharField(max_length=2)
    riesgo = models.DecimalField(max_digits=1,decimal_places=0)
    fecha_visita = models.DateField()
    portafolio = models.ForeignKey(Portafolio, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + " " + self.objetivo

    class Meta:
        db_table = "usuarios_portafolios"
