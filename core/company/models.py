from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import BaseModel


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    street_line_1 = models.CharField(max_length=255)
    street_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    zipcode = models.CharField(max_length=10)

    class Meta:
        db_table = 'testapi_company'
        verbose_name_plural = _('Company')

    def __str__(self):
        return self.name
