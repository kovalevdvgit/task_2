from django.db import models


class Robot(models.Model):

    tuple_status = (
        ('g','Готов к выдаче'),
        ('p','Передан в упаковочный цех'),
    )

    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    status = models.CharField(max_length=1, choices = tuple_status, default='g')