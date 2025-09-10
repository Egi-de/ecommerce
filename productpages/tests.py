# tests.py in the productpages app
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerce.models import Product  # Assuming models are shared
from .models import Review # Assuming a Review model exists

# A test case for the Review model
class ReviewModelTest(TestCase):
    """
    Tests for the Review model.
    """
    def setUp(self):
        # Create a user and product for the review
        self.user = User.objects.create_user(username="reviewer", password="password123")
        self.product = Product.objects.create(name="Reviewed Product", price=50.00, stock=5)
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="This is a great product!"
        )

    def test_review_creation(self):
        """
        Tests if a Review object can be created and saved successfully.
        """
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, "This is a great product!")
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.product, self.product)
        self.assertTrue(isinstance(self.review, Review))

# A test case for views related to product pages
class ProductPagesViewTest(TestCase):
    """
    Tests views that are specific to individual product pages.
    """
    def setUp(self):
        # Create a product to test the view
        self.product = Product.objects.create(name="Test Product", price=100.00, stock=1)

    def test_product_detail_view_with_valid_id(self):
        """
        Tests that the product detail view returns a 200 status code
        with a valid product ID.
        """
        response = self.client.get(reverse('product-detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'productpages/product_detail.html') # Assuming template path
        self.assertContains(response, self.product.name)

    def test_product_detail_view_with_invalid_id(self):
        """
        Tests that the product detail view returns a 404 status code
        with an invalid product ID.
        """
        response = self.client.get(reverse('product-detail', args=[9999]))
        self.assertEqual(response.status_code, 404)
