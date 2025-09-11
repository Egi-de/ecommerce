from django.urls import path
from . import views

urlpatterns = [
    # Home pages
    path('', views.home, name='home'),
    path('home-2/', views.home_2, name='home_2'),
    path('home-3/', views.home_3, name='home_3'),
    path('home-4/', views.home_4, name='home_4'),
    path('home-5/', views.home_5, name='home_5'),

    # Informational pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('404/', views.error_404, name='error_404'),

    # Blog pages
    path('blog/', views.blog, name='blog'),
    path('blog/<int:id>/', views.blog_single, name='blog_single'),
    path('blog/category/<str:category>/', views.blog_category, name='blog_category'),

    # Store pages
    path('store-list/', views.store_list, name='store-list'),
]

     