from django.apps import AppConfig


class AdvertsApp(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adverts'

    def ready(self):
        from .signals import upload_file_task # noqa
