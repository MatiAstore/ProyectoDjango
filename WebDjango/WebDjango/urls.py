"""
URL configuration for WebDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from products.views import ProductListView
from . import views 
from django.conf.urls.static import static 
from django.conf import settings 

urlpatterns = [
    path('', ProductListView.as_view(), name="index"),
    path('usuarios/login', views.login, name="login"),
    path('usuarios/registro', views.registro, name="registro"),
    path('usuarios/salir', views.salir, name="salir"),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('admin/', admin.site.urls),
    path('productos/', include("products.urls")),
    path('carrito/', include("carts.urls")),
    path("orden/", include("orden.urls")),
    path("direcciones/", include("DirEnvio.urls")),
    path("codigopromo/", include("promo_codigo.urls")),
    path("pagos/", include("MetodoPago.urls")),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 

