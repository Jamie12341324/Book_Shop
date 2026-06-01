from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.shortcuts import render
from django.contrib import messages
from .forms import ProductForm
# Create your views here.
def add_product(request):
    """ Add a product to the store"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners an do that')
        return redirect(reverse('home'))
    if request.method=='POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure form is valid.')
    else:
        form=ProductForm()

    form = ProductForm()
    template ='products/add_products.html'
    context = {
        'form': form,
    }
    return render(request, template, context)