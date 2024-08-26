from django.db import models
import string 
import random
from django.db.models.signals import pre_save
from django.utils import timezone 

class PromoCodigoManager(models.Manager):

    def get_validar(self, code):
        actual = timezone.now()
        
        return self.filter(codigo = code).filter(used=False).filter(fecha_inicio__lte=actual).filter(fecha_final__gte=actual).first()

class PromoCodigo(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento = models.FloatField(default=0.0)
    fecha_inicio = models.DateTimeField()
    fecha_final = models.DateTimeField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PromoCodigoManager()

    def __str__(self):
        return self.codigo 
    
    def codigo_used(self):
        self.used = True 
        self.save()

def set_codigo(sender, instance, *args, **kwargs):
    if instance.codigo:
        return 
    
    coders = string.ascii_uppercase + string.digits 
    instance.codigo = "".join(random.choice(coders) for _ in range(5))


pre_save.connect(set_codigo, sender=PromoCodigo)