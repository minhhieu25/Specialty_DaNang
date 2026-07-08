from django.db import models

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Họ và tên")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Nội dung")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày gửi")

    class Meta:
        verbose_name = "Liên hệ"
        verbose_name_plural = "Liên hệ"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.phone}"
