from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    fields = ("title", "description", "price", "image") #campos que se mostraran en el formulario
    list_display = ("__str__", "slug", "created_at") #campos que se mostraran en la lista de productos

admin.site.register(Product, ProductAdmin)