from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login as lg 
# from django.contrib.auth.models import User
from users.models import User
from django.contrib import messages 
from . forms import Registro
from products.models import Product
from django.http import HttpResponseRedirect

def index(request): 
    productos = Product.objects.all()
    return render(request, "index.html", {
        "mensaje": "Ingreso",
        "titulo": "Personas",
        "productos": productos})

def login(request): 
    if request.user.is_authenticated:
        return redirect ("index")

    if request.method == "POST": 
        username = request.POST.get('username') 
        password = request.POST.get('password')
        
        usuarios = authenticate(username=username, password=password)
        if usuarios: 
            lg(request,usuarios)
            messages.success(request, f"Bienvenido {usuarios.username}")
            
            if request.GET.get("next"): 
                return HttpResponseRedirect(request.GET["next"])
            
            return redirect("index")
        else:
            messages.error(request, "Datos incorrectos")

    return render(request, "users/login.html", {})

def salir(request):
    logout(request)
    messages.success(request, "Sesion cerrada")
    return redirect ("login")

def registro(request):
    if request.user.is_authenticated:
        return redirect ("index")

    form = Registro(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # username = form.cleaned_data.get("username")
        # email = form.cleaned_data.get("email")
        # password = form.cleaned_data.get("password")

        # usuario = User.objects.create_user(username, email, password) #crea usuario
        usuario = form.save()
        if usuario: 
            messages.success(request, f"Usuario registrado con exito")
            return redirect("login")
        else: 
            messages.error(request, "Usuario no creado")

    return render(request, "users/registro.html", {
        "form": form 
    })

