from django.db import models
from django.utils.text import slugify

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Danh mục tin tức"
        verbose_name_plural = "Danh mục tin tức"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, related_name='articles', on_delete=models.SET_NULL, null=True, verbose_name="Danh mục")
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="Hình ảnh")
    excerpt = models.TextField(verbose_name="Đoạn trích", blank=True)
    content = models.TextField(verbose_name="Nội dung")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng")
    is_featured = models.BooleanField(default=False, verbose_name="Nổi bật")

    class Meta:
        verbose_name = "Bài viết"
        verbose_name_plural = "Bài viết"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
