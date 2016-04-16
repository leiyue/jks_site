# -*- coding: utf-8 -*-
# -*- date: 2016-04-13 22:27 -*-

from mezzanine import template

register = template.Library()


@register.inclusion_tag('admin/includes/backup.html')
def admin_backup():
    pass
