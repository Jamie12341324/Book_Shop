from django.shortcuts import render,redirect
from django.urls import reverse
# method of importing a model from another app from chatgpt
from products.models import Product
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

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
        product.save()
        return redirect("/products/product_list/")
    template ='product_add.html'
    return render(request, template)

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
        product_to_change.save()
        return redirect("/products/product_list/")
    if request.method=="GET":
        product=Product.objects.get(id=product_id)
        context={
            "product":product,
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
