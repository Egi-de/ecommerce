# tests.py in the homepage app
from django.test import TestCase
from django.urls import reverse

class HomepageViewTest(TestCase):
    """
    Tests for the homepage view.
    """
    def test_homepage_view_status_code(self):
        """
        Ensures the homepage view returns a 200 OK status code.
        """
        response = self.client.get(reverse('homepage')) # Assuming 'homepage' is the URL name
        self.assertEqual(response.status_code, 200)

    def test_homepage_view_template(self):
        """
        Ensures the homepage view uses the correct template.
        """
        response = self.client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'homepage/index.html')
