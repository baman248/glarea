from django.db.models import fields
from django.forms import ModelForm
from store import models
from django import forms

class ModelFormCustom(ModelForm):
    def __init__(self, *args, creator=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.creator = creator

    def save(self, *args, **kwargs):
        self.instance.created_by = self.creator
        return super().save(*args, **kwargs)

class OrderForm(ModelFormCustom):
    class Meta:
        model = models.Order
        fields = ['medicine','quantity','from_stock',
        'customer','shipping_mode','shipping_mode']

class CustomerForm(ModelFormCustom):
    class Meta:
        model = models.Customer
        fields = ['name','is_dr','phone_number1','phone_number2','phone_number3','email']

class MedicineForm(ModelFormCustom):
    class Meta:
        model = models.Medicine
        fields = ['name','code','price_peso',
        'price_usd','india_code','price_dr']

class MoneyTransactionFrom(ModelFormCustom):
    class Meta:
        model = models.MoneyTransaction
        fields = ['amount','remarks','customer']

class StockTransactionForm(ModelFormCustom):
    class Meta:
        model = models.StockTransaction
        fields = ['quantity','stock']

class StockForm(ModelFormCustom):
    class Meta:
        model = models.Stock
        fields = ['medicine','location','quantity','expiry_date']

class ShippingModeForm(ModelFormCustom):
    class Meta:
        model = models.ShippingMode
        fields = ['name']

class DeliveryDoneForm(forms.Form):
    delivery_date = forms.DateField()
    
class PaymentDoneForm(forms.Form):
    payment_date = forms.DateField()
    bank = forms.CharField(max_length=200)


