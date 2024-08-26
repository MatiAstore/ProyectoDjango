from django.shortcuts import render
from django.http import HttpResponse
from .models import Cart, CartProduct
from products.models import Product
from .funciones import funcionCarrito
from django.shortcuts import redirect, get_object_or_404

def my_view(request):
    # Devolver una respuesta de texto simple
    return HttpResponse("Hola, este es un texto simple.")


def cart(request): 
    cart = funcionCarrito(request)
    return render(request, 'carts/cart.html', {
        "cart": cart 
    })

# def my_view(request):
#     return HttpResponse("Hola, como andas matias")

def add(request):
    cart = funcionCarrito(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    quantity = int(request.POST.get("quantity", 1))

    # cart.products.add(product, through_defaults={
    #     "quantity": quantity
    # })

    # Uso del Manager para crear o actualizar la cantidad del producto en el carrito
    product_cart = CartProduct.objects.crearActualizar(cart = cart, product = product, quantity = quantity)

    return render(request, "carts/add.html", {
        "product": product
    })

def remove(request): 
    cart = funcionCarrito(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))


    cart.products.remove(product) 

    return redirect('cart')