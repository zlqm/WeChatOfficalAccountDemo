from django.contrib import admin

from .models import (OpenWeChatAccount, ReplyTemplate, EventReply, Follower,
                     QRCode)


# Register your models here.
@admin.register(OpenWeChatAccount)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'appid', 'account_type']
    list_filter = ['account_type']


@admin.register(ReplyTemplate)
class ReplyTemplateAdmin(admin.ModelAdmin):
    list_display = ['pk', 'wechat_account', 'description', 'type']
    list_filter = ['wechat_account']


@admin.register(EventReply)
class EventReplyAdmin(admin.ModelAdmin):
    list_display = ['pk', 'wechat_account', 'description', 'event', 'value']


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'wechat_account', 'unionid', 'openid']
    list_filter = ('wechat_account', )


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ['description', 'wechat_account', 'create_time', 'url']
