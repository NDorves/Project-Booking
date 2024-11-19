from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking_app.user'

    def ready(self):
        import booking_app.user.signals
