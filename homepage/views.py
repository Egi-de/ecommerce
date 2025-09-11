from django.shortcuts import render
from .models import Store

# Create your views here.

def home(request):
    """Home page (Home 1)"""
    return render(request, 'index.html')

# Alternative home pages
def home_2(request):
    """Home 2"""
    return render(request, 'pages/index-2.html')

def home_3(request):
    """Home 3"""
    return render(request, 'pages/index-3.html')

def home_4(request):
    """Home 4"""
    return render(request, 'pages/index-4.html')

def home_5(request):
    """Home 5"""
    return render(request, 'pages/index-5.html')

# Informational pages
def about(request):
    """About us page"""
    return render(request, 'pages/about.html')

def contact(request):
    """Contact page"""
    return render(request, 'pages/contact.html')

def error_404(request):
    """404 Error page"""
    return render(request, 'pages/404error.html')

# Blog pages
def blog(request):
    """Blog listing page"""
    return render(request, 'pages/blog.html')

def blog_single(request, id=1):
    """Blog single post"""
    return render(request, 'pages/blog-single.html')

def blog_category(request, category='general'):
    """Blog category page"""
    return render(request, 'pages/blog-category.html')

def store_list(request):
    """Store list page"""
    stores = Store.objects.all()

    return render(request, 'pages/store-list.html', {'stores': stores})