from copy import deepcopy

from django import forms
from django.contrib import admin
from mezzanine.pages import admin as pages_admin

from .models import CategoryLink

CATEGORY_LINK_FIEDSETS = deepcopy(pages_admin.PageAdmin.fieldsets)
CATEGORY_LINK_FIEDSETS[0][1]['fields'].insert(1, 'blog_category')


class CategoryLinkForm(forms.ModelForm):
    model = CategoryLink


class CategoryLinkAdmin(pages_admin.PageAdmin):
    form = CategoryLinkForm
    fieldsets = CATEGORY_LINK_FIEDSETS


admin.site.register(CategoryLink, CategoryLinkAdmin)
