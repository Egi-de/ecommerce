from django.shortcuts import render

# Create your views here.

def product_list(request):
    """Shop Grid - Filter (main product listing)"""
    return render(request, 'pages/shop-grid.html')

def product_grid_3(request):
    """Shop Grid - 3 column"""
    return render(request, 'pages/shop-grid-3-column.html')

def product_list_filter(request):
    """Shop List - Filter"""
    return render(request, 'pages/shop-list.html')

def product_filter(request):
    """Shop - Filter"""
    return render(request, 'pages/shop-filter.html')

def product_wide(request):
    """Shop Wide"""
    return render(request, 'pages/shop-fullwidth.html')

def product_single(request, id=1):
    """Shop Single"""
    return render(request, 'pages/shop-single.html')

def product_single_v2(request, id=1):
    """Shop Single v2"""
    return render(request, 'pages/shop-single-2.html')

def product_wishlist(request):
    """Shop Wishlist"""
    return render(request, 'pages/shop-wishlist.html')

def product_cart(request):
    """Shop Cart"""
    return render(request, 'pages/shop-cart.html')

def product_checkout(request):
    """Shop Checkout"""
    return render(request, 'pages/shop-checkout.html')

# Store Views
def store_list(request):
    """Store List"""
    return render(request, 'pages/store-list.html')

def store_grid(request):
    """Store Grid"""
    return render(request, 'pages/store-grid.html')

def store_single(request, id=1):
    """Store Single"""
    return render(request, 'pages/store-single.html')
