from django.contrib import admin
from .models import Product, Category, ProductImage, ProductPromotion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductPromotionInline(admin.TabularInline):
    model = ProductPromotion
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_best_seller', 'created_at')
    list_filter = ('is_best_seller', 'category')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductPromotionInline]

from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('customer_name', 'content')

from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'total_price', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'id')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'updated_at')
