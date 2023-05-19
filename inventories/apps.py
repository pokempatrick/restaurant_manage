from django.apps import AppConfig


class InventoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventories'

    def ready(self) -> None:
        import inventories.signals
