import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Post, Category, Tag

from django.views.generic import ListView, DetailView
from pure_pagination import PaginationMixin


# Create your views here.
class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 5


class PostDetailview(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response


class ArchiveView(IndexView):
    """归档页面"""
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(created_time__year=year, created_time__month=month)


class CategoryView(IndexView):
    """分类页面"""
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)


class TagView(IndexView):
    """标签页面"""
    def get_queryset(self):
        cate = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=cate)
