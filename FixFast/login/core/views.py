from multiprocessing import AuthenticationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
#parte del formulario 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
#librerias para servidor smtp y exchange
from datetime import datetime, timedelta

#renderizacion de todas las paginas
def home(request):
    return render(request, 'core/home.html')

def creaciondeticket(request):
    return render(request, 'core/creaciondeticket.html')

def configuracion(request):
    return render(request, 'core/configuracion.html')

def creaciondeticket(request):
    return render(request, 'core/creaciondeticket.html')

def ticketscerrados(request):
    return render(request, 'core/ticketscerrados.html')

def configuraciondecorreo(request):     
    return render(request, 'core/configuraciondecorreo.html')

def lista_tickets(request):     
    return render(request, 'core/listaticket.html')

def lista_tickets(request):     
    return render(request, 'core/editarticket.html') 

def lista_usuarios(request):     
    return render(request, 'core/lista_usuarios.html')

def editaruser(request):     
    return render(request, 'core/editaruser.html')

def editaruser(request):     
    return render(request, 'core/agregaruser.html')

def editaruser(request):     
    return render(request, 'core/eliminaruser.html')

@login_required
def products(request):
    return render(request, 'core/products.html')

#parte del formulario 
def exit(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  # Cambia 'home' por la URL de la página a la que deseas redirigir al usuario después del registro
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

#para devolver error si ingresa mal usuario y contraseña 
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationError(data=request.POST)
        if form.is_valid():
            # Lógica para el inicio de sesión exitoso
            return redirect('home')
    else:
        form = AuthenticationForm() # type: ignore

    return render(request, 'login.html', {'form': form})
#esta parte es la logica para que guarde datos en la bd de django
from django.shortcuts import render, redirect
from .forms import TicketForm

def creaciondeticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige a la página de inicio o donde desees después de guardar el ticket
    else:
        form = TicketForm()
    return render(request, 'core/creaciondeticket.html', {'form': form})


from .models import Ticket

def alltickets(request):
    tickets = Ticket.objects.all()
    return render(request, 'core/alltickets.html', {'tickets': tickets})

# logica para cerrar el Ticket-------------------------------------------------------------------------------------------------------

from django.shortcuts import get_object_or_404, redirect
from .models import Ticket

def cerrar_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.closed = True
    ticket.save()
    return redirect('home')

def all_closed_tickets(request):
    closed_tickets = Ticket.objects.filter(closed=True)
    return render(request, 'ticketscerrados.html', {'closed_tickets': closed_tickets})

#logica de la vista para procesar los correos
from django.shortcuts import render, redirect
from .logicadecorreo import obtener_correos
import threading

def configurar_correo(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        pop_server = request.POST.get('pop_server')
        port = int(request.POST.get('port'))
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Crear un hilo para ejecutar la función de obtener correos
        correo_thread = threading.Thread(target=obtener_correos, args=(pop_server, port, username, password))
        correo_thread.start()

        # Redirigir al usuario a la página de inicio después de iniciar el hilo
        return redirect('products')

    # Renderizar el formulario HTML
    return render(request, 'configuracion_correo.html')

#termina la logica de recepcion de correos -------------------------------------------------------------------------------------------

#logica para server smtp

def configure_smtp(request):
    return render(request, 'core/configure_smtp.html')

def enviar_correo1(request):
    return render(request, 'core/enviar_correo1.html')

from django.shortcuts import render
from django.http import HttpResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import ConfiguracionCorreo


def enviar_correo(request):
    if request.method == 'POST':
        smtp_host = request.POST.get('email_host')
        smtp_port = int(request.POST.get('email_port'))
        smtp_user = request.POST.get('email_host_user')
        smtp_password = request.POST.get('email_host_password')
        destinatario = request.POST.get('destinatario')
        asunto = 'FixFast te da la Bienvenida'
        cuerpo = 'Servidor STMP configurado correctamente'

                # Guardar configuración de correo en la base de datos
        configuracion, created = ConfiguracionCorreo.objects.get_or_create(
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_password=smtp_password
        )
        configuracion.smtp_password = smtp_password  # Actualizamos la contraseña
        configuracion.save()

        # Crear el mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = smtp_user
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        try:
            # Conectar al servidor SMTP
            with smtplib.SMTP(smtp_host, smtp_port) as servidor:
                servidor.starttls()  # Iniciar TLS para seguridad
                servidor.login(smtp_user, smtp_password)  # Iniciar sesión en el servidor
                servidor.sendmail(smtp_user, destinatario, mensaje.as_string())  # Enviar correo
            
            return HttpResponse("Correo enviado exitosamente.")
        except Exception as e:
            return HttpResponse(f"Error al enviar el correo: {e}")
            

    return render(request, 'enviar_correo.html')

#aqui termina la logica para el servidor smtp

#Notificaciones con smtp 
def notificaciones(request):
    return render(request, 'core/notificaciones.html')


#perfil de usuario
def perfildeusuario(request):
    return render(request, 'core/perfildeusuario.html')


#logica de francisco

def listatickets(request):
    tickets = Ticket.objects.all()  # Obtén todos los objetos de la tabla ticket
    return render(request, 'core/listaticket.html', {'tickets': tickets})
#editar tickets
from django.shortcuts import get_object_or_404, redirect
from .models import Ticket

def editarticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        ticket.id = request.POST['id']
        ticket.title = request.POST['title']
        ticket.description = request.POST['description']
        ticket.save()
        return redirect('listatickets')
    return render(request, 'editarticket.html', {'ticket': Ticket})

# core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Ticket  # Asegúrate de importar tu modelo

def eliminarticket(request, ticket_id):
    # Obtener el producto o devolver un 404 si no existe
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Eliminar el producto
    ticket.delete()

    # Enviar un mensaje de éxito (opcional)
    messages.success(request, f'El ticket "{ticket.title}" ha sido eliminado con éxito.')

    # Redirigir a la lista de productos
    return redirect('listatickets')  # Asegúrate de que este nombre coincida con tu URL para la lista de productos



#-----------------------
#-------------------

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User

def lista_usuarios(request):
    usuarios = User.objects.all()  # Captura todos los usuarios de la base de datos
    return render(request, 'core/lista_usuarios.html', {'usuarios': usuarios})


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from .forms import User


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
 # Asegúrate de importar tu modelo

def eliminaruser(request, user_id):
    # Obtener el producto o devolver un 404 si no existe
    usuarios = get_object_or_404(User, id=user_id)

    # Eliminar el producto
    usuarios.delete()

    # Enviar un mensaje de éxito (opcional)
    messages.success(request, f'El usuario "{usuarios.username}" ha sido eliminado con éxito.')

    # Redirigir a la lista de productos
    return redirect('listauser')  # Asegúrate de que este nombre coincida con tu URL para la lista de productos



def editaruser(request, user_id):
    usuarios = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        usuarios.username = request.POST['username']
        usuarios.last_name = request.POST['last_name']
        usuarios.email = request.POST['email']
        usuarios.save()
        return redirect('listauser')
    return render(request, 'editaruser.html', {'usuarios': usuarios})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def agregaruser(request, user_id):
    usuarios = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        usuarios.username = request.POST['username']
        usuarios.last_name = request.POST['last_name']
        usuarios.email = request.POST['email']
        usuarios.save()
        return redirect('listauser')
    return render(request, 'agregaruser.html', {'usuarios': usuarios})

#parte logica para los reportes

def reportes(request):
    return render(request, 'core/reportes.html')

import csv
from django.http import HttpResponse
from core.models import Ticket  # Asegúrate de que este sea tu modelo

def exportar_csv(request):
    # Crear la respuesta con tipo de contenido CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tickets.csv"'

    # Crear el escritor CSV
    writer = csv.writer(response)
    writer.writerow(['ID', 'Título', 'Descripción', 'Prioridad', 'Asignado', 'Categoría', 'Cerrado'])

    # Obtener todos los tickets y escribir las filas
    tickets = Ticket.objects.all().values_list('id', 'title', 'description', 'priority', 'asignar', 'categorias', 'closed')
    for ticket in tickets:
        writer.writerow(ticket)

    return response

import openpyxl
from django.http import HttpResponse
from core.models import Ticket

def exportar_excel(request):
    # Crear un archivo Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Tickets'

    # Agregar los encabezados
    ws.append(['ID', 'Título', 'Descripción', 'Prioridad', 'Asignado', 'Categoría', 'Cerrado'])

    # Obtener todos los tickets y escribir las filas
    tickets = Ticket.objects.all().values_list('id', 'title', 'description', 'priority', 'asignar', 'categorias', 'closed')
    for ticket in tickets:
        ws.append(ticket)

    # Preparar la respuesta HTTP para descargar el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="tickets.xlsx"'
    
    wb.save(response)
    return response

