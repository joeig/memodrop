from django.apps import AppConfig


class BraindumpConfig(AppConfig):
    name = 'braindump'

    def ready(self):
        import braindump.signals
