# -*- coding: utf-8 -*-
# -*- date: 2016-04-16 22:13 -*-

from django import forms
from mezzanine.core.models import CONTENT_STATUS_DRAFT

from .models import NewsPost

hidden_field_defaults = ("status", "gen_description", "allow_comments")


class NewsPostForm(forms.ModelForm):
    """
    Model form for ``NewsPost`` that provides the quick news panel in the
    admin dashboard.
    """

    class Meta:
        model = NewsPost
        fields = ("title", "content") + hidden_field_defaults

    def __init__(self):
        initial = {}
        for field in hidden_field_defaults:
            initial[field] = NewsPost._meta.get_field(field).default
        initial["status"] = CONTENT_STATUS_DRAFT
        super(NewsPostForm, self).__init__(initial=initial)
        for field in hidden_field_defaults:
            self.fields[field].widget = forms.HiddenInput()
