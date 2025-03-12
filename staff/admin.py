
# admin.py
from django.contrib import admin
from .models import Product, Review, Rating, Testimonial, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status', 'quantity')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product','comment')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product','stars')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty forms to display for adding new OrderItems
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('price',)  # Price is calculated, so it should be read-only

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at', 'total_price', 'is_completed')
    list_filter = ('is_completed', 'created_at', 'updated_at')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]  # Add OrderItems inline in the Order admin page

    # Customize how the total price is displayed in the admin list
    def total_price_display(self, obj):
        return f"€{obj.total_price}"
    total_price_display.short_description = 'Total Price'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')
    list_filter = ('order__is_completed', 'product')
    search_fields = ('order__id', 'product__name')

    # Customize how the price is displayed in the admin list
    def price_display(self, obj):
        return f"€{obj.price}"
    price_display.short_description = 'Price'

# Register models with their respective admin classes
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)