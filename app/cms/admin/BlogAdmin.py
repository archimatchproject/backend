from app.cms.models import Blog
from django.contrib import admin
from app.cms.admin.utils.BlockAdmin import BlockInline

class BlogAdmin(admin.ModelAdmin):
    model = Blog
    inlines = [BlockInline]
    list_display=('title',)
    
admin.site.register(Blog, BlogAdmin)