from django.urls import path
from . import views
urlpatterns = [
    # path('', views.all_products, name='products'),
    path('add/', views.add_product, name='add_product'),
    path('product_list/', views.view_products, name='product_list'),
    path('product_detail/<int:product_id>/', views.product_details, name='product_detail'),
    path('checkout/<int:product_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    
    # path('<int:product_id>/', views.product_detail, name='product_detail'),
    # path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    # path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]