from django.db.models.fields.related import ForeignKey
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class ShippingMode(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.name)

class Customer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    balance = models.FloatField(default=0)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number1 = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    phone_number2 = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    phone_number3 = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    is_dr = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return '{}'.format(self.name)

class Medicine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=200)
    price_peso = models.FloatField()
    price_usd = models.FloatField(blank=True)
    india_code = models.FloatField()
    price_dr = models.FloatField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return '{}'.format(self.name)

class Stock(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT )
    location = models.CharField(max_length=100)
    quantity = models.IntegerField()
    expiry_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return '{} at {}'.format(self.medicine, self.location)

class Order(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    shipping_mode = models.ForeignKey(ShippingMode, on_delete=models.RESTRICT)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_done = models.BooleanField(default=False)
    payment_done = models.BooleanField(default=False)
    payment_date = models.DateField(blank=True,null=True)
    bank = models.CharField(max_length=200, blank=True)
    from_stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return '{} quant. of {}'.format(self.quantity,self.medicine)


class MoneyTransaction(models.Model):
    amount = models.FloatField()
    remarks = models.TextField(max_length=2000)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return '{}'.format(self.amount)

class StockTransaction(models.Model):
    quantity = models.IntegerField()
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return '{} of {}'.format(self.quantity, self.stock)

class StockCreateTransaction(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT )
    location = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return '{} at {}'.format(self.medicine, self.location)



# Create your models here.
