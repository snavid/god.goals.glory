from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
from .models import CustomUser
from staff.models import Product, Order, OrderItem

User = get_user_model()

def get_dummy_image():
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=b'test',  # Non-empty content
        content_type='image/jpeg'
    )

class AuthenticationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'email': 'test@example.com',
            'username': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'telephone': '+12125552368'  # Valid phone number
        }

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'email': 'test@example.com',
            'username': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'telephone': '+12125552368',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'profile_picture': get_dummy_image()
        })
        if response.status_code != 302:
            print('Register form errors:', response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        user = User.objects.get(email='test@example.com')
        self.assertFalse(user.is_active)

    def test_login_view(self):
        user = User.objects.create_user(**self.user_data)
        user.is_active = True
        user.save()
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        user = User.objects.create_user(**self.user_data)
        self.client.login(username='test@example.com', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

class UserProfileViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            telephone='+12125552368'
        )
        self.client.login(username='test@example.com', password='testpass123')

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        image = get_dummy_image()
        response = self.client.post(reverse('profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'test@example.com',
            'username': 'test@example.com',
            'telephone': '+12125552368',
            'profile_picture': image
        })
        if response.status_code != 302:
            print('Profile form errors:', response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(email='test@example.com')
        self.assertEqual(updated_user.first_name, 'Updated')

class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            telephone='+12125552368'
        )
        self.client.login(username='test@example.com', password='testpass123')
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
            size_xxl=True,
            image=get_dummy_image()
        )

    def test_homepage_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', response.context)
        self.assertIn('latest_products', response.context)

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], self.product)

class CartViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            telephone='+12125552368'
        )
        self.client.login(username='test@example.com', password='testpass123')
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
            size_xxl=True,
            image=get_dummy_image()
        )

    def test_add_to_cart(self):
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]), {
            'quantity': 2,
            'size': 'M'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OrderItem.objects.filter(
            product=self.product,
            order__user=self.user,
            order__is_completed=False
        ).exists())

    def test_cart_view(self):
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
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('order', response.context)

    def test_update_cart_item_size(self):
        order = Order.objects.create(
            user=self.user,
            total_price=Decimal('99.99'),
            address='123 Test St',
            payment_method='cash'
        )
        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            price=Decimal('99.99'),
            sizes='M'
        )
        response = self.client.post(reverse('update_cart_item_size', args=[item.id]), {
            'size': 'L'
        })
        self.assertEqual(response.status_code, 302)
        updated_item = OrderItem.objects.get(id=item.id)
        self.assertEqual(updated_item.sizes, 'L')

    def test_remove_cart_item(self):
        order = Order.objects.create(
            user=self.user,
            total_price=Decimal('99.99'),
            address='123 Test St',
            payment_method='cash'
        )
        item = OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            price=Decimal('99.99'),
            sizes='M'
        )
        response = self.client.post(reverse('remove_cart_item', args=[item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(OrderItem.objects.filter(id=item.id).exists()) 