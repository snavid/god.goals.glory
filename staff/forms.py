# forms.py
from django import forms
from .models import Product, Review, Rating, Testimonial

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'status', 'quantity', 'image']

class PraiseForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['user', 'caption', 'product', 'image', 'image_2', 'image_3', 'image_4']

class OrderForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.Textarea)
    payment_method = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('cash', 'Cash'), ('paypal', 'PayPal')])

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment...', 'class': 'form-control'}),
        }

class RatingForm(forms.ModelForm):
    stars = forms.ChoiceField(choices=[(i, f"{i} Stars") for i in range(1, 6)], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Rating
        fields = ['stars']
