import markdown
from django.utils.html import strip_tags
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import re
from django.utils import timezone
from django.utils.functional import cached_property


# Create your models here.
class Category(models.Model):
    name = models.CharField('分类名', max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签名', max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('标题', max_length=70, blank=False)
    body = models.TextField('内容', blank=False)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)

    excerpt = models.CharField('摘要', max_length=200, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    views = models.PositiveIntegerField('阅读数', default=0, editable=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time', 'title']

    def __str__(self):
        return self.title

    # 自定义方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # 首先实例化一个 Markdown 类，用于渲染 body 的文本
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    @property
    def toc(self):
        return self.rich_content.get('toc', '')

    @property
    def body_html(self):
        return self.rich_content.get('content', '')

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)


def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ''
    return {"content": content, "toc": toc}
