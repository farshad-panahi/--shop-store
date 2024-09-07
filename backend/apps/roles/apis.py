from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer
from .models import Customer
from rest_framework.parsers import MultiPartParser
from rest_framework.renderers import AdminRenderer


class CustomerViewset(ModelViewSet):
    http_method_names = ("get", "post", "patch")
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = (IsAdminUser,)
    parser_classes = [
        MultiPartParser,
    ]
    renderer_classes = [
        AdminRenderer,
    ]

    @action(detail=False, methods=("GET", "PUT"), permission_classes=(IsAuthenticated,))
    def me(self, request):
        customer = get_object_or_404(Customer, user_id=request.user.id)

        if request.method == "GET":
            ser = CustomerSerializer(customer)
            return Response(ser.data, status=status.HTTP_200_OK)

        elif request.method == "PUT":
            ser = CustomerSerializer(customer, request.data)
            ser.is_valid(raise_exception=True)
            ser.save()

            return Response(ser.data, content_type="application/json")
