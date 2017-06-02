import datetime

from django.utils import timezone
from django.db import models

class PinCode(models.Model):
    pin_code = models.PositiveSmallIntegerField()
    voter = models.PositiveIntegerField()
    station = models.PositiveIntegerField()

    creation = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return (timezone.now() - self.creation).total_seconds() < 3600

    def __str__(self):
        return '{:06d}'.format(self.pin_code)
