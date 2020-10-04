from django.core.management.base import BaseCommand, CommandError
from apps.official_account.models import OpenWeChatAccount


class Command(BaseCommand):
    def handle(self, *args, **options):
        account_lst = OpenWeChatAccount.objects.filter(
            account_type='official_account')
        for account in account_lst:
            self.stdout.write('[appid: {}] start updating'.format(
                account.appid))
            account.wx_app.refresh_access_token()
            self.stdout.write('[appid: {}] updated'.format(account.appid))
