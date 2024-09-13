from django.urls import path, include
from .views import home, products, exit, creaciondeticket, alltickets, configuracion, ticketscerrados, configuraciondecorreo, configure_smtp, enviar_correo1
from .views import notificaciones, perfildeusuario, lista_usuarios, agregaruser, editaruser, eliminarticket, eliminaruser, editarticket, listatickets, reportes
from .views import exportar_csv, exportar_excel
from django.conf import settings
from django.conf.urls.static import static
#formulario 
from .views import register, products
#reestablecimiento de contraseña
from django.contrib.auth import views as auth_views
from . import views




#todas las urls a las que se puede acceder desde el proyecto
urlpatterns = [
   path('', home, name='home'),#nos devuelve al inicio de la pagina
   path('products/', products, name='products_login'), #nos redirecciona al dashboard
   path('products/', products, name='products'),
   path('logout/', exit, name='exit'),#nos permite salir de nuestra cuenta
   path('register/', register, name='register'),
   path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),#nos manda para resetear las password
   path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),#nos muestra el mensaje de listo 
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   path('creaciondeticket/', creaciondeticket, name='creaciondeticket'), #nos manda a la creacion de tickets
   path('alltickets/', alltickets, name='alltickets' ),#nos manda a la donde estan los tickets
   path('creaciondeticket/', creaciondeticket, name='creaciondeticketdirecto'),
   path('cerrar-ticket/<int:ticket_id>/', views.cerrar_ticket, name = 'cerrar_ticket'),
   path('configuracion/', configuracion, name='configuracion'),
   path('ticketscerrados/', ticketscerrados, name='ticketcerrados'),
   path('configuraciondecorreo/', configuraciondecorreo, name='configuraciondecorreo'),#pagina para configurar correo pop3
   path('configuracion-correo/', views.configurar_correo, name='configuracion_correo'),
   path('configure_smtp/', configure_smtp, name='configure_smtp'),
   path('enviar_correo1/', enviar_correo1, name='enviar_correo1' ),
   path('enviar-correo/', views.enviar_correo, name='enviar_correo'),
   path('notificaciones/', notificaciones, name='notificaciones'),
   path('perfil-usuario/', perfildeusuario, name='Perfil_usuario'),
   path('listaticket/', listatickets, name='listatickets'),
   path('editarticket/<int:ticket_id>/', editarticket, name='editarticket'),
   path('eliminarticket/<int:ticket_id>/', eliminarticket, name='eliminarticket'),
   path('eliminaruser/<int:user_id>/', eliminaruser, name='eliminaruser'),
   path('editaruser/<int:user_id>/', editaruser, name='editaruser'),
   path('agregaruser/<int:user_id>/', agregaruser, name='agregaruser'),
   path('listauser/', lista_usuarios, name='listauser'),
   path('configuraciondecorreo/', configuraciondecorreo, name='configuraciondecorreo'),#pagina para configurar correo pop3
   path('configuracion-correo/', views.configurar_correo, name='configuracion_correo'),
   path('reportes/', reportes, name='reportes'),
   path('exportar/csv/', exportar_csv, name='exportar_csv'),
   path('exportar/excel/', exportar_excel, name='exportar_excel'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    

