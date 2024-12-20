from django.db import models
from django.forms import ModelForm

# Create your models here.
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(unique = True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = "usuarios"

class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    asunto = models.CharField(max_length=100)
    mensaje = models.CharField(max_length=2000)

    def __str__(self):
        return self.usuario.nombre + " - " + self.asunto

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

    def __str__(self):
        return str(self.riesgo) + " " + self.tiempo + " - " + str(self.fecha)

    class Meta:
        db_table = "portafolios"

class UsuarioPortafolio(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    metrica = models.CharField(max_length=25)
    objetivo = models.CharField(max_length=100)
    dinero = models.DecimalField(max_digits=12,decimal_places=0)
    tiempo = models.CharField(max_length=2)
    riesgo = models.DecimalField(max_digits=1,decimal_places=0)
    uuid_string = models.CharField(max_length=33)
    fecha_visita = models.DateField()
    tipo_portafolio = models.CharField(max_length=25, blank=True, null=True)
    portafolio = models.ForeignKey(Portafolio, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.nombre + " " + str(self.fecha_visita)

    class Meta:
        db_table = "usuarios_portafolios"
