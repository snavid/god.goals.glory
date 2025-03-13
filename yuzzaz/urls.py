from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('homepage/', views.homepage, name='homepage'),
    path('', views.land, name='land'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('login/', views.login, name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    # path('products/', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('delete_order/<int:pk>/', views.delete_order, name='delete_order'),

    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('send/order/email', views.send_order_email, name='send_order_email'),
    # path('besa', views.besa, name='besa'),
    path('update_cart_item_size/<int:item_id>/', views.update_cart_item_size, name='update_cart_item_size'),



]