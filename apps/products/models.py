from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Đường dẫn")
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name="Hình ảnh đại diện")
    
    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Danh mục")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True, verbose_name="Đường dẫn")
    name = models.CharField(max_length=255, verbose_name="Tên sản phẩm")
    short_description = models.TextField(verbose_name="Mô tả ngắn", blank=True, null=True)
    description = models.TextField(verbose_name="Mô tả chi tiết", blank=True, null=True)
    price = models.IntegerField(verbose_name="Giá")
    image = models.ImageField(upload_to='products/', verbose_name="Hình ảnh chính", blank=True, null=True)
    stock = models.IntegerField(default=100, verbose_name="Số lượng tồn kho")
    is_best_seller = models.BooleanField(default=False, verbose_name="Bán chạy")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Hình ảnh phụ")
    
    class Meta:
        verbose_name = "Hình ảnh phụ"
        verbose_name_plural = "Hình ảnh phụ"

class ProductPromotion(models.Model):
    product = models.ForeignKey(Product, related_name='promotions', on_delete=models.CASCADE)
    content = models.CharField(max_length=255, verbose_name="Nội dung khuyến mãi")
    
    class Meta:
        verbose_name = "Khuyến mãi"
        verbose_name_plural = "Khuyến mãi"

    def __str__(self):
        return self.content

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, verbose_name="Tên khách hàng")
    rating = models.IntegerField(verbose_name="Đánh giá (sao)")
    content = models.TextField(verbose_name="Nội dung nhận xét", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Nhận xét"
        verbose_name_plural = "Nhận xét"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.rating} sao"

from django.contrib.auth import get_user_model
User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Chờ xử lý'),
        ('processing', 'Đang chuẩn bị hàng'),
        ('shipped', 'Đang giao hàng'),
        ('delivered', 'Đã giao'),
        ('cancelled', 'Đã hủy'),
    )
    
    PAYMENT_CHOICES = (
        ('cod', 'Thanh toán khi nhận hàng (COD)'),
        ('bank_transfer', 'Chuyển khoản ngân hàng/Momo'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Người dùng")
    full_name = models.CharField(max_length=150, verbose_name="Họ và tên")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    address = models.TextField(verbose_name="Địa chỉ giao hàng")
    note = models.TextField(verbose_name="Ghi chú", blank=True, null=True)
    
    shipping_fee = models.IntegerField(default=0, verbose_name="Phí giao hàng")
    total_price = models.IntegerField(verbose_name="Tổng tiền (bao gồm ship)")
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod', verbose_name="Phương thức thanh toán")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái đơn hàng")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-created_at']

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='order_items', on_delete=models.SET_NULL, null=True)
    price = models.IntegerField(verbose_name="Giá tại thời điểm mua")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self):
        return f"{self.quantity} x {self.product.name if self.product else 'Sản phẩm đã xóa'}"
