from rest_framework import serializers
from django.db import transaction
from apps.roles.models import BaseUser


from .models import Order, OrderItem, Product, Category, Cart, CartItem, ProductImage


class CategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("genre", "about")


class ProductSerializer(serializers.ModelSerializer):
    class ProductImageSerializer(serializers.ModelSerializer):
        product = serializers.StringRelatedField()

        class Meta:
            model = ProductImage
            fields = ("id", "image", "product")

    category = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "name",
            "slug",
            "description",
            "unit_price",
            "inventory",
            "dt_created",
            "dt_modified",
            "images",
        )


class CartItemSerializer(serializers.ModelSerializer):
    class ProductCartSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ["id", "name", "unit_price"]
            read_only_fields = (
                "unit_price",
                "name",
            )

    sum_of = serializers.SerializerMethodField("get_sum_of")
    product = ProductCartSerializer()

    class Meta:
        model = CartItem
        fields = ("id", "quantity", "product", "sum_of")

    def get_sum_of(self, cart_item: "CartItem") -> serializers.IntegerField:
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    checkout = serializers.SerializerMethodField()
    num_of_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "dt_created", "items", "checkout", "num_of_items")
        read_only_fields = ("id",)

    def get_checkout(self, cart: Cart) -> serializers.IntegerField:
        return sum(
            [item.product.unit_price * item.quantity for item in cart.items.all()]
        )

    def get_num_of_items(self, cart: Cart) -> serializers.IntegerField:
        return len(cart.items.all())


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "quantity",
        ]


class AddCartItemSerilizer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "id", "product", "quantity"

    def create(self, validated_data):
        cart_id = self.context.get("cart_pk")
        product = validated_data.get("product")
        quantity = validated_data.get("quantity")

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)
        self.instance = cart_item
        return cart_item


class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "unit_price"]


class OrderItemSeriliazer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "order",
            "quantity",
            "unit_price",
        ]


class OrderSeriliazer(serializers.ModelSerializer):
    items = OrderItemSeriliazer(many=True)
    customer_email = serializers.StringRelatedField(source="customer")

    class Meta:
        model = Order
        fields = ["id", "customer_email", "status", "dt_created", "items"]
        read_only_fields = ["status"]


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        try:
            if (
                Cart.objects.prefetch_related("items").get(id=cart_id).items.count()
                == 0
            ):
                print("was empty")
                raise serializers.ValidationError("cart is empty")

        except Cart.DoesNotExist:
            raise serializers.ValidationError("cart not found")

        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            customer = BaseUser.objects.get(id=user_id)

            order = Order()
            order.customer = customer
            order.save()

            customer_cart_items = CartItem.objects.select_related("product").filter(
                cart_id=cart_id
            )

            bulk_cart_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity,
                )
                for item in customer_cart_items
            ]

            OrderItem.objects.bulk_create(bulk_cart_items)

            Cart.objects.get(id=cart_id).delete()

            return order
