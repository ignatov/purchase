from decimal import Decimal
from django.db.models import Model, CharField, ForeignKey, ManyToManyField, EmailField, DecimalField

class SupplierType(Model):
    name = CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Supplier(Model):
    name = CharField(max_length=255, unique=True)
    site = CharField(max_length=200, blank=True)
    email = EmailField(max_length=100, blank=True)
    type = ForeignKey(SupplierType, blank=False)

    def __unicode__(self):
        return "%s %s" % (self.name, self.email)

class ProductType(Model):
    name = CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Product(Model):
    name = CharField(max_length=255, unique=True)
    type = ForeignKey(ProductType, default=None, null=True, blank=True)
    gost = CharField(max_length=200, blank=True)
    price = DecimalField(name='Price', max_digits=10, decimal_places=2, blank=True, null=True)
    suppliers = ManyToManyField('Supplier', blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.name, self.gost)
