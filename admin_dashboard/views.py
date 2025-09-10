from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Product, Customer, DashboardStats
from .forms import ProductForm, ProductSearchForm

# Create your views here.

@login_required(login_url='/auth/login/')
def dashboard(request):
    """Dashboard view with dynamic statistics"""

    # Calculate dashboard statistics
    today = timezone.now().date()
    two_days_ago = today - timedelta(days=2)
    current_month = today.replace(day=1)

    # Get or create today's stats
    stats, created = DashboardStats.objects.get_or_create(
        date=today,
        defaults={
            'total_earnings': 0,
            'daily_earnings': 0,
            'new_customers': 0,
            'total_customers': Customer.objects.count()
        }
    )

    # Calculate monthly earnings (sum of all daily earnings this month)
    monthly_earnings = DashboardStats.objects.filter(
        date__gte=current_month
    ).aggregate(total=Sum('daily_earnings'))['total'] or 0

    # Calculate new customers in last 2 days
    new_customers_2_days = Customer.objects.filter(
        created_at__date__gte=two_days_ago
    ).count()

    # Total customers
    total_customers = Customer.objects.count()

    # Total products
    total_products = Product.objects.filter(is_active=True).count()

    # Recent customers (last 5)
    recent_customers = Customer.objects.select_related('user').order_by('-created_at')[:5]

    # Recent products (last 5)
    recent_products = Product.objects.filter(is_active=True).order_by('-created_at')[:5]

    context = {
        'monthly_earnings': monthly_earnings,
        'total_customers': total_customers,
        'new_customers_2_days': new_customers_2_days,
        'total_products': total_products,
        'recent_customers': recent_customers,
        'recent_products': recent_products,
        'today': today,
    }

    return render(request, 'dashboard/index.html', context)

@login_required(login_url='/auth/login/')
def create_product(request):
    """Create new product view"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('products_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'title': 'Add New Product',
        'submit_text': 'Create Product'
    }
    return render(request, 'dashboard/add-product.html', context)

@login_required(login_url='/auth/login/')
def products_list(request):
    """List all products with search and filtering"""
    search_form = ProductSearchForm(request.GET)
    products = Product.objects.all().order_by('-created_at')

    # Apply search and filters
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')
        status_filter = search_form.cleaned_data.get('status')
        category_filter = search_form.cleaned_data.get('category')

        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__icontains=search_query)
            )

        if status_filter:
            products = products.filter(status=status_filter)

        if category_filter:
            products = products.filter(category=category_filter)

    # Pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'search_form': search_form,
        'total_products': products.count(),
        'page_obj': page_obj,
    }
    return render(request, 'dashboard/products.html', context)

@login_required(login_url='/auth/login/')
def product_detail(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'dashboard/product-detail.html', context)


@login_required(login_url='/auth/login/')
def edit_product(request, pk):
    """Edit product view"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('products_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'title': f'Edit Product: {product.name}',
        'submit_text': 'Update Product'
    }
    return render(request, 'dashboard/add-product.html', context)


@login_required(login_url='/auth/login/')
def delete_product(request, pk):
    """Delete product view"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('products_list')

    context = {
        'product': product,
    }
    return render(request, 'dashboard/delete-product.html', context)


@login_required(login_url='/auth/login/')
def toggle_product_status(request, pk):
    """Toggle product active status via AJAX"""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        product.is_active = not product.is_active
        product.save()

        return JsonResponse({
            'success': True,
            'is_active': product.is_active,
            'message': f'Product "{product.name}" {"activated" if product.is_active else "deactivated"} successfully!'
        })

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required(login_url='/auth/login/')
def customers_list(request):
    """List all customers"""
    customers = Customer.objects.select_related('user').order_by('-created_at')
    context = {
        'customers': customers,
        'total_customers': customers.count()
    }
    return render(request, 'dashboard/customers.html', context)
