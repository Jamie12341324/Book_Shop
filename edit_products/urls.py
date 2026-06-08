from django.urls import path
from . import views

urlpatterns = [
    path('product_add/', views.product_add, name='product_add'),
]