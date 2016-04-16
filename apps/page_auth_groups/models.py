from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.pages.models import Page


class PageAuthGroup(models.Model):
    page = models.ForeignKey(Page, verbose_name=_('page'))
    group = models.ForeignKey(Group, verbose_name=_('group'), related_name='pages')

    class Meta:
        verbose_name = _('Page Auth Group')
        verbose_name_plural = _('Page Auth Group')
        ordering = ('group',)
        unique_together = ('page', 'group')

    @classmethod
    def unauthorized_pages(cls, user):
        if user.is_superuser:
            return list()
        groups = user.groups.all()
        if user.is_anonymous() or len(groups) == 0:
            return list(set(cls.objects.values_list('page__pk', flat=True)))
        pages = cls.objects.filter(group__in=groups).values_list('page__pk', flat=True)
        return list((cls.objects.exclude(page__in=pages).values_list('page__pk', flat=True)))


