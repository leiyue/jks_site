# -*- coding: utf-8 -*-
# -*- date: 2016-04-17 00:02 -*-

from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from mezzanine import template
from mezzanine.generic.models import Keyword

from ..forms import NewsPostForm
from ..models import NewsPost, NewsCategory

User = get_user_model()

register = template.Library()


@register.as_tag
def news_months(*args):
    dates = NewsPost.objects.published().values_list('publish_date', flat=True)
    date_dicts = [{'date': datetime(d.year, d.month, 1)} for d in dates]
    month_dicts = []
    for date_dict in date_dicts:
        if date_dict not in month_dicts:
            month_dicts.append(date_dict)
    for i, date_dict in enumerate(month_dicts):
        month_dicts[i]['post_count'] = date_dicts.count(date_dict)
    return month_dicts


@register.as_tag
def news_categories(*args):
    news_posts = NewsPost.objects.published()
    categories = NewsCategory.objects.filter(newsposts__in=news_posts)
    return list(categories.annotate(post__count=Count('newsposts')))


@register.as_tag
def news_authors(*args):
    news_posts = NewsPost.objects.published()
    authors = User.objects.filter(newspost__in=news_posts)
    return list(authors.annotate(post__count=Count('newsposts')))


@register.as_tag
def news_recent_posts(limit=5, tag=None, username=None, category=None):
    news_posts = NewsPost.objects.published().select_related('user')
    title_or_slug = lambda s: Q(title=s) | Q(slug=s)
    if tag is not None:
        try:
            tag = Keyword.objects.get(title_or_slug(tag))
            news_posts = news_posts.filter(keywords__keyword=tag)
        except Keyword.DoesNotExist:
            return []
    if category is not None:
        try:
            category = NewsCategory.objects.get(title_or_slug(category))
            news_posts = news_posts.filter(categories=category)
        except NewsCategory.DoesNotExist:
            return []
    if username is not None:
        try:
            author = User.objects.get(username=username)
            news_posts = news_posts.filter(user=author)
        except User.DoesNotExist:
            return []
    return list(news_posts[:limit])


@register.inclusion_tag('admin/includes/quick_news.html', takes_context=True)
def quick_news(context):
    context['form'] = NewsPostForm()
    return context
