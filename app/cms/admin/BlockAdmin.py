from django.contrib import admin

from app.cms.models import Block, SliderImage


class SliderImageInline(admin.TabularInline):

    model = SliderImage
    extra = 1


class BlockInline(admin.StackedInline):
    model = Block
    extra = 1
    inlines = [SliderImageInline]

    def get_inline_instances(self, request, obj=None):
        if obj and obj.block_type == "slider":
            return [SliderImageInline(self.model, self.admin_site)]
        return super().get_inline_instances(request, obj)


class BlockAdmin(admin.ModelAdmin):
    list_display = ("block_type", "blog", "content")
    list_filter = ("block_type", "blog")

    inlines = [SliderImageInline]

    def get_inline_instances(self, request, obj=None):
        if obj and obj.block_type == "slider":
            return [SliderImageInline(self.model, self.admin_site)]
        return super().get_inline_instances(request, obj)


admin.site.register(Block, BlockAdmin)
