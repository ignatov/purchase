__author__ = 'ignatov'

from purchase.nomenclature.models import SupplierType, Supplier, Product, ProductType
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    fields = ['name', 'gost', 'price', 'type', 'suppliers']
    list_display = ['name', 'gost', 'price']
    search_fields = ['name', 'gost']

admin.site.register(Product, ProductAdmin)
admin.site.register([SupplierType, Supplier, ProductType])
