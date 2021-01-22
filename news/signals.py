from django.db.models.signals import post_save, pre_save, m2m_changed, post_init
from django.core.signals import request_finished
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Author, Post, Category, PostCategory
from django.template.loader import render_to_string
from .forms import PostForm
import time

@receiver(m2m_changed, sender=PostCategory)
def notify_managers_appointment(sender, instance, **kwargs):
    new_post_categories = Post.objects.order_by('-id')[0].categories.all()

    list_of_users = []
    for tag in new_post_categories:
        for i in range(len(Category.objects.get(tag=tag).subscribers.all())):
            list_of_users.append(Category.objects.get(tag=tag).subscribers.all()[i].email)
    link_id = instance.id
    link = f'http://127.0.0.1:8000/news/{link_id}'
    html_content = render_to_string(
        '../templates/appointment.html',
        {
            'appointment': instance, 'link': link
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'{instance.headline}',
        body=f'{instance.text}',
        from_email='zagaalexey@yandex.ru',
        to= list_of_users
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
