from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as DjoserUserCreaterSrz


class CustomerCreateSerializer(DjoserUserCreaterSrz):
    # user_email = serializers.StringRelatedField(source="user")

    class Meta(DjoserUserCreaterSrz.Meta):
        fields = ("id", "email", "password")


class CustomerSerializer(DjoserUserCreaterSrz):
    class Meta(DjoserUserCreaterSrz.Meta):
        fields = (
            "id",
            "email",
        )
