from django.db import models


class SingletonManager(models.Manager):
    def get_instance(self):
        instance, created = self.get_or_create(pk=1)
        return instance
