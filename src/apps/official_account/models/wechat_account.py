from django.db import models

from OpenWeChat.app import OfficialAccount
from OpenWeChat.auth import Auth

from .cache import auth_cache

class OpenWeChatAccount(models.Model):
    ACCOUNT_TYPE = [
        ('official_account', '公众号'),
        ('mini_program', '小程序'),
    ]

    appid = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    secret = models.CharField(max_length=256)
    account_type = models.CharField(max_length=32, choices=ACCOUNT_TYPE)
    callback_token = models.CharField(max_length=32)

    class Meta:
        verbose_name = '微信开放平台帐号'
        verbose_name_plural = '微信开放平台帐号列表'

    def __str__(self):
        return '平台帐号-{}'.format(self.name)

    @property
    def wx_auth(self):
        global auth_cache
        return Auth(self.appid, self.secret, auth_cache, self.callback_token)

    @property
    def wx_app(self):
        if self.account_type == 'official_account':
            return OfficialAccount(self.wx_auth)
