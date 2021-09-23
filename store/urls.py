from django.urls import path

from . import views
app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('stocks/', views.stocks, name='stocks'),
    path('orders/', views.orders, name='orders'),
    path('medicines/',views.medicines, name='medicines'),
    path('customers/', views.customers, name='customers'),
    path('add_order/', views.addOrder, name='add_order' ),
    path('create_shipping_mode/', views.createShippingMode, name='create_shipping_mode'),
    path('create_customer/',views.createCustomer, name='create_customer'),
    path('create_transaction/', views.createTransaction, name='create_transaction'),
    path('customer_details/<int:pk>',views.customerDetails, name='customer_details'),
    path('create_medicine/', views.createMedicine, name='create_medicine'),
    path('add_stocks/', views.addStocks, name='add_stocks'),
    path('order_details/<int:pk>',views.orderDetails, name='order_details'),
    path('medicine_details/<int:pk>', views.medicineDetails, name='medicine_details')
]