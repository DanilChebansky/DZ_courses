from rest_framework.serializers import ModelSerializer

from materials.validators import PayValidator
from users.models import User, Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        validators = [PayValidator(field1="course", field2="lesson")]


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "is_active", "password", "payments")


class AnotherUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "phone", "city", "is_active")
