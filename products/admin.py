from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Category
from .models import Order

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)