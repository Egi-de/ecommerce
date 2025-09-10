from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product
from .forms import ProductForm
import tempfile
from PIL import Image
import io


class ProductCRUDTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass123')

        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=19.99,
            category='Snacks & Munchies',
            stock_quantity=100,
            status='active'
        )

    def create_test_image(self):
        """Create a test image file"""
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='JPEG')
        image_file.seek(0)
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=image_file.read(),
            content_type='image/jpeg'
        )

    def test_product_list_view(self):
        """Test product list view"""
        response = self.client.get(reverse('products_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'Products')

    def test_product_create_view_get(self):
        """Test product create view GET request"""
        response = self.client.get(reverse('create_product'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add New Product')

    def test_product_create_view_post(self):
        """Test product create view POST request"""
        data = {
            'name': 'New Test Product',
            'description': 'New Test Description',
            'price': 29.99,
            'category': 'Bakery & Biscuits',
            'stock_quantity': 50,
            'status': 'active'
        }
        response = self.client.post(reverse('create_product'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation

        # Check if product was created
        self.assertTrue(Product.objects.filter(name='New Test Product').exists())

    def test_product_detail_view(self):
        """Test product detail view"""
        response = self.client.get(reverse('product_detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, self.product.description)

    def test_product_edit_view_get(self):
        """Test product edit view GET request"""
        response = self.client.get(reverse('edit_product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Product')
        self.assertContains(response, self.product.name)

    def test_product_edit_view_post(self):
        """Test product edit view POST request"""
        data = {
            'name': 'Updated Test Product',
            'description': 'Updated Description',
            'price': 39.99,
            'category': 'Dairy, Bread & Eggs',
            'stock_quantity': 75,
            'status': 'draft'
        }
        response = self.client.post(reverse('edit_product', kwargs={'pk': self.product.pk}), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update

        # Check if product was updated
        updated_product = Product.objects.get(pk=self.product.pk)
        self.assertEqual(updated_product.name, 'Updated Test Product')
        self.assertEqual(updated_product.status, 'draft')

    def test_product_delete_view_get(self):
        """Test product delete view GET request"""
        response = self.client.get(reverse('delete_product', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure?')
        self.assertContains(response, self.product.name)

    def test_product_delete_view_post(self):
        """Test product delete view POST request"""
        product_id = self.product.pk
        response = self.client.post(reverse('delete_product', kwargs={'pk': product_id}))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion

        # Check if product was deleted
        self.assertFalse(Product.objects.filter(pk=product_id).exists())

    def test_product_search_functionality(self):
        """Test product search functionality"""
        # Create additional products for search testing
        Product.objects.create(
            name='Apple Juice',
            description='Fresh apple juice',
            price=5.99,
            category='Tea, Coffee & Drinks',
            stock_quantity=30,
            status='active'
        )

        # Test search by name
        response = self.client.get(reverse('products_list'), {'search': 'Apple'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Apple Juice')
        self.assertNotContains(response, 'Test Product')

    def test_product_filter_by_status(self):
        """Test product filtering by status"""
        # Create products with different statuses
        Product.objects.create(
            name='Draft Product',
            description='Draft product',
            price=15.99,
            category='Snacks & Munchies',
            stock_quantity=20,
            status='draft'
        )

        # Test filter by status
        response = self.client.get(reverse('products_list'), {'status': 'draft'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Draft Product')

    def test_product_form_validation(self):
        """Test product form validation"""
        # Test with invalid data
        form_data = {
            'name': '',  # Required field
            'description': 'Test',
            'price': -10,  # Invalid price
            'category': 'Snacks & Munchies',
            'stock_quantity': -5,  # Invalid stock
            'status': 'active'
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('price', form.errors)
        self.assertIn('stock_quantity', form.errors)

    def test_product_with_image_upload(self):
        """Test product creation with image upload"""
        test_image = self.create_test_image()
        data = {
            'name': 'Product with Image',
            'description': 'Product with test image',
            'price': 25.99,
            'category': 'Fruits & Vegetables',
            'stock_quantity': 40,
            'status': 'active',
            'image': test_image
        }
        response = self.client.post(reverse('create_product'), data)
        self.assertEqual(response.status_code, 302)

        # Check if product was created with image
        product = Product.objects.get(name='Product with Image')
        self.assertTrue(product.image)


class ProductModelTestCase(TestCase):
    def test_product_str_method(self):
        """Test product string representation"""
        product = Product(name='Test Product')
        self.assertEqual(str(product), 'Test Product')

    def test_product_status_badge_class(self):
        """Test product status badge class property"""
        product = Product(status='active')
        self.assertEqual(product.status_badge_class, 'bg-light-primary text-dark-primary')

        product.status = 'draft'
        self.assertEqual(product.status_badge_class, 'bg-light-warning text-dark-warning')

        product.status = 'deactive'
        self.assertEqual(product.status_badge_class, 'bg-light-danger text-dark-danger')

    def test_product_status_display(self):
        """Test product status display property"""
        product = Product(status='active')
        self.assertEqual(product.status_display, 'Active')
