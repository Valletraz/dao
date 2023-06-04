from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import truncatewords

from .models import Post


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):

    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category=instance.category.name
    ).values_list('email', flat=True)

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
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()



# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from .models import Product
#
#
# @receiver(post_save, sender=Product)
# def product_created(instance, **kwargs):
#     print('Создан товар', instance)