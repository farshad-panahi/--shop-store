from django.contrib import admin

from .models import (
    Category, 
    Product,
    Order,
    OrderItem,
    Cart,
    CartItem
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('genre', 'about')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    
    class CartItemInline(admin.TabularInline):
        """
        CART ITEMS INLINE
        """
        model = CartItem
        fields= ('id', 'cart', 'product', 'quantity')
        extra = 0
        min_num= 1



    list_display = ('id', 'dt_created')
    inlines =(CartItemInline,)


