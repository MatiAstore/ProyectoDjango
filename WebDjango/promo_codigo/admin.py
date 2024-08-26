from django.contrib import admin
from .models import PromoCodigo

class CodigoPromoAdmin(admin.ModelAdmin):
    exclude = ["codigo"]

admin.site.register(PromoCodigo, CodigoPromoAdmin)