from django.apps import AppConfig


class LeitorConfig(AppConfig):
    name = 'leitor'

    def ready(self):
        import leitor.signals  # noqa: F401
