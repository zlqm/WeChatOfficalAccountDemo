from django.apps import AppConfig


class OfficialAccountConfig(AppConfig):
    name = 'apps.official_account'
    verbose_name = '公众号管理'

    def ready(self):
        print('ready is called')
        from . import signals
