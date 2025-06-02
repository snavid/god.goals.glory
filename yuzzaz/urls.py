from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('homepage/', views.homepage, name='homepage'),
    path('story/', views.story, name='story'),
    path('', views.land, name='land'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('login/', views.login, name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete_order'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('send/order/email', views.send_order_email, name='send_order_email'),
    path('update_cart_item_size/<int:item_id>/', views.update_cart_item_size, name='update_cart_item_size'),
    path('update_stage/<int:order_id>/', views.update_stage, name='update_stage'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='yuzzaz/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='yuzzaz/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='yuzzaz/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='yuzzaz/password_reset_complete.html'), name='password_reset_complete'),
    
]