from django.db import models, connection
from django.utils.translation import gettext_lazy as _
import constants


class Weekday(models.Model):
    name = models.CharField(_('Name'), max_length=20)

    class Meta:
        verbose_name = _('Weekday')
        verbose_name_plural = _('Weekdays')

    def __str__(self):
        return str(_(self.name))


if 'helper_weekday' in connection.introspection.table_names():
    for index, weekday in enumerate(constants.WEEKDAYS):
        try:
            Weekday.objects.get(id=index)
        except:
            Weekday.objects.create(id=index, name=weekday[1])
