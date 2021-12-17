from django.db import models



class TelecomApi(models.Model):
    code = models.CharField(max_length=32, blank=False, null=False)
    price = models.PositiveBigIntegerField()