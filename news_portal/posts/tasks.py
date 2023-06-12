import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from news_portal import settings
from posts.models import Subscriber, Post
from celery import shared_task


@shared_task
def new_post_notify(instance_id):
    instance = Post.objects.get(pk=instance_id)
    categories = instance.category.all()
    email_list = []

    for cat in categories:
        subscribers = Subscriber.objects.filter(category=cat)
        email_list += [subs.user.email for subs in subscribers]

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


@shared_task
def weekly_notification():
    # определить список статей за последнюю неделю
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    articles_to_send = Post.objects.filter(add_time__gte=last_week).order_by('-add_time')
    categories = set(articles_to_send.values_list('category__name', flat=True))
    email_list = []
    url = settings.SITE_URL

    for cat in categories:
        subscribers = Subscriber.objects.filter(category__name=cat)
        email_list += [subs.user.email for subs in subscribers]
    email_list = set(email_list)

    subject, from_email, to = 'Новые публикации за неделю', 'valletraz@yandex.ru', email_list

    html_content = render_to_string('weekly_update.html',
                                    {'articles_to_send': articles_to_send, 'url': url})  # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
