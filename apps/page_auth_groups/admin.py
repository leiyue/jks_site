from copy import deepcopy

from django.contrib import admin
from django.contrib.messages import INFO
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin, LinkAdmin
from mezzanine.pages.models import Page, RichTextPage, Link

from .models import PageAuthGroup


class PageAuthGroupAdminMixin(object):
    def save_related(self, request, form, formsets, change):
        super(PageAuthGroupAdminMixin, self).save_related(
            request,
            form,
            formsets,
            change
        )
        parent_id = request.GET.get('parent', None)
        if parent_id is not None and not change and form.instance.pageauthgroup_set.count() == 0:
            for parent_pag in PageAuthGroup.objects.filter(page_id=parent_id):
                parent_title = parent_pag.page.title
                PageAuthGroup.objects.create(page=form.instance, group=parent_pag.group)
                msg = (_('The %(model_name)s "%(page_title)s" has inherited the'
                         ' authorizations from parent "%(parent_title)s"') %
                       {'model_name': form.instance._meta.verbose_name,
                        'page_title': form.instance.title,
                        'parent_title': parent_title})
                self.message_user(request, msg, INFO)


class PageAuthGroupInline(TabularDynamicInlineAdmin):
    model = PageAuthGroup


class PageAuthGroupAdmin(PageAuthGroupAdminMixin, PageAdmin):
    inlines = deepcopy(PageAdmin.inlines) + [PageAuthGroupInline]


class LinkAuthGroupAdmin(PageAuthGroupAdminMixin, LinkAdmin):
    inlines = deepcopy(LinkAdmin.inlines) + [PageAuthGroupInline]


admin.site.unregister(Page)
admin.site.unregister(RichTextPage)
admin.site.unregister(Link)
admin.site.register(Page, PageAuthGroupAdmin)
admin.site.register(RichTextPage, PageAuthGroupAdmin)
admin.site.register(Link, LinkAuthGroupAdmin)
