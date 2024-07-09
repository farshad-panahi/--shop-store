from django.contrib import admin

from .models import (
    Category, 
    Product,
    Order,
    OrderItem,
    TempCart,
    TempCartItem
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('genre', 'about')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
