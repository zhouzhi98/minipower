from django.shortcuts import render

from django.http import HttpResponse
from .models import Post, Tag, Category
from config.models import SideBar

# Create your views here.
def post_list(request, category_id=None, tag_id=None):
    category = None
    tag = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
    sidebars = SideBar.get_all()
    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': sidebars,
    }
    context.update(Category.get_navs())
    return render(request, "blog/list.html", context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    return render(request, 'blog/detail.html', context={'post': post})


def link(request):
    return HttpResponse('link')
