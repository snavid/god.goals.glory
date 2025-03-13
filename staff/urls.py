# urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('staff_dashboard', views.staff_dashboard, name='staff_dashboard' ),

    path('add/', views.add_product, name='add_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('products_list/', views.products_list, name='products_list'),
    path("edit_product/<int:product_id>/", views.edit_product, name="edit_product"),  # Edit template
    
    path('add/', views.add_testimonial, name='add_testimonial'),
    path('delete_testimonial/<int:pk>/', views.delete_testimonial, name='delete_testimonial'),
    path('testimonials_list/', views.testimonials_list, name='testimonials_list'),
    path("edit_testimonial/<int:testimonial_id>/", views.edit_testimonial, name="edit_testimonial"),  # Edit template
    
    path('delete_order/<int:pk>/', views.delete_order, name='delete_order'),
    path('orders_list/', views.orders_list, name='orders_list'),
    path('users_list/', views.users_list, name='users_list'),


    path('staff/order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    path('add-rating/<int:product_id>/', views.add_rating, name='add_rating'),
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    path('review_rate/<int:product_id>/', views.review_rate, name='review_rate'),
    path('add-testimonial/', views.add_testimonial, name='add_testimonial'),
    path('actions/', views.actions, name='actions'),
    path("waitlist/join/", views.join_waitlist, name="join_waitlist"),
    path("waitlist/admin/", views.waitlist_admin, name="waitlist_admin"),
    path("waitlist/send-email/", views.send_bulk_email, name="send_bulk_email"),
    path('email-template/', views.email_template_list, name='email_template_list'),
    path("email-template/delete/<int:template_id>/", views.delete_template, name="delete_template"),
    path("email-template/create/", views.email_template_create, name="email_template_create"),  # New template
    path("email-template/edit/<int:template_id>/", views.email_template_edit, name="email_template_edit"),  # Edit template
    path("waitlist/send-email/<int:template_id>/", views.send_bulk_email, name="send_bulk_email"),

]
