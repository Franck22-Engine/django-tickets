from django import forms
from .models import Ticket, ConfiguracionCorreo
from django.contrib.auth.models import User
# nos permite realizar el modelo para nuestra bd de tickets
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'asignar', 'categorias']


class UsuarioForm(forms.ModelForm):
    class Meta2:
        model = User
        fields = ['username','last_name','email']
        

class ConfiguracionCorreoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionCorreo
        fields = ['smtp_host', 'smtp_port', 'smtp_user', 'smtp_password']
        widgets = {
            'smtp_password': forms.PasswordInput(),
        }

        
