from django.apps import AppConfig


class PoolConfig(AppConfig):
    name = 'pool'
    verbose_name = 'Target Pool'

    def ready(self):
        import pool.signals
