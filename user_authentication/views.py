from django.shortcuts import render

# Create your views here.

def login_view(request):
    """Sign in page"""
    return render(request, 'pages/signin.html')

def logout_view(request):
    """Sign out page"""
    return render(request, 'pages/signout.html')

def signup_view(request):
    """Sign up page"""
    return render(request, 'pages/signup.html')

def forgot_password_view(request):
    """Forgot password page"""
    return render(request, 'pages/forgot-password.html')

# Account management views
def account_orders(request):
    """Account orders page"""
    return render(request, 'pages/account-orders.html')

def account_settings(request):
    """Account settings page"""
    return render(request, 'pages/account-settings.html')

def account_address(request):
    """Account address page"""
    return render(request, 'pages/account-address.html')

def account_payment(request):
    """Account payment method page"""
    return render(request, 'pages/account-payment-method.html')

def account_notifications(request):
    """Account notifications page"""
    return render(request, 'pages/account-notification.html')
