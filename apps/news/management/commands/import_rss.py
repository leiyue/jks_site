# -*- coding: utf-8 -*-
# -*- date: 2016-04-17 00:43 -*-

from datetime import timedelta
from optparse import make_option
from time import timezone
from urllib.parse import urljoin
from urllib.request import urlopen

from django.core.management import CommandError

from ..base import BaseImporterCommand


class Command(BaseImporterCommand):
    """
    Import an RSS feed into the news app.
    """

    option_list = BaseImporterCommand.option_list + (
        make_option("-r", "--rss-url", dest="rss_url",
                    help="RSS feed URL"),
        make_option("-p", "--page-url", dest="page_url",
                    help="URL for a web page containing the RSS link"),
    )
    help = ("Import an RSS feed into the news app. Requires the "
            "dateutil and feedparser packages installed, and also "
            "BeautifulSoup if using the --page-url option.")

    def handle_import(self, options):

        rss_url = options.get("rss_url")
        page_url = options.get("page_url")
        if not (page_url or rss_url):
            raise CommandError("Either --rss-url or --page-url option "
                               "must be specified")

        try:
            from dateutil import parser
        except ImportError:
            raise CommandError("dateutil package is required")
        try:
            from feedparser import parse
        except ImportError:
            raise CommandError("feedparser package is required")
        if not rss_url and page_url:
            if "://" not in page_url:
                page_url = "http://%s" % page_url
            try:
                from BeautifulSoup import BeautifulSoup
            except ImportError:
                raise CommandError("BeautifulSoup package is required")
            for l in BeautifulSoup(urlopen(page_url).read()).findAll("link"):
                if ("application/rss" in l.get("type", "") or
                            "application/atom" in l.get("type", "")):
                    rss_url = urljoin(page_url, l["href"])
                    break
            else:
                raise CommandError("Could not parse RSS link from the page")

        posts = parse(rss_url)["entries"]
        for post in posts:
            if hasattr(post, 'content'):
                content = post.content[0]["value"]
            else:
                content = post.summary
            tags = [tag["term"] for tag in getattr(post, 'tags', [])]
            try:
                pub_date = parser.parse(getattr(post, "published",
                                                post.updated)) - timedelta(seconds=timezone)
            except AttributeError:
                pub_date = None
            self.add_post(title=post.title, content=content,
                          pub_date=pub_date, tags=tags, old_url=None)
