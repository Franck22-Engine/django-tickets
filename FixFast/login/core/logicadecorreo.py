import poplib
import threading
import time
from email import parser
from django.conf import settings
from core.models import Ticket, ConfiguracionCorreo
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def enviar_notificacion_ticket(ticket):
    # Obtener la configuración de correo desde la base de datos
    configuracion = ConfiguracionCorreo.objects.first()
    if not configuracion:
        print("No se ha configurado el servidor de correo.")
        return

    smtp_host = configuracion.smtp_host
    smtp_port = configuracion.smtp_port
    smtp_user = configuracion.smtp_user
    smtp_password = configuracion.smtp_password

    destinatario = 'steed.galvez@gmail.com'  # Cambia esto por la dirección de correo de destino
    asunto = f'Nuevo Ticket Creado: {ticket.title}'
    cuerpo = f"""
    Se ha creado un nuevo ticket:

    Título: {ticket.title}
    Descripción: {ticket.description}

    Prioridad: {ticket.priority}
    Asignado a: {ticket.asignar}
    Categoría: {ticket.categorias}
    """

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

        print("Correo de notificación enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo de notificación: {e}")

def process_email(msg_content):
    email_message = parser.Parser().parsestr(msg_content)
    
    # Extraer el asunto y el cuerpo
    subject = email_message['subject']
    body = email_message.get_payload()
    
    # Crear un nuevo ticket con el contenido del correo
    ticket = Ticket.objects.create(
        title=subject,
        description=body,
    )
    
    print("Nuevo ticket creado a partir del correo:")
    print(f"Título: {subject}")
    print(f"Descripción: {body}")
    
    # Enviar notificación de nuevo ticket
    enviar_notificacion_ticket(ticket)

    print("Nuevo correo electrónico recibido:")
    print(msg_content)

def obtener_correos(pop_server, port, username, password):
    while True:
        try:
            # Conectarse al servidor POP3
            mail = poplib.POP3(pop_server, port)
            mail.user(username)
            mail.pass_(password)

            # Obtener el número total de mensajes en la bandeja de entrada
            num_messages = len(mail.list()[1])
            print(f'Número total de mensajes en la bandeja de entrada: {num_messages}')

            # Leer los nuevos mensajes uno por uno
            for i in range(1, num_messages + 1):
                # Obtener el contenido del mensaje
                response, msg_bytes, octets = mail.retr(i)
                msg_content = b'\n'.join(msg_bytes).decode('utf-8')

                # Procesar el correo electrónico
                process_email(msg_content)

                # Marcar el mensaje como eliminado (opcional)
                mail.dele(i)

            # Cerrar la conexión
            mail.quit()

        except Exception as e:
            print(f'Error al procesar correos electrónicos: {e}')

        # Esperar un tiempo antes de la siguiente verificación (por ejemplo, 30 segundos)
        time.sleep(30)
