from django.db import models
import jinja2

from OpenWeChat.messages import reply

CONTENT_SCHEMA = {
    'type': 'array',
    'minItems': 1,
    'maxItems': 3,
    'items': {
        'oneOf': [{
            'type': 'object',
            'properties': {
                'type': 'text',
                'content': {
                    'type': 'string'
                },
            },
            'required': ['type', 'content']
        }, {
            'type': 'object',
            'properties': {
                'type': 'media_image',
                'media_id': {
                    'type': 'string'
                }
            },
            'required': ['type', 'media_id']
        }, {
            'type': 'object',
            'properties': {
                'type': 'template_image',
                'bg_img_url': {
                    'type': 'string',
                },
                'qrcode_content': {
                    'type': 'string'
                },
                'elements': {
                    'type': 'array',
                    'items': {
                        'type': 'string',
                        'enum': ['nickname', 'avatar', 'qrcode'],
                        'minItems': 1,
                        'maxItems': 3,
                        'uniqueItems': True
                    }
                }
            }
        }]
    }
}


class ReplyTemplate(models.Model):
    class ReplyType:
        TEXT = 'text'
        IMAGE = 'image'
        IMAGE_TEMPLATE = 'template_image'

    ReplyTypeChoices = (
        (ReplyType.TEXT, '文本'),
        (ReplyType.IMAGE, '图片'),
        (ReplyType.IMAGE_TEMPLATE, '图片模板'),
    )

    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=32, choices=ReplyTypeChoices)
    content = models.TextField()
    wechat_account = models.ForeignKey('OpenWeChatAccount',
                                       blank=False,
                                       null=False,
                                       related_name='reply_templates',
                                       on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '回复模板'
        verbose_name_plural = '回复模板列表'

    def __str__(self):
        return '回复模板-{}'.format(self.description)

    def generate_reply(self, request_message, **context):
        if self.type == self.ReplyType.TEXT:
            try:
                msg_content = jinja2.Template(self.content).render(**context)
            except jinja2.TemplateSyntaxError:
                msg_content = self.content
            return reply.TextResponse(request_message, msg_content)
        return reply.BlankResponse()
