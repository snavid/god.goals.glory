from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import datetime
from django.contrib.auth.decorators import user_passes_test
import smtplib, random
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from .forms import UserRegistrationForm, CustomUserForm
from staff.forms import OrderForm
from .models import CustomUser
from staff.models import Product, Testimonial, OrderItem, Order
import datetime
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta


User = get_user_model()

# Register view: Handles user registration and sending activation email
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            # user.is_active = False
            user.save()

            # Send activation email
            current_site = get_current_site(request)
            mail_subject = "Activate your user account"
            message = render_to_string("emails/activate_account.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http',
                'current_year': datetime.datetime.now().year,
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = "html"  # Ensure the email content type is HTML
            email.send()

            messages.success(
                request, f"Dear {user.first_name}, we have sent an activation link to your email. Please check your email to complete registration. You cannot proceed without that link")
            return redirect('land')  # Redirect to login page
    else:
        form = UserRegistrationForm()

    return render(request, 'yuzzaz/register.html', {'form': form})


# Activate view: Handles the account activation via the token
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for confirming your email. You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid.")
        return redirect('land')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = CustomUser.objects.filter(email=username).first()
        if user and user.check_password(password):
            auth_login(request, user)
            messages.success(request, "You have successfully logged in.")

            if user.is_staff:
                return redirect('actions')  # Updated to use namespace
            return redirect('homepage')

        messages.error(request, "Invalid credentials, please try again.")

    return render(request, 'yuzzaz/login.html')

def homepage(request):
    user = request.user  # Get the user object
    has_pending_order = False  # Default value

    if user.is_authenticated:
        has_pending_order = Order.objects.filter(user=user, is_completed=False).exists()

    context = {
        'products': Product.objects.all().order_by('-created_at'),
        'latest_products': Product.objects.order_by('-created_at')[:6],  # Get last 6 products
        'testimonials': Testimonial.objects.all().order_by('-created_at'),
        'user': user,
        'has_pending_order': has_pending_order
    }

    return render(request, 'yuzzaz/homepage.html', context)

def land(request):
    context = {
    }
    return render(request, 'yuzzaz/land.html', context)

def logout(request):
    auth_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')


@login_required
def profile(request):
    user = request.user  # Get the current logged-in user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')  # Redirect to the same page
    else:
        form = CustomUserForm(instance=user)

    return render(request, 'yuzzaz/profile.html', {
        'user': user,
        'form': form,
        'has_pending_order': Order.objects.filter(user=request.user, is_completed=False).exists()

    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    products = list(Product.objects.all())
    ordered_date = timezone.now()
    order_ready_date = ordered_date + timedelta(days=2)
    delivered_date = ordered_date + timedelta(days=1)
    user = request.user
    has_pending_order = False  # Default value
    if user.is_authenticated:
        has_pending_order = Order.objects.filter(user=user, is_completed=False).exists()

    context = {
        'product': product,
        'latest_products': Product.objects.order_by('-id')[:6],  # Get last 6 products
        'testimonials': Testimonial.objects.all().order_by('-created_at'),
        'user': request.user,
        'random_products' : random.sample(products, min(len(products), 4)),  # Select up to 4 random items
        'ordered_date': ordered_date,
        'order_ready_date': order_ready_date,
        'delivered_date': delivered_date,
        'has_pending_order': has_pending_order

    }
    return render(request, 'yuzzaz/shop.html', context)




@login_required
def update_cart_item_size(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__is_completed=False)
    if request.method == 'POST':
        new_size = request.POST.get('size')

        if new_size and new_size != item.sizes:  # Update only if the size is different
            item.sizes = new_size
            item.save()

    return redirect('cart')



def is_staff(user):
    return user.is_staff  # Only allow staff members

@user_passes_test(is_staff)
@login_required
def update_stage(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_stage = request.POST.get('stage')

    if new_stage and new_stage != order.stage:
        order.stage = new_stage
        order.save()

        # Send email notification when order is updated
        if new_stage == "Ready":
            send_oda_email(order, "Your order is now ready!", "emails/order_ready_email.html")
        elif new_stage == "Delivered":
            send_oda_email(order, "Your order has been delivered!", "emails/order_delivered_email.html")

        messages.success(request, f"Order stage updated to {new_stage}, and user has been notified.")
    else:
        messages.error(request, "Invalid stage selection.")

    return redirect('orders_list')


def send_oda_email(order, subject, template_name):
    user = order.user
    order_items = [
        {
            'name': item.product.name,
            'quantity': item.quantity,
            'total': item.quantity * item.product.price,
            'size': item.sizes,
        }
        for item in order.items.all()
    ]

    html_message = render_to_string(template_name, {
        'user': user,
        'order': order,  # Add this line
        'order_items': order_items,
        'total_price': order.total_price,
        'address': order.address,
        'current_year': datetime.datetime.now().year,
    })
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(subject, plain_message, to=[user.email])
    email.attach_alternative(html_message, "text/html")
    email.send()



@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, is_completed=False).first()
    completed_orders = Order.objects.filter(user=request.user, is_completed=True).order_by('-id')[:5]
    if order and not order.items.exists():
        order.delete()
        order = None

    return render(request, 'yuzzaz/cart.html', {
        'order': order,
        'has_pending_order': order is not None,
        'completed_orders': completed_orders,
        'has_completed_orders': completed_orders.exists(),
    })


@login_required
def order_confirmation (request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'yuzzaz/order-confirmation.html', {'order': order})



@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, is_completed=False).first()

    if not order:
        return redirect('cart')  # Redirect if no pending order exists
        
    order_items = []
    total_price = 0

    for item in order.items.all():
                item_total = item.quantity * item.product.price  # Calculate item total
                total_price += item_total
                order_items.append({
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'price': item.product.price,
                    'total': item_total,
                    'sub_total': item_total,
                    'size': item.sizes,  # Include item size
                })

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)  # Bind form to existing order
        if form.is_valid():
            form.instance.is_completed = True  # Mark order as completed
            form.save()

            # Get updated order details
            user = request.user
            address = form.cleaned_data['address']
            payment_method = form.cleaned_data['payment_method']

            order_items = []
            total_price = 0
            
            for item in order.items.all():
                item_total = item.quantity * item.product.price  # Calculate item total
                total_price += item_total
                order_items.append({
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'price': item.product.price,
                    'total': item_total,
                    'sub_total': item_total,
                    'size': item.sizes,  # Include item size
                })

            # Render email template with shipping details
            html_message = render_to_string("emails/order_email.html", {
                'user': user,
                'order_items': order_items,
                'total_price': total_price,
                'address': address,
                'payment_method': payment_method,
                'current_year': datetime.datetime.now().year,

                'stage': order.stage,  # ✅ Include order stage
                'id': order.id,  # ✅ Include order ID
            })

            plain_message = strip_tags(html_message)
            subject = "🛒 Your Order Confirmation"
            email = EmailMultiAlternatives(subject, plain_message, to=[user.email])
            email.attach_alternative(html_message, "text/html")
            email.send()

            messages.success(request, "Order placed successfully, and confirmation email sent!")
            return redirect('cart')
    else:
        form = OrderForm(instance=order)  # Pre-fill form with existing order data

    return render(request, 'yuzzaz/checkout.html', {
        'order': order,
        'form': form,
        'has_pending_order': Order.objects.filter(user=request.user, is_completed=False).exists()
    })


@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('homepage')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    sizes = request.POST.get("sizes", "M")  # Default size if not selected

    if not sizes:
        messages.error(request, "Please select a size before adding to cart.")
        return redirect("product_detail", product_id=product.id)

    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        sizes=sizes,
        defaults={'price': product.price, 'quantity': 1}
    )

    if not created:
        order_item.quantity += 1

    order_item.price = order_item.quantity * product.price  # Ensure correct calculation
    order_item.save()

    # **Recalculate total cart price**
    order.total_price = sum(item.price for item in order.items.all())
    order.save()

    return redirect('cart')


@login_required
def increase_quantity(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)

    order_item.quantity += 1
    order_item.price = order_item.quantity * order_item.product.price
    order_item.save()

    # **Update total cart price**
    order_item.order.total_price = sum(item.price for item in order_item.order.items.all())
    order_item.order.save()
    messages.success(request, "Order item increased by 1")
    return redirect('cart')


@login_required
def decrease_quantity(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)

    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.price = order_item.quantity * order_item.product.price
        order_item.save()
    else:
        order_item.delete()  # Remove item if quantity is zero

    # **Update total cart price**
    order = order_item.order
    order.total_price = sum(item.price for item in order.items.all()) if order.items.exists() else 0
    order.save()
    messages.success(request, "Order item decreased by 1")
    return redirect('cart')


@login_required
def remove_cart_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    order = order_item.order  # store reference before deletion
    order_item.delete()

    # Recalculate total cart price after item is removed
    order.total_price = sum(item.price for item in order.items.all()) if order.items.exists() else 0
    order.save()
    messages.success(request, "Order item was removed")
    return redirect('cart')



@login_required
def send_order_email(request):
    user = request.user
    order = Order.objects.filter(user=user, is_completed=False).first()

    if not order:
        messages.error(request, "No pending orders found.")
        return redirect('cart')

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            payment_method = form.cleaned_data['payment_method']

            order_items = []
            total_price = 0

            for item in order.items.all():
                item_total = item.quantity * item.product.price  # Calculate item total
                total_price += item_total
                order_items.append({
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'price': item.product.price,
                    'total': item_total,
                    'size': item.sizes,  # Include item size
                })

            # Render email template with shipping details
            html_message = render_to_string("yuzzaz/order_email.html", {
                'user': user,
                'order_items': order_items,
                'total_price': total_price,
                'address': address,
                'payment_method': payment_method,
                'current_year': datetime.datetime.now().year,
            })

            plain_message = strip_tags(html_message)
            subject = "🛒 Your Order Confirmation"
            email = EmailMultiAlternatives(subject, plain_message, to=[user.email])
            email.attach_alternative(html_message, "text/html")
            email.send()

            # ✅ Mark the order as completed
            order.is_completed = True
            order.save()

            messages.success(request, "Order confirmation email sent successfully.")
            return redirect('homepage')
        else:
            messages.error(request, "Please provide a valid shipping address.")

    return redirect('cart')

def story(request):
    users = list(User.objects.all())
    yuzzaz = User.objects.all()
    random_users = random.sample(users, min(8, len(users)))
    return render(request, 'yuzzaz/story.html', {'users': random_users, 'yuzzaz': yuzzaz})