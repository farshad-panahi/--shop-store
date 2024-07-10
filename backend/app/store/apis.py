from rest_framework                import mixins
from rest_framework.viewsets       import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters        import OrderingFilter, SearchFilter

from .permissions import IsAdminOrReadOnly

from .paginations                  import ProductPagination
from .models        import (
                            Category,
                            Product,
                            Cart,
                            CartItem
                        )
from .serializers   import (
                            AddCartItemSerilizer,
                            CartItemSerializer,
                            CategorySerilizer,
                            ProductSerializer,
                            CartSerializer,
                        )


class ProductViewset(ReadOnlyModelViewSet):
    """
    PRODUCTS VIEW NEEDS PK FOR DETAIL
    """
    serializer_class = ProductSerializer
    queryset         = Product.objects.select_related('category')
    filter_backends  = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category_id',]
    ordering_fields  = ['unit_price', 'inventory']
    search_fields    = ['name', 'category__genre']
    pagination_class = ProductPagination


class CategoryViewset(ModelViewSet):
    """
    CATEGORY VIEW NEEDS PK FOR DETAIL
    """
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerilizer
    queryset         = Category.objects.prefetch_related('products')


class CartViewset(
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet
                ):
    
    serializer_class = CartSerializer
    queryset         = Cart.objects.prefetch_related('items__product')


class CartItemViewset(ModelViewSet):
    
    def get_queryset(self):
        cart_pk = self.kwargs.get('cart_pk')
        return CartItem.objects.select_related('product', 'cart').filter(cart_id = cart_pk)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerilizer
        return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['cart_pk']= self.kwargs.get('cart_pk')

        return context