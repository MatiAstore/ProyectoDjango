from django.db import models
from django.contrib.auth.models import  AbstractUser 
from django.db.models.deletion import CASCADE

from orden.comun import OrdenStatus

#OnetoOneField() 

class User(AbstractUser):
    def get_full_name(self) -> str:
        return "{}, {}".format(self.first_name, self.last_name)

    @property 
    def direccion_envio(self):
        return self.direccionenvio_set.filter(default=True).first() #traemos la direccion por Default

    def has_direccion_envio(self):
        return self.direccion_envio is not None #retorna si el usuario tiene una direccion

    def ordenes_completadas(self):
        return self.orden_set.filter(status=OrdenStatus.COMPLETED).order_by("-id")


class Cliente(User): 
    class Meta:
        proxy = True

    def get_products(self):
        return []
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    biografia = models.TextField()
