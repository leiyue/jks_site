# -*- coding: utf-8 -*-
from django.db import models

from django.utils.translation import ugettext_lazy as _
from mezzanine.core.fields import FileField, RichTextField

from mezzanine.core.models import RichText, Orderable, Slugged, SiteRelated

from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to

LOREM_STRING = '不但喜愛小孩子是。卻沒法搬出城外去，世界上沒有群比蘿莉控更強大的人們？' \
               '是恨！連馬桶都改裝成電水井了，他的思想也不細密，解嘲已往的一切，所以。如是幾次。' \
               '其禍害甚至會比七日之火更甚，小書！托他們直是白托。' \
               '又接著說道，他知道她眼睛快。可是誰也沒見她走出去，涼了。' \
               '你穿來的白衣不曾沾著一斑的泥污。不是永遠的相隔讓人害怕，居然獵到一隻麻雀？'


class HomePage(Page, RichText):
    heading = models.CharField(_('Heading'), max_length=200,
                               default=_('Hello, World'),
                               help_text=_('The heading under the icon blurbs'))
    sub_heading = models.CharField(_('SubHeading'), max_length=1000,
                                   default=_('This is a template for a simple marketing or ' +
                                             'informational website. It includes a large callout called ' +
                                             'a jumbotron and three supporting pieces of content. Use it ' +
                                             'as a starting point to create something more unique.'),
                                   help_text=_('The subheading just below the heading'))
    heading_button = models.CharField(_('Button text'), max_length=200, default=_('Learn more'))
    heading_link = models.CharField(_('Button link'), max_length=200, blank=True, default=_('#'),
                                    help_text=_('Optional, if provided the heading button will be visible'))
    iconbox_heading = models.CharField(_('Iconbox heading'), max_length=200, null=True, blank=True,
                                       help_text=_('Optional, if provided the iconbox heading will be visible'))
    content_heading = models.CharField(_('Content heading'), max_length=200, default=_('About us'))

    class Meta:
        verbose_name = _('Home page')
        verbose_name_plural = _('Home pages')


class Slide(Orderable):
    homepage = models.ForeignKey(HomePage, related_name='slides')
    image = FileField(verbose_name=_('Image'), upload_to=upload_to('apps.themes.Slide.image', 'slider'),
                      format='Image', max_length=255, null=True, blank=True)


class IconBlurb(Orderable):
    homepage = models.ForeignKey(HomePage, related_name='blurbs')
    icon = FileField(verbose_name=_('Image'), upload_to=upload_to('apps.themes.IconBlurb.icon', 'icons'),
                     format='Image', max_length=255, null=True, blank=True)
    title = models.CharField(_('Title'), max_length=200, default=_('Heading'))
    content = models.TextField(_('Content'), default=LOREM_STRING)
    link = models.CharField(_('Link'), max_length=200, blank=True,
                            help_text=_('Optional, if provided clicking the blurb will go here'))


class SiteWideContent(SiteRelated):
    box_1st_title = models.CharField(_('Box 1 title'), max_length=200, default=_('About'))
    box_1st_content = RichTextField(_('Box 1 content'), default=LOREM_STRING)
    box_2nd_title = models.CharField(_('Box 2 title'), max_length=200, default=_('Contact'))
    box_2nd_content = RichTextField(_('Box 2 content'), default=LOREM_STRING)
    box_3rd_title = models.CharField(_('Box 3 title'), max_length=200, default=_('Links'))
    box_3rd_content = RichTextField(_('Box 3 content'), default=LOREM_STRING)

    class Meta:
        verbose_name = _('Site wide content')
        verbose_name_plural = _('Site wide content')
