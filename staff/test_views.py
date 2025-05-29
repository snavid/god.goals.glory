from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from .models import Product, Review, Rating, Testimonial, Order, OrderItem, WaitlistUser, WaitlistEmailTemplate
from .forms import ProductForm, ReviewForm, RatingForm, PraiseForm

User = get_user_model()

class StaffViewsTest(TestCase):
    def setUp(self):
        # Create a staff user
        self.staff_user = User.objects.create_user(
            username='staff@example.com',
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )
        # Create a regular user
        self.regular_user = User.objects.create_user(
            username='user@example.com',
            email='user@example.com',
            password='userpass123'
        )
        self.client = Client()
        
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('99.99'),
            description='Test Description',
            quantity=10,
            status='available',
            size_s=True,
            size_m=True,
            size_l=True,
            size_xl=True,
            size_xxl=True
        )

    def test_staff_dashboard_access(self):
        # Test staff access
        self.client.login(username='staff@example.com', password='staffpass123')
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Test non-staff access
        self.client.login(username='user@example.com', password='userpass123')
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect

    def test_add_product(self):
        self.client.login(username='staff@example.com', password='staffpass123')
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        response = self.client.post(reverse('add_product'), {
            'name': 'New Product',
            'price': '149.99',
            'description': 'New Description',
            'quantity': 5,
            'image': image,
            'status': 'available',
            'size_s': True,
            'size_m': True,
            'size_l': True,
            'size_xl': True,
            'size_xxl': True
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        self.assertTrue(Product.objects.filter(name='New Product').exists())

    def test_edit_product(self):
        self.client.login(username='staff@example.com', password='staffpass123')
        response = self.client.post(
            reverse('edit_product', args=[self.product.id]),
            {
                'name': 'Updated Product',
                'price': '199.99',
                'description': 'Updated Description',
                'quantity': 15,
                'status': 'available',
                'size_s': True,
                'size_m': True,
                'size_l': True,
                'size_xl': True,
                'size_xxl': True
            }
        )
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        updated_product = Product.objects.get(id=self.product.id)
        self.assertEqual(updated_product.name, 'Updated Product')

    def test_delete_product(self):
        self.client.login(username='staff@example.com', password='staffpass123')
        response = self.client.post(reverse('delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

class UserInteractionViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user@example.com',
            email='user@example.com',
            password='userpass123'
        )
        self.client = Client()
        self.client.login(username='user@example.com', password='userpass123')
        
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('99.99'),
            description='Test Description',
            quantity=10,
            status='available',
            size_s=True,
            size_m=True,
            size_l=True,
            size_xl=True,
            size_xxl=True
        )

    def test_add_review(self):
        response = self.client.post(
            reverse('add_review', args=[self.product.id]),
            {'comment': 'Great product!'}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        self.assertTrue(Review.objects.filter(
            product=self.product,
            user=self.user,
            comment='Great product!'
        ).exists())

    def test_add_rating(self):
        response = self.client.post(
            reverse('add_rating', args=[self.product.id]),
            {'stars': 5}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        self.assertTrue(Rating.objects.filter(
            product=self.product,
            user=self.user,
            stars=5
        ).exists())

class WaitlistViewsTest(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='staff@example.com',
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )
        self.client = Client()
        self.client.login(username='staff@example.com', password='staffpass123')

    def test_join_waitlist(self):
        response = self.client.post(reverse('join_waitlist'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'tel1': '+1234567890'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        self.assertTrue(WaitlistUser.objects.filter(
            email='john@example.com'
        ).exists())

    def test_waitlist_admin(self):
        response = self.client.get(reverse('waitlist_admin'))
        self.assertEqual(response.status_code, 200)

    def test_email_template_management(self):
        # Create template
        template = WaitlistEmailTemplate.objects.create(
            subject='Test Template',
            content='Test Content'
        )
        
        # Test template list view
        response = self.client.get(reverse('email_template_list'))
        self.assertEqual(response.status_code, 200)
        
        # Test template edit
        response = self.client.post(
            reverse('email_template_edit', args=[template.id]),
            {
                'subject': 'Updated Template',
                'content': 'Updated Content'
            }
        )
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        updated_template = WaitlistEmailTemplate.objects.get(id=template.id)
        self.assertEqual(updated_template.subject, 'Updated Template') 