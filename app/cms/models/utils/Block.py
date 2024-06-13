from django.db import models
from app.CMS.models.Blog import Blog


class Block(models.Model):
    BLOG_BLOCK_TYPES = [
        ("title", "Title"),
        ("paragraph", "Paragraph"),
        ("image", "Image"),
        ("slider", "Slider"),
    ]

    blog = models.ForeignKey(Blog, related_name="blocks", on_delete=models.CASCADE)
    block_type = models.CharField(max_length=10, choices=BLOG_BLOCK_TYPES)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="BlockImages/", blank=True, null=True)

    def __str__(self):
        return f"{self.get_block_type_display()} for {self.blog.title}"
