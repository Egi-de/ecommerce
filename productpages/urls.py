from django.urls import path
from . import views

urlpatterns = [
    # Product/Shop pages
    path('', views.product_list, name='product_list'),
    path('grid-3/', views.product_grid_3, name='product_grid_3'),
    path('list/', views.product_list_filter, name='product_list_filter'),
    path('filter/', views.product_filter, name='product_filter'),
    path('wide/', views.product_wide, name='product_wide'),
    path('single/<int:id>/', views.product_single, name='product_single'),
    path('single-v2/<int:id>/', views.product_single_v2, name='product_single_v2'),
    path('wishlist/', views.product_wishlist, name='product_wishlist'),
    path('cart/', views.product_cart, name='product_cart'),
    path('checkout/', views.product_checkout, name='product_checkout'),

    # Store pages
    path('stores/', views.store_list, name='store_list'),
    path('stores/grid/', views.store_grid, name='store_grid'),
    path('stores/<int:id>/', views.store_single, name='store_single'),
]
