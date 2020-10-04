from django.db import models
from OpenWeChat.auth.cache import DummyCache


class Cache(models.Model):
    key = models.CharField(max_length=64, primary_key=True)
    value = models.TextField()
    update_time = models.DateTimeField(auto_now=True)
    expires_in = models.PositiveIntegerField()


class AuthCache(DummyCache):
    def get_credential_data(self, key):
        record = Cache.objects.filter(key=key).first()
        if record:
            return record.value
        return None

    def update_credential_data(self, key, value, expires_in):
        return Cache.objects.update_or_create(
            key=key,
            defaults={
                'value': value,
                'expires_in': expires_in
            },
        )


auth_cache = AuthCache()
