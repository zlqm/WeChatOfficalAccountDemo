from OpenWeChat.consts import EventType
from django.db import models


class EventReply(models.Model):
    # 和微信回调接口的事件不是一一对应
    EventTypeChoices = (
        ('text', '文本关键词'),
        (EventType.SCAN.value, '事件二维码'),
        (EventType.SUBSCRIBE.value, '关注公中号'),
        (EventType.CLICK.value, '菜单点击'),
    )

    description = models.CharField(max_length=1024)
    event = models.CharField(max_length=16,
                             null=False,
                             blank=False,
                             choices=EventTypeChoices)
    value = models.CharField(max_length=128)
    reply_template = models.ForeignKey('ReplyTemplate',
                                       blank=False,
                                       null=False,
                                       on_delete=models.DO_NOTHING)
    wechat_account = models.ForeignKey('OpenWeChatAccount',
                                       blank=False,
                                       null=False,
                                       related_name='event_replies',
                                       on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '回复规则'
        verbose_name_plural = '回复规则列表'

    def __str__(self):
        return '回复规则-{}'.format(self.description)
