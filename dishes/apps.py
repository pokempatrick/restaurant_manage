from django.apps import AppConfig


class DishesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dishes'

    def ready(self) -> None:
        import dishes.signals
