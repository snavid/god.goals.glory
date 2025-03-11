# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Review, Rating, Testimonial
from .forms import ProductForm, ReviewForm, RatingForm, PraiseForm
from django.http import JsonResponse

def staff_dashboard(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('staff_dashboard')  # Redirect to prevent form resubmission on refresh

    context = {
        'form': form,
        'fomu': PraiseForm(request.POST, request.FILES),
        'products': Product.objects.all(),
        'testimonials' : Testimonial.objects.all().order_by('-created_at'),
        'latest_products': Product.objects.order_by('-id')[:6]  # Get last 6 products
    }
    return render(request, 'staff/staff_dashboard.html', context)

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('homepage')  # Redirect back to homepage after submitting

    return redirect('homepage')

@login_required
def add_testimonial(request):
    if request.method == 'POST':
        fomu = PraiseForm(request.POST, request.FILES)  # Handle images
        if fomu.is_valid():
            testimonial = fomu.save(commit=False)
            testimonial.user = request.user  # Attach the logged-in user
            testimonial.save()
            return redirect('homepage')  # Redirect after saving

    return redirect('homepage')

@login_required
def add_rating(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={'stars': form.cleaned_data['stars']}
            )
            return redirect('homepage')  # Redirect back to homepage after submitting

    return redirect('homepage')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('staff_dashboard')  # Redirect to dashboard after update
    else:
        form = ProductForm(instance=product)
    return render(request, 'staff/update_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('staff_dashboard')

@login_required
def review_rate(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    ratings = Rating.objects.filter(product=product)
    return render(request, 'staff/review_rate.html', {'product': product, 'reviews': reviews, 'ratings': ratings})