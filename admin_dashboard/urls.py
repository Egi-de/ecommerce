from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("categories/", views.categories_list, name="categories_list"),
]
