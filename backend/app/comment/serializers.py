from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    NO NEED TO SEND PRODUCT ID
    NO NEED TO SEND USER ID
    PROVIDES BY CONTEXT
    """
    class Meta:
        model=Comment
        fields = ('id', 'content', 'datetime_created', 'commentor', 'product')
        read_only_fields = ('product', 'commentor')

    def create(self, validated_data):
        commentor  = self.context.get('request').user
        product_pk = self.context.get('product_pk')
        comment    = Comment.objects.create(
                                        commentor=commentor,
                                        product_id=product_pk,
                                        **validated_data
                                    )
        return comment