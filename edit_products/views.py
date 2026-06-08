from django.shortcuts import render

# Create your views here.

def product_add(request):
    """ Add a product to the store"""
    if request.user.is_superuser:
        pass
    template ='product_add.html'
    return render(request, template)