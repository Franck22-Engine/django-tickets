from django.db import models

# Create your models here.

#definimos nuestra clase ticket para crear la BD con sus campos respectivos
class Ticket(models.Model):
    sender = models.EmailField(default=" ")
    subject = models.CharField(max_length=255, default=" ")
    body = models.TextField(default=" ")
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])
    asignar = models.CharField(max_length=20, choices=[
        ('', 'sin asignar'),
        ('Davis Hernandez', 'Davis Hernandez'),
        ('Libby Arias', 'Libby Arias'),
        ('Katherine Monterroso', 'Katherine Monterroso'),
        ('Daniel Hall', 'Daniel Hall')
        
    ],
    default=''
    )
    categorias = models.CharField(max_length=30, choices= [
        ('', 'sin categoria'),
        ('red', 'Red'),
        ('Impresoras', 'Impresoras'),
        ('Disco_duro', 'Disco duro'),
        ('Aplicaciones', 'Aplicaciones')
    ],
    default=''
    )
    # nos permite cerrar el ticket 
    closed = models.BooleanField(default=False)


#modelo para guardar los datos de servidor SMTP
class ConfiguracionCorreo(models.Model):
    smtp_host = models.CharField(max_length=255)
    smtp_port = models.IntegerField()
    smtp_user = models.CharField(max_length=255)
    smtp_password = models.CharField(max_length=255) 

    def __str__(self):
        return self.title