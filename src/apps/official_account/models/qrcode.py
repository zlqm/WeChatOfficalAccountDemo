from urllib.parse import quote
import json


from django.db import models


class QRCode(models.Model):
    class Type:
        QR_SCENE = 'QS'
        QR_STR_SCENE = 'QSS'
        QR_LIMIT_SCENE = 'QLS'
        QR_LIMIT_STR_SCENE = 'QLSS'

    TypeChoices = (
        (Type.QR_SCENE, '临时整型参数值'),
        (Type.QR_STR_SCENE, '临时的字符串参数值'),
        (Type.QR_LIMIT_SCENE, '永久的整数型参数值'),
        (Type.QR_LIMIT_STR_SCENE, '永久的字符串参数值'),
    )
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=12, choices=TypeChoices)
    event_value = models.CharField(max_length=64)
    content = models.CharField(max_length=2048, default='{}')
    wechat_account = models.ForeignKey('OpenWeChatAccount',
                                       on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '事件二维码'
        verbose_name_plural = '事件二维码列表'
        unique_together = ['wechat_account', 'type', 'event_value']

    def sync_with_wechat(self):
        resp_json = self.wechat_account.wx_app.create_qrcode(self.event_value)
        self.content = json.dumps(resp_json)

    @property
    def url(self):
        return 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=' + \
                quote(json.loads(self.content).get('ticket'))
