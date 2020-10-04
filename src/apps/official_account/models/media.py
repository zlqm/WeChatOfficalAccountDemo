from OpenWeChat.consts import MediaType
from django.db import models


class Media(models.Model):

    TypeChoices = (
        (MediaType.IMAGE, '图片'),
        (MediaType.VOICE, '声音'),
        (MediaType.VIDEO, '视频'),
        (MediaType.THUMB, '缩略图'),
    )

    description = models.CharField(max_length=2048)
    type = models.CharField('资源类型', max_length=32, choices=TypeChoices)
    media_id = models.CharField(max_length=1024)
    is_active = models.BooleanField(default=True)
    wechat_account = models.ForeignKey('OpenWeChatAccount',
                                       on_delete=models.DO_NOTHING)
    extra_data = models.TextField(null=False, blank=False, default='{}')
    create_time = models.PositiveIntegerField()
    update_time = models.PositiveIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'wechat_media'
