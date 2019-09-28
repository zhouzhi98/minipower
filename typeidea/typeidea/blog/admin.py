from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site


# Register your models here.
class PostInline(admin.StackedInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav')
    inlines = [PostInline, ]

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    title = "分类过滤器"
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_time', 'owner', 'operator', ]
    list_display_links = []
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']
    actions_on_top = True
    actions_on_bottom = True
    save_on_top = True
    # fields = (('title', 'category'), 'desc', 'status', 'content', 'owner', 'tag', )
    # filter_vertical = ('tag',)
    form = PostAdminForm
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (('title', 'category'), 'status',),
        }),
        ('内容', {
            'fields': ('desc', 'content',),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('cus_admin:blog_post_change', args=(obj.id,)))

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(owner=request.user)

    """class Media:
        css = {'all': ("https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",),
               }
        js = ("https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js",)"""
