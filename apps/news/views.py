from calendar import month_name

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import paginate

from .feeds import PostsRSS, PostsAtom
from .models import NewsPost, NewsCategory

User = get_user_model()


def news_post_list(request, tag=None, year=None, month=None, username=None,
                   category=None, template="news/news_post_list.html",
                   extra_context=None):
    """
    Display a list of news posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``news/news_post_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
    templates = []
    news_posts = NewsPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        news_posts = news_posts.filter(keywords__keyword=tag)
    if year is not None:
        news_posts = news_posts.filter(publish_date__year=year)
        if month is not None:
            news_posts = news_posts.filter(publish_date__month=month)
            try:
                month = month_name[int(month)]
            except IndexError:
                raise Http404()
    if category is not None:
        category = get_object_or_404(NewsCategory, slug=category)
        news_posts = news_posts.filter(categories=category)
        templates.append(u"news/news_post_list_%s.html" %
                         str(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        news_posts = news_posts.filter(user=author)
        templates.append(u"news/news_post_list_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    news_posts = news_posts.select_related("user").prefetch_related(*prefetch)
    news_posts = paginate(news_posts, request.GET.get("page", 1),
                          settings.BLOG_POST_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"news_posts": news_posts, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    context.update(extra_context or {})
    templates.append(template)
    return TemplateResponse(request, templates, context)


def news_post_detail(request, slug, year=None, month=None, day=None,
                     template="news/news_post_detail.html",
                     extra_context=None):
    """. Custom templates are checked for using the name
    ``news/news_post_detail_XXX.html`` where ``XXX`` is the news
    posts's slug.
    """
    news_posts = NewsPost.objects.published(
        for_user=request.user).select_related()
    news_post = get_object_or_404(news_posts, slug=slug)
    related_posts = news_post.related_posts.published(for_user=request.user)
    context = {"news_post": news_post, "editable_obj": news_post,
               "related_posts": related_posts}
    context.update(extra_context or {})
    templates = [u"news/news_post_detail_%s.html" % str(slug), template]
    return TemplateResponse(request, templates, context)


def news_post_feed(request, format, **kwargs):
    """
    News posts feeds - maps format to the correct feed view.
    """
    try:
        return {"rss": PostsRSS, "atom": PostsAtom}[format](**kwargs)(request)
    except KeyError:
        raise Http404()
