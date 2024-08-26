from django.urls import path 
from .import views

urlpatterns = [
    path('',views.EnvioDirecciones.as_view(), name="direccion_envio"),
    path('nueva', views.formularioDir , name="formulariodir"),
    path('editar/<int:pk>', views.UpdateDireccion.as_view(), name="update"),
    path('eliminar/<int:pk>', views.DeleteDireccion.as_view(), name="delete"),
    path('default/<int:pk>', views.FuncDefault, name="default"),
]