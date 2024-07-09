from rest_framework.viewsets       import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters        import OrderingFilter, SearchFilter

from .paginations                  import ProductPagination
from .models        import (
                            Category,
                            Product
                        )
from .serializers   import (
                            CategorySerilizer,
                            ProductSerializer,
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


class CategoryViewset(ReadOnlyModelViewSet):
    """
    CATEGORY VIEW NEEDS PK FOR DETAIL
    """
    serializer_class = CategorySerilizer
    queryset         = Category.objects.prefetch_related('products')