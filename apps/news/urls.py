# -*- coding: utf-8 -*-
# -*- date: 2016-04-16 23:26 -*-

from django.conf.urls import url
from mezzanine.conf import settings
from . import views

_slash = "/" if settings.APPEND_SLASH else ""

# News patterns.
urlpatterns = [
    url("^feeds/(?P<format>.*)%s$" % _slash,
        views.news_post_feed, name="news_post_feed"),
    url("^tag/(?P<tag>.*)/feeds/(?P<format>.*)%s$" % _slash,
        views.news_post_feed, name="news_post_feed_tag"),
    url("^tag/(?P<tag>.*)%s$" % _slash,
        views.news_post_list, name="news_post_list_tag"),
    url("^category/(?P<category>.*)/feeds/(?P<format>.*)%s$" % _slash,
        views.news_post_feed, name="news_post_feed_category"),
    url("^category/(?P<category>.*)%s$" % _slash,
        views.news_post_list, name="news_post_list_category"),
    url("^author/(?P<username>.*)/feeds/(?P<format>.*)%s$" % _slash,
        views.news_post_feed, name="news_post_feed_author"),
    url("^author/(?P<username>.*)%s$" % _slash,
        views.news_post_list, name="news_post_list_author"),
    url("^archive/(?P<year>\d{4})/(?P<month>\d{1,2})%s$" % _slash,
        views.news_post_list, name="news_post_list_month"),
    url("^archive/(?P<year>\d{4})%s$" % _slash,
        views.news_post_list, name="news_post_list_year"),
    url("^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/"
        "(?P<slug>.*)%s$" % _slash,
        views.news_post_detail, name="news_post_detail_day"),
    url("^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>.*)%s$" % _slash,
        views.news_post_detail, name="news_post_detail_month"),
    url("^(?P<year>\d{4})/(?P<slug>.*)%s$" % _slash,
        views.news_post_detail, name="news_post_detail_year"),
    url("^(?P<slug>.*)%s$" % _slash,
        views.news_post_detail, name="news_post_detail"),
    url("^$", views.news_post_list, name="news_post_list"),
]
