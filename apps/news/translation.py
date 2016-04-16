# -*- coding: utf-8 -*-
# -*- date: 2016-04-16 23:30 -*-

from mezzanine.core.translation import (TranslatedSlugged,
                                        TranslatedDisplayable,
                                        TranslatedRichText)
from modeltranslation.translator import translator

from .models import NewsPost, NewsCategory


class TranslatedNewsPost(TranslatedDisplayable, TranslatedRichText):
    fields = ()


class TranslatedNewsCategory(TranslatedSlugged):
    fields = ()


translator.register(NewsPost, TranslatedNewsPost)
translator.register(NewsCategory, TranslatedNewsCategory)
