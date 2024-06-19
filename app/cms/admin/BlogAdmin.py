from django.contrib import admin

from app.cms.admin.BlockAdmin import BlockInline
from app.cms.models import Blog


class BlogAdmin(admin.ModelAdmin):
    model = Blog
    inlines = [BlockInline]
    list_display = ("title",)


admin.site.register(Blog, BlogAdmin)
