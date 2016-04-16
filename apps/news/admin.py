from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import settings
from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin, BaseTranslationModelAdmin
from mezzanine.twitter.admin import TweetableAdminMixin

from .models import NewsPost, NewsCategory

newspost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
newspost_fieldsets[0][1]['fields'].insert(1, 'categories')
newspost_fieldsets[0][1]['fields'].extend(['content', 'allow_comments'])
newspost_list_display = ['title', 'user', 'status', 'admin_link']

if settings.NEWS_USE_FEATURED_IMAGE:
    newspost_fieldsets[0][1]['fields'].insert(-2, 'featured_image')
    newspost_list_display.insert(0, 'admin_thumb')
newspost_fieldsets = list(newspost_fieldsets)
newspost_fieldsets.insert(1, (_('Other posts'), {
    'classes': ('collapse-closed',),
    'fields': ('related_posts',)}))
newspost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ('categories',)


class NewsPostAdmin(TweetableAdminMixin, DisplayableAdmin, OwnableAdmin):
    fieldsets = newspost_fieldsets
    list_display = newspost_list_display
    list_filter = newspost_list_filter
    filter_horizontal = ('categories', 'related_posts',)

    def save_form(self, request, form, change):
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class NewsCategoryAdmin(BaseTranslationModelAdmin):
    fieldsets = ((None, {'fields': ('title',)}),)

    def in_menu(self):
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if 'apps.news.NewsCategory' in items:
                return True
            return False


admin.site.register(NewsPost, NewsPostAdmin)
admin.site.register(NewsCategory, NewsCategoryAdmin)
