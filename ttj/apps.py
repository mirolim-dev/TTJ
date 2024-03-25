from django.apps import AppConfig


class TtjConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ttj'

    def ready(self) -> None:
        from ttj import signals
        return super().ready()