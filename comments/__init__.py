from django.apps import AppConfig

default_app_config = 'comments.CommentsConfig'


class CommentsConfig(AppConfig):
    name = 'comments'
    verbose_name = '评论管理'
