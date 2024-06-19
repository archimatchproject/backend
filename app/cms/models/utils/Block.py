from django.db import models

from app.cms.models.Blog import Blog


class Block(models.Model):
    """
    Model representing a block within a blog post.

    Attributes:
        BLOG_BLOCK_TYPES (list): Choices for types of blocks within a blog post.
        blog (ForeignKey): Blog to which the block belongs, related_name is 'blocks'.
        block_type (CharField): Type of the block, selected from BLOG_BLOCK_TYPES.
        content (TextField): Optional content of the block.
        image (ImageField): Optional image associated with the block, stored in 'BlockImages/' directory.
    """

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
        """
        String representation of the block.
        """
        return f"{self.get_block_type_display()} for {self.blog.title}"
