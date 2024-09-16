from rest_framework_nested import routers
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    # SpectacularRedocView,
    SpectacularSwaggerView,
)


from apps.store.apis import (
    CartItemViewset,
    CartViewset,
    ProductViewset,
    CategoryViewset,
    OrderViewSet,
)
from apps.comment.apis import CommentViewset
# from apps.roles.apis import CustomerViewset


apps_router = routers.DefaultRouter()
apps_router.register("products", ProductViewset, basename="product")
apps_router.register("category", CategoryViewset, basename="category")
apps_router.register("carts", CartViewset, basename="cart")
apps_router.register("orders", OrderViewSet, basename="order")
product_router = routers.NestedDefaultRouter(
    apps_router,
    "products",
    lookup="product",
)
product_router.register("comments", CommentViewset, basename="product-comment")
cart_items_router = routers.NestedDefaultRouter(apps_router, "carts", lookup="cart")
cart_items_router.register("items", CartItemViewset, basename="cart-items")


apps_urls = apps_router.urls + product_router.urls + cart_items_router.urls


urlpatterns = [
    # docs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # path("", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("", include(apps_urls)),
                path("auth/", include("djoser.urls.base")),
                path("auth/", include("djoser.urls.jwt")),
            ]
        ),
    ),
]
