from django.contrib import admin
from store import models
admin.site.register(models.ShippingMode)
admin.site.register(models.Order)
admin.site.register(models.Customer)
admin.site.register(models.MoneyTransaction)
admin.site.register(models.Medicine)
admin.site.register(models.Stock)
admin.site.register(models.StockTransaction)
admin.site.register(models.StockCreateTransaction)

# Register your models here.
