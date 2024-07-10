from rest_framework_nested import routers
from django.urls    import include, path

from .apis          import CartItemViewset, CartViewset, ProductViewset, CategoryViewset
from ..comment.apis import CommentViewset

#TODO ADD CART ITEMS ROUTER HERE WHEN DONE

router = routers.DefaultRouter() 
router.register('products', ProductViewset, basename='product')
router.register('category', CategoryViewset,basename='category')
router.register('carts'   , CartViewset)

product_router = routers.NestedDefaultRouter(
                                                router,
                                                'products',
                                                lookup='product',
    )

product_router.register(
    'comments', CommentViewset, basename='product-comment'
    )

cart_items_router = routers.NestedDefaultRouter(
                                                router,
                                                'carts',
                                                lookup='cart',
    )
cart_items_router.register('items', CartItemViewset, basename='cart-items')



urlpatterns =   router.urls \
                + product_router.urls \
                + cart_items_router.urls 