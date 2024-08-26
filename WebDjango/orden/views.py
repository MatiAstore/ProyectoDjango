from django.contrib import messages 
from django.shortcuts import get_object_or_404, redirect, render
from .models import Orden
from carts.funciones import deleteCart, funcionCarrito
from .utils import deleteOrden, funcionOrden, breadcrumb
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from DirEnvio.models import DireccionEnvio
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorador import validar_cart_and_orden

class OrdenViews(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "orden/ordenes.html"

    def get_queryset(self):
        return self.request.user.ordenes_completadas()

@login_required(login_url="login")
@validar_cart_and_orden
def orden(request, cart, orden):
    if orden is None: 
        return HttpResponse("Orden invalida")

    return render(request, 'orden/orden.html', {
        "cart": cart, 
        "orden": orden, 
        "breadcrumb": breadcrumb()
    })

@login_required(login_url="index")
@validar_cart_and_orden
def direccion(request, cart, orden):
    direccion_envio = orden.get_or_set_direccion_envio()
    contDireccion = request.user.direccionenvio_set.count() > 1 

    return render(request, 'orden/direccion.html', {
        "cart":cart, 
        "orden":orden,
        "direccion_envio": direccion_envio,
        "contDireccion": contDireccion,
        "breadcrumb": breadcrumb(address=True)
    })


@login_required(login_url="index")
def select_direccion(request):
    direccion_envios = request.user.direccionenvio_set.all()
    return render(request, "orden/select_direccion.html", {
        "breadcrumb": breadcrumb(address=True),
        "direccion_envios": direccion_envios,    
    })

@login_required(login_url="index")
@validar_cart_and_orden
def check_direccion(request, pk, cart, orden):
    direccion_envio = get_object_or_404(DireccionEnvio, pk=pk)

    if request.user.id != direccion_envio.user_id:
        return redirect("index")
    
    orden.update_direccion_envio(direccion_envio)

    return redirect("direccion")


@login_required(login_url="login")
@validar_cart_and_orden
def confirmacion(request, cart, orden):
    direccion_envio = orden.direccion_envio
    if direccion_envio is None:
        return redirect("direccion")
    
    return render (request, "orden/confirmacion.html", {
        "cart":cart,
        "orden":orden,
        "direccion_envio" : direccion_envio, 
        "breadcrumb": breadcrumb(address= True, confirmation=True)
    })

@login_required(login_url="login")
@validar_cart_and_orden
def cancelar_orden(request, cart, orden):
    if request.user.id != orden.user_id: 
        return redirect ("index")
    
    orden.cancelar()
    deleteCart(request)
    deleteOrden(request)

    print("Despues de eliminar el carrito:", request.session.get("cart_id"))

    messages.error(request, "Orden eliminada correctamente")
    return redirect ("index")

@login_required(login_url="login")
@validar_cart_and_orden
def completado(request, cart, orden):
    if request.user.id != orden.user_id: 
        return redirect ("index")   
    
    orden.completado()
    deleteCart(request)
    deleteOrden(request)
    messages.success(request, "Compra completada, pronto llegara a destino")
    return redirect("index")

