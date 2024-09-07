from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        FILTERING COMMENTS BY ID OF PRODUCT,
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
