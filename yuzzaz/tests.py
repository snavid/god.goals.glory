from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import CustomUser

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'John',
            'last_name': 'Doe',
            'telephone': '+1234567890'
        }

    def test_user_creation(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(str(user), 'John Doe')

    def test_user_with_profile_picture(self):
        # Create a simple image file for testing
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # Empty content for testing
            content_type='image/jpeg'
        )
        
        user = CustomUser.objects.create_user(
            **self.user_data,
            profile_picture=image
        )
        self.assertTrue(user.profile_picture)

    def test_user_is_counsellor_property(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertFalse(user.is_counsellor)

    def test_unique_email(self):
        CustomUser.objects.create_user(**self.user_data)
        # Attempting to create another user with the same email should raise an error
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(
                email='test@example.com',
                username='test2@example.com',
                password='anotherpass123',
                first_name='Jane',
                last_name='Doe',
                telephone='+1987654321'
            )

    def test_username_is_email(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.username, user.email)
