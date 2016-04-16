from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'apps.news'

    def ready(self):
        import apps.news.defaults  # noqs