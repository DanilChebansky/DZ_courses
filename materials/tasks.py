from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from config import settings
from django.core.mail import send_mail

from users.models import Subscription

from celery import shared_task


@shared_task
def send_updating_mail(course):
    """Отправляет сообщение всем подписчикам курса при его обновлении (то есть, изменении)"""
    subscriptions = Subscription.objects.filter(course=course)
    try:
        send_mail(
            subject='Обновление курса',
            message=f'Курс {course.name} обновлен',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscription.user.email for subscription in subscriptions]
        )
    except Exception as e:
        print(str(e))


@shared_task
def deactivate():
    user = get_user_model()
    today = timezone.now().today()
    users = user.objects.filter(last_login__lte=today - timedelta(days=30), is_active=True, is_superuser=False, is_staff=False)
    for lazy_user in users:
        lazy_user.is_active = False
        lazy_user.save()
