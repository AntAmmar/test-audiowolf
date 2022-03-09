from django.apps import AppConfig


__all__ = ['ManagerApp']


class ManagerApp(AppConfig):
    name = 'manager'
    label = 'manager'

    def ready(self):
        from manager.tasks import __all__  # noqa
