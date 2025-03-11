# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('staff_dashboard', views.staff_dashboard, name='staff_dashboard' ),
    path('add/', views.add_product, name='add_product'),
    path('update/<int:pk>/', views.update_product, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('add-rating/<int:product_id>/', views.add_rating, name='add_rating'),
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    path('review_rate/<int:product_id>/', views.review_rate, name='review_rate'),
    path('add-testimonial/', views.add_testimonial, name='add_testimonial'),
    
]
