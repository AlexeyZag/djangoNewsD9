from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'

    def ready(self):
        import news.signals

        """from .tasks import send_mails
        from .scheduler import appointment_scheduler
        print('started')

        appointment_scheduler.add_job(
            id='send mails',
            func=send_mails,
            trigger='interval',
            seconds=5
        )
        appointment_scheduler.start()"""
