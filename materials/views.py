from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.paginators import CustomPagination
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from materials.tasks import send_updating_mail
from users.models import Subscription
from users.permissions import IsModer, IsOwner

from drf_yasg.utils import swagger_auto_schema

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (
                ~IsModer,
                IsOwner,
            )
        return super().get_permissions()


    def update(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        serializer = self.get_serializer(course, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            send_updating_mail.delay(course)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModer]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModer | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModer | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner, ~IsModer]


class SubscriptionAPIView(APIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [~IsModer]

    @swagger_auto_schema(operation_description="Subscription's creation", responses={201: "creation or deletion of "
                                                                                          "subscription"})
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user).filter(course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            subs_item_new = Subscription.objects.create(user=user, course=course_item)
            subs_item_new.save()
            message = "подписка добавлена"
        return Response({"message": message})
