# -*- coding: utf-8 -*-
# -*- date: 2016-04-11 22:13 -*-
from mezzanine import template
from mezzanine.utils.sites import current_site_id

from ..models import SiteWideContent

register = template.Library()


@register.as_tag
def get_site_wide_content():
    return SiteWideContent.objects.get_or_create(site_id=current_site_id())[0]
