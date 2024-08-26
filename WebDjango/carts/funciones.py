from .models import Cart 

def funcionCarrito(request): 
    #print(dir(request.session))   
    #request.session.set_expiry(300) 5minutos
    #key = request.session.session_key
    #print(key)
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    cart_id = request.session.get('cart_id')

    cart = Cart.objects.filter(cart_id=cart_id).first() #si no se encuentra devuelve None
    if cart is None:
        cart = Cart.objects.create(user=user)
    
    if user and cart.user is None:
        cart.user = user
        cart.save()

    request.session["cart_id"] = cart.cart_id

    return cart 

def deleteCart(request):
    request.session["card_id"] = None