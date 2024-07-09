from rest_framework_nested import routers
from django.urls    import include, path

from .apis          import ProductViewset, CategoryViewset
from ..comment.apis import CommentViewset

#TODO ADD CART ITEMS ROUTER HERE WHEN DONE

router = routers.DefaultRouter() 
router.register('products', ProductViewset, basename='product')
router.register('category', CategoryViewset,basename='category')

product_router = routers.NestedDefaultRouter(
                                                router,
                                                'products',
                                                lookup='product',
    )

product_router.register(
    'comments', CommentViewset, basename='product-comment'
    )

urlpatterns = [
    path('', include(router.urls + product_router.urls)),
    ]

