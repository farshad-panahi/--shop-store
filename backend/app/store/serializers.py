from rest_framework import serializers


from .models import (
    Product,
    Category
)

class CategorySerilizer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields= (
            'genre', 'about'
        )


class ProductSerializer(serializers.ModelSerializer):

    category  = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name= 'category-detail'
    )
    
    class Meta:
        model  = Product
        fields = (
            'category', 'name', 'slug', 'description', 'unit_price', 'inventory', 'date_created', 'date_modified'
        )
