from django.contrib import admin
from store import models
admin.site.register(models.ShippingMode)
admin.site.register(models.Order)
admin.site.register(models.Customer)
admin.site.register(models.MoneyTransaction)
admin.site.register(models.Medicine)

# Register your models here.
