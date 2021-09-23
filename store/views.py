from django.core.checks import messages
from django.shortcuts import redirect, render
from store import forms, models
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def index(request):
    return render(request,template_name="templates/index.html")

def orders(request):
    
    try:
        all_orders = models.Order.objects.order_by('date')
    except models.Order.DoesNotExist:
        all_orders = False


    return render(request, 'templates/orders.html', {'all_orders':all_orders})

def stocks(request):
    return render(request, template_name='templates/stocks.html')

def addStocks(request):
    if request.method == "POST":
        form = forms.StockTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            quantity = form.cleaned_data['quantity']
            medicine = form.cleaned_data['medicine']
            location = form.cleaned_data['location']
            if location == 'laspinas':
                medicine.las_pinas_stock += quantity
            else:
                medicine.monti_stock += quantity
            messages.info(str(quantity) + ' ' + str(medicine) + ' added')
            return redirect('store:add_stocks')


    all_medicines = models.Medicine.objects.all()
    return render(request, 'templates/add_stocks.html',{'all_medicines':all_medicines})

def medicines(request):
    try:
        all_medicines = models.Medicine.objects.all()
    except models.Medicine.DoesNotExist:
        all_medicines = False
    return render(request, 'templates/medicines.html',{'all_medicines':all_medicines})

def medicineDetails(request, pk):
    try:
        medicine = models.Medicine.objects.get(pk = pk)
    except models.Medicine.DoesNotExist:
        medicine = False
    return render(request, 'templates/medicine_details.html',{'medicine':medicine})

def addStocks(request):
    return render(request,template_name='templates/add_stocks.html')

def customers(request):
    all_customers = models.Customer.objects.all()
    return render(request, template_name='templates/customers.html',context={'all_customers':all_customers})

def customerDetails(request, pk):
    try:
        customer = models.Customer.objects.get(pk = pk)
        print("customer is ",customer)
    except models.Customer.DoesNotExist:
        print("I*******************************CustomerDoesNotExist")
        customer = False
    
    try:
        customer_orders = models.Order.objects.filter(customer= customer)
    except:
        customer_orders = False
    

    return render(request, template_name='templates/customer_details.html',context={'customer':customer, 'customer_orders':customer_orders})



def createMedicine(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.MedicineForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('store:index'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.MedicineForm()

    return render(request, 'templates/create_medicine.html',context={'form':form})
 
def addOrder(request):
        # if this is a POST request we need to process the form dat
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.OrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            medicine = models.Medicine.objects.get(pk=request.POST['medicine'])
            customer = models.Customer.objects.get(pk=request.POST['customer'])
            stock = form.changed_data.get('from_stock')
            quantity = form.cleaned_data.get('quantity')

            ## update stock
            stock.quantity -= quantity

            ## update customer account
            if customer.is_dr:
                customer.balance -= medicine.price_dr*quantity
            else:
                customer.balance -= medicine.price_peso*quantity
            customer.save()
            medicine.save()
            stock.save()
            return HttpResponseRedirect(reverse('store:index'))
    # if a GET (or any other method) we'll create a blank form
    all_medicines = models.Medicine.objects.all()
    all_shipping_modes = models.ShippingMode.objects.all()
    all_customers = models.Customer.objects.all()
    all_stocks = models.Stock.objects.all()

    medicine_dict = dict()
    for i in all_medicines:
        medicine_dict[i.name] = i.id

    shipping_modes_dict = dict()
    for i in all_shipping_modes:
        shipping_modes_dict[i.name] = i.id

    customers_dict = dict()
    for i in all_customers:
        customers_dict[i.name] = i.id

    stock_dict = dict()
    for i in all_stocks:
        stock_dict[i.location] = i.id
    
    context = {'all_medicines':medicine_dict,
               'all_customers':customers_dict,
               'all_shipping_modes':shipping_modes_dict,
               'all_stocks':stock_dict}

    return render(request, 'templates/add_order.html',context=context)

def orderDetails(request, pk):
    try:
        order = models.Order.objects.get(pk = pk)
    except models.Order.DoesNotExist:
        order = False

    if request.method == 'POST':
        if request.POST['form_type'] == 'delivery':
            order.delivery_date = request.POST['delivery_date']
            order.delivery_done = True
        else:
            order.payment_date = request.POST['payment_date']
            order.payment_done = True
        order.save()

    return render(request, template_name='templates/order_details.html',context={'order':order})

def createTransaction(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print("psot method")
        # create a form instance and populate it with data from the request:
        form = forms.MoneyTransactionFrom(request.POST)
        # check whether it's valid:
        print(request.POST)
        if form.is_valid():
            print("IIIIIIVAlid form")
            customer =form.cleaned_data.get('customer')
            amount = float(form.cleaned_data.get('amount'))
            customer.balance += amount
            customer.save()
            return HttpResponseRedirect(reverse('store:index'))
    # if a GET (or any other method) we'll create a blank form
    all_customers = models.Customer.objects.all()
    return render(request, 'templates/create_transaction.html',context={'all_customers':all_customers})

def createCustomer(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.CustomerForm(request.POST)
        # check whether it's valid:
        print(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('store:index'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.CustomerForm()

    return render(request, 'templates/create_customer.html',context={'form':form})

def createShippingMode(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.ShippingModeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('store:index'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.ShippingModeForm()

    return render(request, 'templates/create_shipping_mode.html',context={'form':form})

