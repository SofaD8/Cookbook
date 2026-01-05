from django.apps import AppConfig


class CookbookConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cookbook"

    def ready(self):
        import cookbook.signals
