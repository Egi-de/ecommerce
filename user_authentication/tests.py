# tests.py in the user_authentication app
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# A test case for the User model and its basic functionality
class UserModelTest(TestCase):
    """
    Tests the creation and properties of the built-in Django User model.
    """
    def test_create_user(self):
        """
        Ensures a user can be created with a username and password.
        """
        user = User.objects.create_user(username="testuser", password="password123")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """
        Ensures a superuser can be created with the correct permissions.
        """
        admin_user = User.objects.create_superuser(
            username="adminuser", 
            email="admin@example.com", 
            password="password123"
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.check_password("password123"))

# A test case for views related to user authentication
class AuthenticationViewTest(TestCase):
    """
    Tests the login, logout, and registration views.
    """
    def setUp(self):
        self.client = self.client
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123',
        }
        self.login_url = reverse('login')  # Assuming 'login' is the URL name
        self.register_url = reverse('register')  # Assuming 'register' is the URL name
        self.logout_url = reverse('logout')  # Assuming 'logout' is the URL name
        self.homepage_url = reverse('homepage') # Assuming 'homepage' is the name of the home page URL

    def test_registration_view(self):
        """
        Tests a successful user registration and redirection.
        """
        # POST a new user's data to the registration view
        response = self.client.post(self.register_url, self.user_data, follow=True)
        # Check that a new user was created in the database
        self.assertEqual(User.objects.count(), 1)
        # The view should redirect to the homepage or login page after successful registration
        self.assertRedirects(response, self.homepage_url) 
        self.assertTemplateUsed(response, 'homepage/index.html')

    def test_login_view_success(self):
        """
        Tests a successful user login.
        """
        # First, create a user to log in with
        User.objects.create_user(username="testuser", password="password123")
        
        # POST login credentials
        response = self.client.post(self.login_url, {
            'username': 'testuser', 
            'password': 'password123'
        }, follow=True)
        
        # Check for successful authentication and redirection
        self.assertRedirects(response, self.homepage_url)
        # The user should now be logged in
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_view_failure(self):
        """
        Tests a failed login attempt with invalid credentials.
        """
        # POST incorrect credentials without creating a user first
        response = self.client.post(self.login_url, {
            'username': 'nonexistent', 
            'password': 'wrongpassword'
        })
        # The status code should be 200 (page rendered with error) and user should not be authenticated
        self.assertEqual(response.status_code, 200)
        user = response.context.get('user')
        if user:
            self.assertFalse(user.is_authenticated)

    def test_logout_view(self):
        """
        Tests a user logging out and being redirected correctly.
        """
        # Log in a user first
        User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        
        # Request the logout URL
        response = self.client.get(self.logout_url, follow=True)
        
        # Check that the user is no longer authenticated and redirected to the login page
        self.assertRedirects(response, self.homepage_url)
        self.assertFalse(response.context['user'].is_authenticated)
