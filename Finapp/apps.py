from django.apps import AppConfig


class FinappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Finapp'

    def ready(self):
        import Finapp.signals  # Import the signals module to ensure it's loaded
