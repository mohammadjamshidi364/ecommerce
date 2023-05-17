from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json

from .models import *




def store(request):
    
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    
    products = Product.objects.all()
    
    products = Product.objects.filter(name__icontains=q)
    
    
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total":0 , "get_cart_items":0}
        cartItem = order['get_cart_items']
        
    context = {'products':products , 'cartItem':cartItem}
    return render(request , 'store/store.html' , context)

@login_required(login_url="login")
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {"get_cart_total":0 , "get_cart_items":0}
        cartItem = order['get_cart_items']
        
    context = {'items':items , 'order':order , 'cartItem':cartItem}
    return render(request , 'store/cart.html' , context)

@login_required(login_url="login")
def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer 
        order , created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
        cartItem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0 , "get_cart_items":0}
    
    context = {'order':order , 'items':items , 'cartItem':cartItem}
    return render(request , 'store/checkout.html', context)

@login_required(login_url="login")
def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order , created = Order.objects.get_or_create(customer=customer , complete=False)
    
    orderItem , created = OrderItem.objects.get_or_create(product=product , order=order)
    
    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('item was added' , safe=False)