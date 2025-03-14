# views.py
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from .models import WaitlistUser, WaitlistEmailTemplate
from .forms import WaitlistSignupForm, EmailTemplateForm
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Review, Rating, Testimonial, Order, OrderItem
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
    form = PraiseForm()
    if request.method == 'POST':
        form = PraiseForm(request.POST, request.FILES)  # Handle images
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user  # Attach the logged-in user
            testimonial.save()
            messages.success(request, 'Testimonial added successfully')
            return redirect('staff_dashboard')  # Redirect after saving
    context = {
        'form': form,
        'title': 'Add Testimonial',
        'action': 'Add Testimonial',
    }
    return render(request, 'staff/actions_form.html', context)


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



def testimonials_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'staff/testimonials_list.html', {'testimonial': testimonials})

def edit_testimonial(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    
    if request.method == "POST":
        form = PraiseForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'testimonial edited successfully')
            return redirect('testimonials_list')
    else:
        form = PraiseForm(instance=testimonial)
    
    return render(request, 'staff/actions_form.html', {'form': form, 'title': 'Edit testimonial'})


@login_required
def add_testimonial(request):
    if request.method == 'POST':
        form = PraiseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial added successfully')
            return redirect('testimonials_list')
    else:
        form = PraiseForm()
    context = {
    'form': form,
    'title': 'Add testimonial',
    'action': 'Add testimonial',
    }
    return render(request, 'staff/actions_form.html', context)

@login_required
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted successfully')
    return redirect('testimonials_list')

User = get_user_model()

@login_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'staff/users_list.html', {'user': users})

@login_required
def orders_list(request):
    orders = Order.objects.all()
    return render(request, 'staff/orders_list.html', {'order': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related('items'), id=order_id)
    return render(request, 'staff/order_details.html', {'order': order})

@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('orders_list')




def products_list(request):
    products = Product.objects.all()
    return render(request, 'staff/products_list.html', {'product': products})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product edited successfully')
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'staff/actions_form.html', {'form': form, 'title': 'Edit Product'})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully')
            return redirect('products_list')
    else:
        form = ProductForm()
    context = {
    'form': form,
    'title': 'Add Product',
    'action': 'Add Product',
    }
    return render(request, 'staff/actions_form.html', context)

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('products_list')



@login_required
def review_rate(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    ratings = Rating.objects.filter(product=product)
    return render(request, 'staff/review_rate.html', {'product': product, 'reviews': reviews, 'ratings': ratings})







def join_waitlist(request):
    """Allow users to join the waitlist and receive confirmation email."""
    if request.method == "POST":
        form = WaitlistSignupForm(request.POST)
        if form.is_valid():
            waitlist_user = form.save()
            
            # Confirmation email
            subject = "🎉 Welcome to the GOD·GOALS·GLORY Waitlist!"
            html_content = render_to_string("emails/waitlist_confirmation.html", {'user': waitlist_user})
            plain_content = strip_tags(html_content)
            email = EmailMultiAlternatives(subject, plain_content, to=[waitlist_user.email])
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(request, "You've been added to the waitlist! Check your email for confirmation.")
            return redirect("land")
        else:
            # messages.error(request, "Please enter a valid email.")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    
    else:
        form = WaitlistSignupForm()

    return render(request, "yuzzaz/land.html", {"form": form})

def waitlist_admin(request):
    """Allow staff to view all waitlist users."""
    users = WaitlistUser.objects.all().order_by('-joined_at')
    return render(request, "waitlist/admin.html", {"users": users})

def send_bulk_email(request):
    """Send emails to all waitlist users."""
    if request.method == "POST":
        form = EmailTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            email_template = form.save()

            users = WaitlistUser.objects.all()
            recipient_list = [user.email for user in users]

            html_content = email_template.content
            plain_content = strip_tags(html_content)
            subject = email_template.subject

            email = EmailMultiAlternatives(subject, plain_content, to=recipient_list)
            email.attach_alternative(html_content, "text/html")
            if email_template.attachment:
                email.attach(email_template.attachment.name, email_template.attachment.read())

            email.send()
            messages.success(request, "Email sent to all waitlist users!")
            return redirect("waitlist_admin")
        else:
            messages.error(request, "Error sending email.")

    else:
        form = EmailTemplateForm()

    return render(request, "waitlist/send_email.html", {"form": form})










# List email templates
def email_template_list(request):
    templates = WaitlistEmailTemplate.objects.all()
    return render(request, 'emails/template_list.html', {'templates': templates})

# Edit an existing template
def email_template_edit(request, template_id):
    template = get_object_or_404(WaitlistEmailTemplate, id=template_id)
    
    if request.method == "POST":
        form = EmailTemplateForm(request.POST, request.FILES, instance=template)
        if form.is_valid():
            form.save()
            return redirect('email_template_list')
    else:
        form = EmailTemplateForm(instance=template)
    
    return render(request, 'emails/template_form.html', {'form': form})

# Create a new template
def email_template_create(request):
    if request.method == "POST":
        form = EmailTemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('email_template_list')
    else:
        form = EmailTemplateForm()
    
    return render(request, 'emails/template_form.html', {'form': form})

def delete_template(request, template_id):
    template = get_object_or_404(WaitlistEmailTemplate, id=template_id)
    template.delete()
    messages.success(request, "Email template deleted successfully.")
    return redirect("email_template_list")

# View: Send bulk emails
# def send_bulk_email(request, template_id):
#     template = get_object_or_404(WaitlistEmailTemplate, id=template_id)
#     # users = ["user1@example.com", "user2@example.com"]  # Replace with actual waitlist users  DB
#     users = WaitlistUser.objects.values_list("email", flat=True)

#     subject = template.subject
#     content = template.content
#     attachment = template.attachment
#     # html_message = render_to_string("emails/email_template.html", {"subject": subject, "content": content})
#     html_message = render_to_string("emails/send_email.html", {"subject": subject, "content": content, "attachment": attachment})
#     plain_message = strip_tags(html_message)

#     for user_email in users:
#         # email = EmailMultiAlternatives(subject, plain_message, to=[user_email])
#         email = EmailMultiAlternatives(subject, plain_message, to=list(users))
#         email.attach_alternative(html_message, "text/html")
#         if template.attachment:
#             email.attach_file(template.attachment.path)
#         email.send()

#     return redirect('email_template_list')

def send_bulk_email(request, template_id):
    template = get_object_or_404(WaitlistEmailTemplate, id=template_id)
    users = WaitlistUser.objects.values_list("email", flat=True)

    if not users:
        messages.warning(request, "No users found in the waitlist.")
        return redirect('email_template_list')

    subject = template.subject
    content = template.content
    attachment = template.attachment
    html_message = render_to_string("emails/send_email.html", {"subject": subject, "content": content, "attachment": attachment})
    plain_message = strip_tags(html_message)

    try:
        email = EmailMultiAlternatives(subject, plain_message, to=list(users))
        email.attach_alternative(html_message, "text/html")
        if attachment:
            email.attach_file(attachment.path)
        email.send()

        messages.success(request, f"Email successfully sent to {len(users)} users.")
    except Exception as e:
        messages.error(request, f"Error sending email: {e}")

    return redirect('email_template_list')


def actions(request):
    """Allow staff to view all waitlist users."""
    users = WaitlistUser.objects.all().order_by('-joined_at')
    return render(request, "staff/actions.html", {"users": users})
