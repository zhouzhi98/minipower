from django.contrib import admin

from .models import Comment
from typeidea.custom_site import custom_site

# Register your models here.
@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
    fields = ('target', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
