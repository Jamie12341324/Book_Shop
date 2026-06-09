from django.urls import path
from . import views

urlpatterns = [
    path('product_add/', views.product_add, name='product_add'),
    path('product_delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('product_edit/<int:product_id>/', views.product_edit, name='product_edit'),
]