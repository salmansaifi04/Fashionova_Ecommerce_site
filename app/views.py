from django.shortcuts import render, redirect
from django.views import View
from .models import cart, Customer, Product, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required   # function based view
from django.utils.decorators import method_decorator # class based view


def home(request):
    bottom_wear = Product.objects.filter(category='BW')
    top_wear = Product.objects.filter(category='TW')
    mobiles = Product.objects.filter(category='M')
    return render(request, 'app/home.html', {'bottom_wear':bottom_wear, 'top_wear':top_wear, 'mobiles':mobiles})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
        item_already_in_cart = cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists
    return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart': item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    cart(user=user, product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        c = cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':c, 'totalamount':totalamount, 'amount':amount})
        else:
            return render(request, 'app/emptycart.html')

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': amount + shipping_amount,
        }
        
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount': amount + shipping_amount,
        }
        
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            
        data = {
            'amount':amount,
            'totalamount': amount + shipping_amount,
        }
        
        return JsonResponse(data)

@login_required
def buy_now(request):
    # user = request.user
    # product_id = request.GET.get('prod_id')
    # product = Product.objects.get(id = product_id)
    # cart(user=user, product=product).save()
    # return redirect('checkout')
    return render(request, 'app/buynow.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Samsung' or data == 'OnePlus' or data=='Apple':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=20000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=20000)
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def bottomwear(request, data=None):
    if data == None:
        bottomwear = Product.objects.filter(category='BW')
    elif data == 'Levis' or data == 'NEWPORT' or data=='Numero-Uno' or data == 'Allen-Solly' or data == 'Red-Tape':
        bottomwear = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt=500)
    elif data == 'above':
        bottomwear = Product.objects.filter(category='BW').filter(discounted_price__gte=500)
    return render(request, 'app/bottomwear.html', {'bottomwear':bottomwear})

def topwear(request, data=None):
    if data == None:
        topwear = Product.objects.filter(category='TW')
    elif data == 'Arrow' or data == 'Ajio' or data=='Blackberrys' or data == 'Gucci' or data == 'HRX':
        topwear = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwear = Product.objects.filter(category='TW').filter(discounted_price__lt=400)
    elif data == 'above':
        topwear = Product.objects.filter(category='TW').filter(discounted_price__gte=400)
    return render(request, 'app/topwear.html', {'topwear':topwear})

def customerregistration(request):
    if request.method == "POST":
        fm = CustomerRegistrationForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'successfully register !!! now you can login !!!')
        return render(request, 'app/customerregistration.html', {'form':fm})
    else:
        fm = CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html', {'form':fm})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'totalamount':totalamount, 'add':add, 'cart_items':cart_items})

@method_decorator(login_required, name='dispatch')    
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

@login_required
def orderdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    c = cart.objects.filter(user=user)
    for i in c:
        OrderPlaced(user=user, customer=customer, product=i.product, quantity=i.quantity).save()
        i.delete()
    return redirect("orders")

@login_required
def orders(request):
    order = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'orders':order})
