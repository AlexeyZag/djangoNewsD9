from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from django.template.loader import render_to_string
from news.models import Post
from django.core.mail import mail_admins, send_mail

# Create your views here.


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'add_article.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Post(
            headline=request.POST['headline'],
            text=request.POST['text'],
        )
        appointment.save()

        send_mail(
            subject=f'{appointment.headline}',
            # имя клиента и дата записи будут в теме для удобства
            message=appointment.text,  # сообщение с кратким описанием проблемы
            from_email='peterbadson@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=['alex8.8@mail.ru']  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )

        return redirect('')