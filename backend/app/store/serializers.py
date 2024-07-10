from rest_framework import serializers


from .models import (
    Product,
    Category,
    Cart,
    CartItem
)

class CategorySerilizer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields= (
            'genre', 'about'
        )


TAX = 0.001


class ProductSerializer(serializers.ModelSerializer):

    category  = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name= 'category-detail'
    )
    
    class Meta:
        model  = Product
        fields = (
            'category', 'name', 'slug', 'description', 'unit_price', 'inventory', 'dt_created', 'dt_modified'
        )



class CartItemSerializer(serializers.ModelSerializer):
    class CartProductItem(serializers.ModelSerializer):
        class Meta:
            model=Product
            fields=('id','name', 'slug', 'unit_price',)

    sum_of = serializers.SerializerMethodField('get_sum_of')
    class Meta:
        model=CartItem
        fields= ('id', 'quantity','product', 'sum_of')
        
    
    def get_sum_of(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):    
    items = CartItemSerializer(many=True, read_only=True)
    checkout     = serializers.SerializerMethodField()
    num_of_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ('id', 'dt_created', 'items', 'checkout', 'num_of_items')
        read_only_fields = ('id',)

    def get_checkout(self, cart:Cart):
        return sum(
            [
                item.product.unit_price * item.quantity
                for item in cart.items.all()
            ]
        )
    
    def get_num_of_items(self, cart):
        return len(cart.items.all())


class AddCartItemSerilizer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields= 'id', 'product', 'quantity'

    def create(self, validated_data):
        cart_id  = self.context.get('cart_pk')
        product    = validated_data.get('product')
        quantity = validated_data.get('quantity')
        
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                                        cart_id=cart_id,
                                        **validated_data
                                    )
        self.instance = cart_item
        return cart_item
