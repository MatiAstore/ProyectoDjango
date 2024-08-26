from django.db import models
from django.utils.text import slugify 
from django.db.models.signals import pre_save 
import uuid 

class Product(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    price = models.DecimalField(max_digits=8,decimal_places=2, default=0.0)
    image = models.ImageField(upload_to= "products/", null = False, blank= False)
    created_at = models.DateTimeField(auto_now_add = True)
    slug = models.SlugField(max_length=200, null=False, blank=False, unique=True)

    #Funcion para slug automatico
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title 
    

#Funcion para slug automatico
def new_slug(sender, instance, *args, **kwargs): 
    #instance.slug = slugify(instance.title)
    if instance.title and not instance.slug: 
        slug_created = slugify(instance.title)

        while Product.objects.filter(slug=slug_created).exists():
            slug_created = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])  # Convertir el UUID a una cadena antes de hacer slicing
            )
        instance.slug = slug_created

#Conectar la señal pre_save a la clase Product 
pre_save.connect(new_slug, sender = Product)

