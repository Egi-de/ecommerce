# tests.py in the admin_dashboard app
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# A test case for the admin dashboard view
class AdminDashboardViewTest(TestCase):
    """
    Tests for the admin dashboard view, ensuring it's restricted to staff users.
    """
    def setUp(self):
        # Create a regular user and a staff/admin user
        self.regular_user = User.objects.create_user(username="regularuser", password="password123")
        self.staff_user = User.objects.create_user(
            username="staffuser", 
            password="password123", 
            is_staff=True
        )
        self.dashboard_url = reverse('admin_dashboard') # Assuming 'admin_dashboard' is the URL name

    def test_dashboard_access_for_anonymous_user(self):
        """
        Tests that an anonymous user cannot access the admin dashboard and is redirected.
        """
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302) # Should be a redirect
        self.assertIn('/accounts/login/', response.url) # Redirect to the login page

    def test_dashboard_access_for_regular_user(self):
        """
        Tests that a logged-in non-staff user cannot access the dashboard.
        """
        self.client.login(username="regularuser", password="password123")
        response = self.client.get(self.dashboard_url)
        # Should return a 403 Forbidden or redirect to a different page
        # A common practice is to redirect to the login page with a permission denied message
        self.assertEqual(response.status_code, 302)
        # You would need to check the specific redirect behavior of your app here

    def test_dashboard_access_for_staff_user(self):
        """
        Tests that a staff user can successfully access the admin dashboard.
        """
        self.client.login(username="staffuser", password="password123")
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard/dashboard.html') # Assuming template path
