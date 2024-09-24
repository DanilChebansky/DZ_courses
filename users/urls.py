from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListAPIView, PaymentCreateAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)

router_payment = SimpleRouter()

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payments_create')
]

urlpatterns += router.urls
