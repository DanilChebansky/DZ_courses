from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, AnotherUserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):

        if self.action == "create":
            self.serializer_class = UserSerializer
        elif self.action == "retrieve" and self.request.user == super().get_object():
            self.serializer_class = UserSerializer
        else:
            self.serializer_class = AnotherUserSerializer
        return self.serializer_class


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_way")
    ordering_fields = ("pay_date",)
