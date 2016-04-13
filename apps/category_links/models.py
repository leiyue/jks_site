from django.core.urlresolvers import reverse
from django.db import models
from django.utils.http import urlunquote

from django.utils.translation import ugettext_lazy as _
from mezzanine.blog import models as blog_models
from mezzanine.pages import models as pages_models


class CategoryLink(pages_models.Page):
    blog_category = models.ForeignKey(blog_models.BlogCategory)

    class Meta:
        verbose_name = _('Category link')
        verbose_name_plural = _('Category links')

    def get_absolute_url(self):
        category_slug = self.blog_category.slug
        reverse_url = reverse('blog_post_list_category', args=(category_slug,))
        return reverse_url.strip('/')

    def save(self, *args, **kwargs):
        self.slug = urlunquote(self.get_absolute_url())
        return super(CategoryLink, self).save(*args, **kwargs)
