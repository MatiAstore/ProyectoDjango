from django.db import models
from users.models import User
from carts.models import Cart 
from enum import Enum
import uuid 
from django.db.models.signals import pre_save
from DirEnvio.models import DireccionEnvio
from .comun import OrdenStatus, choices
from promo_codigo.models import PromoCodigo
import decimal 

class Orden(models.Model):
    orden_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion_envio = models.ForeignKey(DireccionEnvio, null=True, blank=True, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=40, choices=choices, default=OrdenStatus.CREATED)
    envio_total = models.DecimalField(default=10, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0, max_digits = 9, decimal_places =2)
    created_at = models.DateTimeField(auto_now_add=True)
    promo_codigo = models.OneToOneField(PromoCodigo, null = True, blank = True, on_delete=models.CASCADE)

    def __str__(self):
        return self.orden_id
    
    def aplicarCodigo(self, promo_codigo):
        if self.promo_codigo is None:
            self.promo_codigo = promo_codigo
            self.save()

            self.update_total() 
            promo_codigo.codigo_used()

    def get_descuento(self):
        if self.promo_codigo: 
            return self.promo_codigo.descuento 
        
        return 0 
    
    def get_total(self): 
        return self.cart.total + self.envio_total - decimal.Decimal(self.get_descuento())

    def update_total(self):
        self.total = self.get_total()
        self.save()

    def get_or_set_direccion_envio(self):
        if self.direccion_envio: #comprueba si la orden tiene una dir
            return self.direccion_envio
        
        direccion_envio = self.user.direccion_envio #sino tiene, toma la principal del usuario
        if direccion_envio:
            self.direccion_envio = direccion_envio 
            self.save()
        return direccion_envio
    
    def update_direccion_envio(self, direccion_envio):
        self.direccion_envio = direccion_envio
        self.save()

    def cancelar(self):
        self.status = OrdenStatus.CANCELED
        self.save()

    def completado(self): 
        self.status = OrdenStatus.COMPLETED
        self.save()


def enviarOrden(sender, instance, *args, **kwargs):
    if not instance.orden_id:
        instance.orden_id = str(uuid.uuid4())

def enviarTotal(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()

pre_save.connect(enviarTotal, sender=Orden)
pre_save.connect(enviarOrden, sender=Orden)
