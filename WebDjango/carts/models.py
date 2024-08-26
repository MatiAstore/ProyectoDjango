from django.db import models
from users.models import User
from products.models import Product 
from django.db.models.signals import pre_save, m2m_changed, post_save 
import decimal 
import uuid
from orden.comun import OrdenStatus

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartProduct")
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    FEE = 0.01

    def __str__(self):
        return self.cart_id 

    def update_total(self):
        self.update_subtotal()
        self.calculate_total()
        
        if self.orden:
            self.orden.update_total() 

    def update_subtotal(self):
        self.subtotal = sum([
           i.quantity * i.product.price for i in self.product_related()
        ])
        self.save()

    def calculate_total(self): 
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE))
        self.save()

    def product_related(self):
        return self.cartproduct_set.select_related("product")
    
    @property 
    def orden(self):
        return self.orden_set.filter(status=OrdenStatus.CREATED).first()

class CartProductManager(models.Manager): 

    def crearActualizar(self, cart, product, quantity=1):
        # Intentar obtener o crear una instancia de CartProduct
        object, created = self.get_or_create(cart=cart, product=product)

        if not created: # Si ya existía, sumar la cantidad 
            quantity = object.quantity + quantity

          # Llamar al método update_quantity para actualizar la cantidad
        object.update_quantity(quantity)
        return object 

class CartProduct(models.Model): 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CartProductManager()

    def update_quantity(self, quantity=1):
        self.quantity = quantity 
        self.save()

def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

def update_totals(sender, instance, action, *args, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.update_total()

def postActualizar(sender, instance, *args, **kwargs):
    instance.cart.update_total()

post_save.connect(postActualizar, sender = CartProduct)
pre_save.connect(set_cart_id, sender=Cart)
m2m_changed.connect(update_totals, sender=Cart.products.through)
