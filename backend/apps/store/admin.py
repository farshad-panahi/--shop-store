from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem, Cart, CartItem, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ("genre", "about")


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )

    inlines = (ProductImageInline,)

    # def list_images(self, obj):
    #     images = [
    #         pi.image.url
    #         for pi in
    #         ProductImage.objects.filter(product_id=obj.id)
    #         ][0]
    #     panel = ""
    #     # for url in images[0]:
    #     panel +='\n'.join('<img src="{}" style="max-width:100px; max-height:100px"/>'.format(images)
    #                       )

    # return format_html(panel)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    class CartItemInline(admin.TabularInline):
        """
        CART ITEMS INLINE
        """

        model = CartItem
        fields = ("id", "cart", "product", "quantity")
        extra = 0
        min_num = 1

    list_display = ("id", "dt_created")
    inlines = (CartItemInline,)
