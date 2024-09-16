from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import IsAuthenticatedOrReadOnly


@extend_schema(
    tags=["Comments of products"],
    parameters=[
        OpenApiParameter(
            "product_pk",
            OpenApiTypes.INT,
            description="Primary key of the product",
            location=OpenApiParameter.PATH,
        ),
        # OpenApiParameter('id', OpenApiTypes.INT, description='Primary key of the comment', location=OpenApiParameter.PATH),
    ],
)
class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self) -> list[Comment]:
        """
        FILTERING COMMENTS BY PK OF PRODUCT,
        TO DISPLAY ONLY COMMENTS OF THAT SPECIFIC PRODUCT
        """
        product_pk = self.kwargs["product_pk"]
        return Comment.objects.filter(product_id=product_pk)

    def get_serializer_context(self):
        """
        INJECTING MORE INFO FOR SERIALIZER
        """
        context = super().get_serializer_context()

        context["commentor"] = self.request.user
        context["product_pk"] = self.kwargs.get("product_pk")

        return context
