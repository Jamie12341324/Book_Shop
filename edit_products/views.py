from django.shortcuts import render,redirect
from django.urls import reverse
# method of importing a model from another app from chatgpt
from products.models import Product
from products.models import Order
from products.models import Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url="/accounts/login/")
def order_list(request):
    if not request.user.is_staff:
        return redirect("/accounts/login/") 
    orders=Order.objects.values().order_by("-created_at")
    template='order_list.html'
    context={
        "orders":orders
    }
    return render(request,template,context)
@login_required(login_url="/accounts/login/")
def my_orders(request):
    orders=Order.objects.filter(Q(user_id=request.user.id)).values().order_by("created_at")
    template='my_orders.html'
    context={
        "orders":orders
    }
    return render(request,template,context)



@login_required(login_url="/accounts/login/")
def product_add(request):
    """ Add a product to the store"""
    if not request.user.is_staff:
        return redirect("/accounts/login/") 
    if request.method=="POST":
        product=Product()
        product.creator=request.user
        product.isbn=request.POST.get("isbn")
        product.title=request.POST.get("title")
        product.author=request.POST.get("author")
        product.rating=request.POST.get("rating")
        product.description=request.POST.get("description")
        product.price=request.POST.get("price")
        product.category_id=request.POST.get("category")
        product.save()
        return redirect("/products/product_list/")
    template ='product_add.html'
    categories=Category.objects.values()
    context={
        "categories":categories,
    }
    return render(request, template, context)

@login_required(login_url="/accounts/login/")
def product_edit(request,product_id):
    if not request.user.is_staff:
        return redirect("/accounts/login/") 
    if request.method=="POST":
        product_to_change=Product.objects.get(Q(id=product_id))
        product_to_change.isbn=request.POST.get("isbn")
        product_to_change.title=request.POST.get("title")
        product_to_change.author=request.POST.get("author")
        product_to_change.rating=request.POST.get("rating")
        product_to_change.description=request.POST.get("description")
        product_to_change.price=request.POST.get("price")
        product_to_change.category_id=request.POST.get("category")
        product_to_change.save()
        return redirect("/products/product_list/")
    if request.method=="GET":
        product=Product.objects.get(id=product_id)
        categories=Category.objects.values()
        context={
            "product":product,
            "categories":categories,
        }
        template='product_edit.html'
        return render(request,template,context)

@login_required(login_url="/accounts/login/")
def product_delete(request,product_id):
    if not request.user.is_staff:
        return redirect("/accounts/login/") 
    if request.method=="GET":
        Product.objects.get(Q(id=product_id)).delete()
        return redirect("/products/product_list/")
