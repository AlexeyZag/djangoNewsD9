from celery import shared_task
from .models import Post, Category
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import time

@shared_task
def my_job():
    tags_post_dict = {}
    tags_users_dict = {}
    list_of_posts = []
    list_of_users = []
    tags_subs = {}
    for tag in Category.objects.all():
        tags_post_dict[tag.tag] = Post.objects.filter(create_time__gt= datetime.fromtimestamp(datetime.timestamp(datetime.now()) - 604800), categories=tag)
        tags_users_dict[tag.tag] = Category.objects.get(tag=tag).subscribers.all()
        list_of_posts.append(Post.objects.filter(create_time__gt= datetime.fromtimestamp(datetime.timestamp(datetime.now()) - 604800), categories=tag))


    for tag in Category.objects.all():
        posts = tags_post_dict[tag.tag]
        users = tags_users_dict[tag.tag]
        emails = []
        for user in users:
            emails.append(user.email)
        html_content = render_to_string(
            '../templates/weekly_subscription.html',
            {
                'posts': posts, 'tag': tag.tag,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Недельная рассылка новостей',
            body='',
            from_email='zagaalexey@yandex.ru',
            to= emails
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()