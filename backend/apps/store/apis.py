from requests import Response
from rest_framework import mixins
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .paginations import ProductPagination
from .models import Category, Order, OrderItem, Product, Cart, CartItem
from .serializers import (
    AddCartItemSerilizer,
    CartItemSerializer,
    CategorySerilizer,
    OrderCreateSerializer,
    OrderSeriliazer,
    ProductSerializer,
    CartSerializer,
    UpdateCartItemSerializer,
)
from drf_spectacular.utils import extend_schema
from django.db.models import Prefetch


@extend_schema(tags=["Products"])
class ProductViewset(ReadOnlyModelViewSet):
    """
    products detail = /{product_id}
    product all comments related = /{product_id}/comments
    product comment detail = /{product_id}/comments/{comment_id}
    """

    serializer_class = ProductSerializer
    queryset = Product.objects.select_related("category")
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        "category_id",
    ]
    ordering_fields = ["unit_price", "inventory"]
    search_fields = ["name", "category__genre"]
    pagination_class = ProductPagination


@extend_schema(tags=["Categories"])
class CategoryViewset(ModelViewSet):
    """
    CATEGORY VIEW NEEDS PK FOR DETAIL
    """

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerilizer
    queryset = Category.objects.prefetch_related("products")


@extend_schema(tags=["Carts"])
class CartViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related("items__product")


@extend_schema(tags=["Cart items"])
class CartItemViewset(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        cart_pk = self.kwargs.get("cart_pk")
        return CartItem.objects.select_related("product", "cart").filter(
            cart_id=cart_pk
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerilizer
        if self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["cart_pk"] = self.kwargs.get("cart_pk")
        return context


@extend_schema(tags=["Orders"])
class OrderViewSet(ModelViewSet):
    serializer_class = OrderSeriliazer
    http_method_names = ["get", "patch", "post", "delete", "head", "options"]

    def get_queryset(self):
        queryset = Order.objects.prefetch_related(
            Prefetch("items", queryset=OrderItem.objects.select_related("product"))
        ).select_related("customer")

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(customer_id=self.request.user.id)

    def get_serializer_class(self):
        default_serilizer = super().get_serializer_class()

        if self.request.method == "POST":
            return OrderCreateSerializer
        return default_serilizer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def create(self, request, *args, **kwargs):
        customer_order = OrderCreateSerializer(
            data=request.data, context={"user_id": self.request.user.id}
        )

        customer_order.is_valid(raise_exception=True)
        customer_order_serilizer = customer_order.save()
        serializer = OrderSeriliazer(customer_order_serilizer)
        return Response(serializer.data)

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [
                IsAdminUser(),
            ]
        return [
            IsAuthenticated(),
        ]
