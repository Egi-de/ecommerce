from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Product URLs
    path('products/', views.products_list, name='products_list'),
    path('products.html', lambda request: redirect('products_list', permanent=True)),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('products/<int:pk>/toggle-status/', views.toggle_product_status, name='toggle_product_status'),

    # Customer URLs
    path('customers/', views.customers_list, name='customers_list'),
]
