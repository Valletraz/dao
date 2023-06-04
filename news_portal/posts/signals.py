from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.defaultfilters import truncatewords
from django.template.loader import render_to_string

from .models import Post, PostCategory, Subscriber


# def send_notifications(instance, pk, title, email_list):
#     text_content = (
#         f'Публикация: {instance.title}\n'
#         f'Текст: {instance.text}\n\n'
#         f'Ссылка на публикацию: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Публикация: {instance.title}<br>'
#         f'Текст: {instance.text}<br><br>'
#         f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#         f'Ссылка на публикацию</a>'
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body=text_content,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=email_list,
#     )
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()


@receiver(m2m_changed, sender=PostCategory)
def post_created_email(instance, **kwargs):
    categories = instance.category.all()
    email_list = []

    for cat in categories:
        subscribers = Subscriber.objects.filter(category=cat)
        print(subscribers)
        email_list += [subs.user.email for subs in subscribers]

    # send_notifications(instance, instance.pk, instance.title, email_list)

    # emails = User.objects.filter(
    #     subscriber__category=instance.category.name
    # ).values_list('email', flat=True)
    print(email_list)

    subject = f'Новая публикация в категории {instance.category.name}'

    text_content = (
        f'Публикация: {instance.title}\n'
        f'Текст: {instance.text}\n\n'
        f'Ссылка на публикацию: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'Публикация: {instance.title}<br>'
        f'Текст: {instance.text}<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на публикацию</a>'
    )
    for email in email_list:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

# @receiver(post_save, sender=Post)
# def product_created(instance, **kwargs):
#     print('Создан товар', instance)
