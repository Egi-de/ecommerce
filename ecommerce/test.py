# tests.py in the ecommerce app
from django.test import TestCase
from django.urls import reverse
from .models import Product, Order, OrderItem
from django.contrib.auth.models import User

# A test case for the Product model
class ProductModelTest(TestCase):
    """
    Tests for the Product model to ensure correct data handling and string representation.
    """
    def setUp(self):
        # Create a sample product for testing
        self.product = Product.objects.create(
            name="Test Product",
            description="A high-quality test product.",
            price=99.99,
            stock=10
        )

    def test_product_creation(self):
        """
        Tests if a Product object can be created and saved successfully.
        """
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 99.99)
        self.assertTrue(isinstance(self.product, Product))

    def test_string_representation(self):
        """
        Tests the string representation of the Product model.
        """
        self.assertEqual(str(self.product), self.product.name)

# A test case for the Order and OrderItem models
class OrderModelTest(TestCase):
    """
    Tests for the Order and OrderItem models.
    """
    def setUp(self):
        # Create a user and products to simulate an order
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.product1 = Product.objects.create(name="Laptop", price=1200.00, stock=5)
        self.product2 = Product.objects.create(name="Mouse", price=25.00, stock=20)
        self.order = Order.objects.create(user=self.user)

    def test_order_creation(self):
        """
        Tests if an Order object can be created and is associated with the user.
        """
        self.assertEqual(self.order.user, self.user)
        self.assertFalse(self.order.is_paid)

    def test_add_item_to_order(self):
        """
        Tests adding an item to an order and verifying the total price.
        """
        # Add a single item to the order
        OrderItem.objects.create(order=self.order, product=self.product1, quantity=1)
        self.assertEqual(self.order.get_cart_total(), 1200.00)

        # Add another item
        OrderItem.objects.create(order=self.order, product=self.product2, quantity=2)
        # Recalculate and test the new total
        expected_total = 1200.00 + (25.00 * 2)
        self.assertEqual(self.order.get_cart_total(), expected_total)

# A test case for views related to the ecommerce app
class EcommerceViewTest(TestCase):
    """
    Tests for views related to the ecommerce app, ensuring correct rendering and
    data context.
    """
    def setUp(self):
        # Use Django's test client to make requests
        self.client = self.client
        self.product = Product.objects.create(name="Test Product", price=100.00, stock=1)

    def test_product_list_view(self):
        """
        Tests the product list view to ensure it returns a 200 OK status code
        and uses the correct template.
        """
        response = self.client.get(reverse('product-list')) # Assuming 'product-list' is the URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/product_list.html')
        self.assertContains(response, self.product.name)

    def test_product_detail_view(self):
        """
        Tests the product detail view, including a check for a valid product ID.
        """
        # Test with a valid product ID
        response = self.client.get(reverse('product-detail', args=[self.product.id])) # Assuming 'product-detail'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ecommerce/product_detail.html')
        self.assertContains(response, self.product.name)

        # Test with an invalid product ID (should return 404)
        response = self.client.get(reverse('product-detail', args=[99999]))
        self.assertEqual(response.status_code, 404)
