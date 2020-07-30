from django.apps import AppConfig

default_app_config = 'blog.BlogConfig'


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = '博客管理'
