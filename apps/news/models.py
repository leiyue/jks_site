from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to


class NewsPost(Displayable, Ownable, RichText, AdminThumbMixin):
    """
    A new post.
    """

    categories = models.ManyToManyField("NewsCategory",
                                        verbose_name=_("Categories"),
                                        blank=True, related_name="newsposts")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    comments = CommentsField(verbose_name=_("Comments"))
    rating = RatingField(verbose_name=_("Rating"))
    featured_image = FileField(verbose_name=_("Featured Image"),
                               upload_to=upload_to("apps.news.NewsPost.featured_image", "news"),
                               format="Image", max_length=255, null=True, blank=True)
    related_posts = models.ManyToManyField("self",
                                           verbose_name=_("Related posts"), blank=True)

    admin_thumb_field = "featured_image"

    class Meta:
        verbose_name = _("News post")
        verbose_name_plural = _("News posts")
        ordering = ("-publish_date",)

    def get_absolute_url(self):
        """
        URLs for news posts can either be just their slug, or prefixed
        with a portion of the post's publish date, controlled by the
        setting ``NEWS_URLS_DATE_FORMAT``, which can contain the value
        ``year``, ``month``, or ``day``. Each of these maps to the name
        of the corresponding urlpattern, and if defined, we loop through
        each of these and build up the kwargs for the correct urlpattern.
        The order which we loop through them is important, since the
        order goes from least granular (just year) to most granular
        (year/month/day).
        """
        url_name = "news_post_detail"
        kwargs = {"slug": self.slug}
        date_parts = ("year", "month", "day")
        if settings.NEWS_URLS_DATE_FORMAT in date_parts:
            url_name = "news_post_detail_%s" % settings.NEWS_URLS_DATE_FORMAT
            for date_part in date_parts:
                date_value = str(getattr(self.publish_date, date_part))
                if len(date_value) == 1:
                    date_value = "0%s" % date_value
                kwargs[date_part] = date_value
                if date_part == settings.NEWS_URLS_DATE_FORMAT:
                    break
        return reverse(url_name, kwargs=kwargs)


class NewsCategory(Slugged):
    """
    A category for grouping news posts into a series.
    """

    class Meta:
        verbose_name = _("News Category")
        verbose_name_plural = _("News Categories")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return ("news_post_list_category", (), {"category": self.slug})
