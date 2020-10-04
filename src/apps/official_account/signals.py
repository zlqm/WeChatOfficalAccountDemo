from django.db.models.signals import pre_save

from .models import QRCode


def sync_qr_code_with_wechat(sender, instance=None, **kwargs):
    if not instance:
        return
    instance.sync_with_wechat()


pre_save.connect(sync_qr_code_with_wechat, sender=QRCode)
