from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from .models import (
    Product, Review, Rating, Testimonial,
    Order, OrderItem, WaitlistUser, WaitlistEmailTemplate
)

User = get_user_model()

class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('99.99'),
            description='Test Description',
            quantity=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, Decimal('99.99'))
        self.assertEqual(self.product.quantity, 10)
        self.assertEqual(self.product.status, 'available')

    def test_product_average_rating(self):
        Rating.objects.create(
            product=self.product,
            user=self.user,
            stars=4
        )
        Rating.objects.create(
            product=self.product,
            user=User.objects.create_user(username='testuser2', email='test2@example.com', password='testpass123'),
            stars=5
        )
        self.assertEqual(self.product.average_rating(), 4.5)

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('99.99'),
            description='Test Description',
            quantity=10
        )

    def test_review_creation(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            comment='Great product!'
        )
        self.assertEqual(review.comment, 'Great product!')
        self.assertEqual(str(review), f"Review by {self.user.username} on {self.product.name}")

class RatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('99.99'),
            description='Test Description',
            quantity=10
        )

    def test_rating_creation(self):
        rating = Rating.objects.create(
            product=self.product,
            user=self.user,
            stars=5
        )
        self.assertEqual(rating.stars, 5)
        self.assertEqual(str(rating), f"Rating 5 by {self.user.username} on {self.product.name}")

    def test_unique_rating_per_user(self):
        Rating.objects.create(
            product=self.product,
            user=self.user,
            stars=5
        )
        # Attempting to create another rating for the same user and product should raise an error
        with self.assertRaises(Exception):
            Rating.objects.create(
                product=self.product,
                user=self.user,
                stars=4
            )

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('99.99'),
            description='Test Description',
            quantity=10
        )

    def test_order_creation(self):
        order = Order.objects.create(
            user=self.user,
            total_price=Decimal('99.99'),
            address='123 Test St',
            payment_method='cash'
        )
        self.assertEqual(order.total_price, Decimal('99.99'))
        self.assertEqual(order.stage, 'Pending')
        self.assertEqual(str(order), f"Order {order.id} by {self.user.username}")

    def test_order_with_items(self):
        order = Order.objects.create(
            user=self.user,
            total_price=Decimal('199.98'),
            address='123 Test St',
            payment_method='cash'
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            price=Decimal('99.99'),
            sizes='M'
        )
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().quantity, 2)

class WaitlistUserModelTest(TestCase):
    def test_waitlist_user_creation(self):
        user = WaitlistUser.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            tel1='+1234567890'
        )
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(str(user), 'John Doe (john@example.com)')

class WaitlistEmailTemplateModelTest(TestCase):
    def test_email_template_creation(self):
        template = WaitlistEmailTemplate.objects.create(
            subject='Welcome to Waitlist',
            content='Welcome to our waitlist!'
        )
        self.assertEqual(template.subject, 'Welcome to Waitlist')
        self.assertEqual(str(template), 'Welcome to Waitlist')
