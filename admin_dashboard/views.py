from django.shortcuts import render
from .models import Category
# Create your views here.

def dashboard(request):
    """Dashboard view"""
    return render(request, 'dashboard/index.html')


def categories_list(request):
    categories = Category.objects.all()
    return render(request, "dashboard/categories.html", {"categories": categories})

