from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),

    # Account management
    path('account/orders/', views.account_orders, name='account_orders'),
    path('account/settings/', views.account_settings, name='account_settings'),
    path('account/address/', views.account_address, name='account_address'),
    path('account/payment/', views.account_payment, name='account_payment'),
    path('account/notifications/', views.account_notifications, name='account_notifications'),
]
