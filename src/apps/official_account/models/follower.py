import json

from django.db import models


class Follower(models.Model):
    id = models.BigAutoField(primary_key=True)
    unionid = models.CharField(max_length=32)
    openid = models.CharField(max_length=32)
    user_info = models.TextField(default='{}')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    wechat_account = models.ForeignKey('OpenWeChatAccount',
                                       on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '关注用户'
        verbose_name_plural = '关注用户列表'
        unique_together = ['wechat_account', 'openid']

    @property
    def nickname(self):
        return json.loads(self.user_info)['nickname']
