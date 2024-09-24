from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="testcase@ya.ru")
        self.course = Course.objects.create(name="English course")
        self.lesson = Lesson.objects.create(
            name="First english lesson", course=self.course, owner=self.user
        )

        self.moder = User.objects.create(email="moder@ya.ru")
        moder_group, created = Group.objects.get_or_create(name="moderator")
        self.moder.groups.add(moder_group)
        self.moder.save()

    def test_user_lesson_retrieve(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_user_lesson_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_create")
        data = {
            "name": "Second english lesson",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_user_lesson_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "name": "First super english lesson",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "First super english lesson")

    def test_user_lesson_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_user_lesson_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "video_url": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_moder_lesson_retrieve(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_moder_lesson_create(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("materials:lessons_create")
        data = {
            "name": "Second english lesson",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_moder_lesson_update(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "name": "First super english lesson",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "First super english lesson")

    def test_moder_lesson_delete(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_moder_lesson_list(self):
        self.client.force_authenticate(user=self.moder)
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "video_url": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="testcase@ya.ru")
        self.course = Course.objects.create(name="English course")
        self.lesson = Subscription.objects.create(course=self.course, user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_change(self):
        url = reverse("materials:subscription")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "подписка удалена")
