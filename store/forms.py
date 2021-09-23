from django.forms import ModelForm
from store import models

class OrderForm(ModelForm):
    class Meta:
        model = models.Order
        fields = ['medicine','quantity','from_stock',
        'customer','shipping_mode','shipping_mode']

class CustomerForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = ['name','is_dr','phone_number1','phone_number2','phone_number3','email']

class MedicineForm(ModelForm):
    class Meta:
        model = models.Medicine
        fields = ['name','code','price_peso',
        'price_usd','india_code','price_dr']

class MoneyTransactionFrom(ModelForm):
    class Meta:
        model = models.MoneyTransaction
        fields = ['amount','remarks','customer']

class StockTransactionForm(ModelForm):
    class Meta:
        model = models.StockTransaction
        fields = ['quantity','stock']
        
class ShippingModeForm(ModelForm):
    class Meta:
        model = models.ShippingMode
        fields = ['name']


