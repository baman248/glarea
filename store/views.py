from django.shortcuts import redirect, render
from store import forms, models
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required()
def index(request):
    messages.success(request, 'welcome to contact.')
    return render(request,template_name="templates/index.html")

@login_required()
def orders(request):
    
    try:
        all_orders = models.Order.objects.order_by('-created_on')
    except models.Order.DoesNotExist:
        all_orders = False


    return render(request, 'templates/orders.html', {'all_orders':all_orders})

@login_required()
def stocks(request):
    all_stock_transactions = models.StockTransaction.objects.order_by('-created_on')
    return render(request, 'templates/stocks.html', {'all_stock_transactions':all_stock_transactions})

@login_required()
def addStocks(request):
    if request.method == "POST":
        form = forms.StockForm(request.POST, creator=request.user)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            medicine = form.cleaned_data.get('medicine')
            location = form.cleaned_data.get('location')
            quantity = form.cleaned_data.get('quantity')
            stock_create_transaction = models.StockCreateTransaction(medicine = medicine,location = location, quantity = quantity, created_by=request.user)
            stock_create_transaction.save()
            form.save()
            messages.success(request, "Stock added successfully")
            return redirect('store:stocks')

    all_medicine = models.Medicine.objects.all()
    return render(request, 'templates/add_stocks.html', {'all_medicine':all_medicine})

@login_required()
def addStockHistory(request):
    all_stock_transactions = models.StockCreateTransaction.objects.order_by('-created_on')
    return render(request, 'templates/add_stock_history.html',{'all_stock_transactions':all_stock_transactions} )

@login_required()
def updateStocks(request):
    if request.method == "POST":
        form = forms.StockTransactionForm(request.POST, creator=request.user)
        if form.is_valid():
            form.save()
            quantity = form.cleaned_data['quantity']
            stock = form.cleaned_data['stock']
            stock.quantity += quantity
            stock.save()
            messages.success(request, "Stock updated successfully")
            return redirect('store:stocks')

    all_stocks = models.Stock.objects.all()
    print(all_stocks)
    
    return render(request, 'templates/update_stocks.html',{'all_stocks':all_stocks})

@login_required()
def medicines(request):
    try:
        all_medicines = models.Medicine.objects.order_by('-created_on')
    except models.Medicine.DoesNotExist:
        all_medicines = False
    return render(request, 'templates/medicines.html',{'all_medicines':all_medicines})

@login_required()
def medicineDetails(request, pk):
    try:
        medicine = models.Medicine.objects.get(pk = pk)
    except models.Medicine.DoesNotExist:
        medicine = False
    return render(request, 'templates/medicine_details.html',{'medicine':medicine})

@login_required()
def customers(request):
    all_customers = models.Customer.objects.order_by('-created_on')
    return render(request, template_name='templates/customers.html',context={'all_customers':all_customers})

@login_required()
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


@login_required()
def createMedicine(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.MedicineForm(request.POST,  creator=request.user)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, "{} is created successfully".format(name))
            return HttpResponseRedirect(reverse('store:medicines'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.MedicineForm()

    return render(request, 'templates/create_medicine.html',context={'form':form})
 
@login_required()
def addOrder(request):
        # if this is a POST request we need to process the form dat
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.OrderForm(request.POST, creator=request.user)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            medicine = models.Medicine.objects.get(pk=request.POST['medicine'])
            customer = models.Customer.objects.get(pk=request.POST['customer'])
            stock = form.cleaned_data.get('from_stock')
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
            return HttpResponseRedirect(reverse('store:orders'))
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

@login_required()
def orderDetails(request, pk):
    payment_form = None
    delivery_form = None
    try:
        order = models.Order.objects.get(pk = pk)
        if not order.payment_done:
            payment_form = forms.PaymentDoneForm()
        if not order.delivery_done:
            delivery_form = forms.DeliveryDoneForm()
        if request.method == 'POST':
            print("it's a post reqeust")
            if request.POST['form_type'] == 'delivery' and not order.delivery_done:
                delivery_form = forms.DeliveryDoneForm(request.POST)
                print(request.POST)
                print(delivery_form.is_valid())
                if delivery_form.is_valid():
                    order.delivery_date = delivery_form.cleaned_data.get('delivery_date')
                    order.delivery_done = True
                    order.save()
                    messages.success(request, "Order updated successfully")

            if request.POST['form_type'] == 'payment' and not order.payment_done:
                payment_form = forms.PaymentDoneForm(request.POST)
                print(payment_form.is_valid())
                if payment_form.is_valid():
                    order.payment_date = payment_form.cleaned_data.get('payment_date')
                    order.payment_done = True
                    order.bank = payment_form.cleaned_data.get('bank')
                    order.save()
                    messages.success(request, "Order updated successfully")

    except models.Order.DoesNotExist:
        order = False
    
    context = {
        'payment_form':payment_form,
        'delivery_form':delivery_form,
        'order':order
    }
    
    return render(request, template_name='templates/order_details.html',context=context)

@login_required()
def createTransaction(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print("psot method")
        # create a form instance and populate it with data from the request:
        form = forms.MoneyTransactionFrom(request.POST, creator=request.user)
        # check whether it's valid:
        print(request.POST)
        if form.is_valid():
            form.save()
            print("IIIIIIVAlid form")
            customer =form.cleaned_data.get('customer')
            amount = float(form.cleaned_data.get('amount'))
            customer.balance += amount
            customer.save()
            messages.success(request, "Transaction of amount {}, is created successfully".format(amount))
            return HttpResponseRedirect(reverse('store:index'))
    # if a GET (or any other method) we'll create a blank form
    all_customers = models.Customer.objects.all()
    return render(request, 'templates/create_transaction.html',context={'all_customers':all_customers})

@login_required()
def moneyTransactionHistory(request):
    all_money_transactions = models.MoneyTransaction.objects.all()
    return render(request, 'templates/money_transaction_history.html',{'all_money_transactions':all_money_transactions})

@login_required()
def createCustomer(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.CustomerForm(request.POST, creator=request.user)
        # check whether it's valid:
        print(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, "{} is created successfully".format(name))
            return HttpResponseRedirect(reverse('store:customers'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.CustomerForm()

    return render(request, 'templates/create_customer.html',context={'form':form})

@login_required()
def createShippingMode(request):
        # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.ShippingModeForm(request.POST, creator=request.user)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('store:index'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.ShippingModeForm()

    return render(request, 'templates/create_shipping_mode.html',context={'form':form})

