from django.shortcuts import get_object_or_404
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course
from users.models import User, Payment
from users.permissions import IsSelfUser
from users.serializers import UserSerializer, PaymentSerializer, AnotherUserSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


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
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsSelfUser]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):

        if self.action in ["create", "update", "partial_update"]:
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


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        product = create_stripe_product(course_item)
        price = create_stripe_price(payment.payment_sum, product)
        session_id, link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = link
        payment.save()
