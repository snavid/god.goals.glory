from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Product(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold_out', 'Sold Out'),
        ('on_production', 'On Production'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')
    image_2 = models.ImageField(upload_to='products/' , blank=True, null=True )
    image_3 = models.ImageField(upload_to='products/' , blank=True, null=True )
    image_4 = models.ImageField(upload_to='products/' , blank=True, null=True )
    # Size availability
    size_s = models.BooleanField(default=True)
    size_m = models.BooleanField(default=True)
    size_l = models.BooleanField(default=True)
    size_xl = models.BooleanField(default=True)
    size_xxl = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        ratings = self.ratings.all()  # Fetch all related ratings
        if ratings.exists():
            return sum(rating.stars for rating in ratings) / ratings.count()
        return 0


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # One rating per user per product

    def __str__(self):
        return f"Rating {self.stars} by {self.user.username} on {self.product.name}"


class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="testimonials")
    image = models.ImageField(upload_to='testimonials/')
    image_2 = models.ImageField(upload_to='testimonials/' , blank=True, null=True )
    image_3 = models.ImageField(upload_to='testimonials/' , blank=True, null=True )
    image_4 = models.ImageField(upload_to='testimonials/' , blank=True, null=True )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.user.username} on {self.product.name}"




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False)
     
    STAGE_CHOICES = [
        ('Pending', 'Pending'),
        ('Ready', 'Ready'),
        ('Delivered', 'Delivered'),
    ]
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=10, choices=[('cash', 'Cash')])    
    address = models.TextField()  # Add this field to store the address
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    SIZE_CHOICES = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]

    sizes = models.CharField(max_length=10, choices=SIZE_CHOICES, default='M')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
    


class WaitlistUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  # Ensure unique emails
    joined_at = models.DateTimeField(auto_now_add=True)
    tel1 = PhoneNumberField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class WaitlistEmailTemplate(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    attachment = models.FileField(upload_to="email_attachments/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject