from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    user_email = serializers.StringRelatedField(source='user')
    class Meta:
        model= Customer
        fields = ('id','user_email', 'phone', 'birth_date')
        read_only_fields='user_email',