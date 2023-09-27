from django.contrib.auth import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
import json
import datetime
from .models import *

# Create your views here.

def main_page(request):
    
    # Login User
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.success(request, ("There was an error logging in. Try again..."))
            return redirect('main')
    # else:
    #     return render(request, 'main')


    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items
    else:
        items = []
        cart = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = cart['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cart': cart, 'items': items, 'cartitems': cartItems}
    return render(request, 'store/index.html', context)


def login_user(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request, ("You are "))
    return redirect('main')


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = authenticate(username=username, password=password)
            login(request, user)
            Customer.objects.create(user=user, name=last_name+' '+first_name, email=email)
            messages.success(request, ("Registration successful!"))
            return redirect('main')
    else:
        form = RegisterUserForm()

    context = {'form': form}
    return render(request, 'store/register.html', context)


def store(request):

    # Login User
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.success(request, ("There was an error logging in. Try again..."))
            return redirect('main')
    # else:
    #     return render(request, 'main')


    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items
    else:
        items = []
        order = {'order_cart_items':0, 'order_cart_total':0}
        cartItems = {'get_cart_items': 0}

    products = Product.objects.all()
    categories = Category.objects.all()

    context = {'products': products, 'cart': cart, 'categories': categories, 'items': items, 'cartItems': cartItems}
    return render(request, 'store/products.html', context)

def product_detail(request):
    context = {}
    return render(request, 'store/product_detail.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items
    else:
        items = []
        cart = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = cart['get_cart_items']

    context = {'items': items, 'cart': cart, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def blog(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items
    else:
        items = []
        cart = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = cart['get_cart_items']

    context = {'items': items, 'cart': cart, 'cartItems': cartItems}
    return render(request, 'store/blog.html', context)


def about(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items
    else:
        items = []
        cart = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = cart['get_cart_items']

    context = {'items': items, 'cart': cart, 'cartItems': cartItems}
    return render(request, 'store/about.html', context)


def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items
    else:
        items = []
        cart = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = cart['get_cart_items']

    context = {'items': items, 'cart': cart, 'cartItems': cartItems}
    return render(request, 'store/contact.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
    else:
        items = []
        cart = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'cart': cart}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('prodcutId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    cart, created = Cart.objects.get_or_create(customer=customer)
    cartItem, created =CartItem.objects.get_or_create(cart=cart, product=product)

    if action == 'add':
        cartItem.quantity = (cartItem.quantity + 1)
    elif action == 'remove':
        cartItem.quantity = (cartItem.quantity - 1)

    cartItem.save()

    if cartItem.quantity <= 0:
        cartItem.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        
        items = cart.cartitem_set.all()

        order = Order.objects.create(customer=customer)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        order.price_total = cart.get_cart_total
        order.product_total = cart.get_cart_items
        order.complete = False
        order.save()


        for item in items:
            OrderItem.objects.get_or_create(order=order, product=item.product, quantity=item.quantity)

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            district=data['shipping']['district'],
            zipcode=data['shipping']['zipcode'],
        )
    else:
        items = []
        cart = {'get_cart_total': 0, 'get_cart_items': 0}

    return JsonResponse('Payment complete', safe=False)


def search_category(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
    else:
        items = []
        cart = {'get_cart_total': 0, 'get_cart_items': 0}

    category = get_object_or_404(Category, pk=id)
    products = Product.objects.filter(category=id)

    context = {'items': items, 'cart': cart, 'products': products, 'category': category}

    return render(request, 'store/search_category.html', context)