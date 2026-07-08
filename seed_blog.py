import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.blog.models import BlogCategory, Article

def seed_blog():
    print("Seeding blog categories and articles...")
    
    # Create Categories
    cat_tin_tuc, _ = BlogCategory.objects.get_or_create(name="Tin tức ẩm thực", slug="tin-tuc-am-thuc")
    cat_su_kien, _ = BlogCategory.objects.get_or_create(name="Sự kiện văn hóa", slug="su-kien-van-hoa")
    cat_meo_vat, _ = BlogCategory.objects.get_or_create(name="Mẹo vặt vào bếp", slug="meo-vat")

    # Create Articles
    articles_data = [
        {
            "title": "Lễ hội Ẩm thực Đà Nẵng 2026: Tinh hoa hội tụ",
            "slug": "le-hoi-am-thuc-da-nang-2026",
            "category": cat_su_kien,
            "excerpt": "Đừng bỏ lỡ cơ hội thưởng thức hàng ngàn món ăn đặc sản vùng miền tại Lễ hội Ẩm thực Đà Nẵng diễn ra vào cuối tháng này.",
            "content": "Lễ hội Ẩm thực Đà Nẵng 2026 hứa hẹn sẽ là sự kiện bùng nổ nhất mùa hè năm nay. Sự kiện sẽ quy tụ hơn 200 gian hàng ẩm thực từ khắp các tỉnh miền Trung. Du khách không chỉ được nếm thử những món ăn trứ danh như Mì Quảng, Bún chả cá, Tré, mà còn được chiêm ngưỡng các nghệ nhân trình diễn cách chế biến trực tiếp. <br><br>Sự kiện sẽ diễn ra từ ngày 15 đến 20 tháng 7 tại Công viên Biển Đông.",
            "is_featured": True
        },
        {
            "title": "Top 5 Đặc sản khô làm quà biếu lý tưởng nhất",
            "slug": "top-5-dac-san-kho-lam-qua",
            "category": cat_tin_tuc,
            "excerpt": "Khám phá danh sách 5 món đặc sản khô được du khách săn lùng nhiều nhất để làm quà tặng người thân.",
            "content": "Nếu bạn đang phân vân không biết mua gì về làm quà sau chuyến du lịch Đà Nẵng, hãy tham khảo ngay danh sách sau: <br>1. <b>Mực rim me</b>: Chua chua, ngọt ngọt, cay xé lưỡi - món ăn vặt quốc dân.<br>2. <b>Chả bò Đà Nẵng</b>: Thơm nồng mùi tiêu, dai giòn sần sật.<br>3. <b>Cá bò rim</b>: Món nhắm tuyệt vời cho những buổi chiều tụ tập.<br>4. <b>Tré bà Đệ</b>: Đặc sản không thể lẫn vào đâu được.<br>5. <b>Bò khô nguyên lát</b>: Đậm vị thịt bò, cay nồng ớt miền Trung.",
            "is_featured": False
        },
        {
            "title": "Bí quyết bảo quản chả bò được lâu mà vẫn thơm ngon",
            "slug": "bi-quyet-bao-quan-cha-bo",
            "category": cat_meo_vat,
            "excerpt": "Chả bò mua về nếu không biết cách bảo quản sẽ rất dễ bị chua. Đây là bí quyết từ chuyên gia.",
            "content": "Chả bò Đà Nẵng vốn không sử dụng chất bảo quản, do đó thời hạn sử dụng ở nhiệt độ thường rất ngắn (chỉ khoảng 1-2 ngày). Để bảo quản chả bò lâu mà vẫn giữ được độ dai ngon, bạn nên:<br><br>- <b>Bảo quản trong ngăn mát tủ lạnh</b>: Chả sẽ để được khoảng 5-7 ngày. Khi ăn, bạn nên lấy ra trước 30 phút để chả nguội bớt hoặc quay nhẹ qua lò vi sóng.<br>- <b>Bảo quản trong ngăn đá</b>: Chả sẽ để được 1 tháng. Khi muốn ăn, bạn phải rã đông tự nhiên trong ngăn mát tủ lạnh từ hôm trước, sau đó hấp lại cho nóng.<br><br>Tuyệt đối không nên để chả bò ở ngoài quá lâu trong thời tiết nắng nóng.",
            "is_featured": False
        }
    ]

    for data in articles_data:
        article, created = Article.objects.get_or_create(slug=data['slug'], defaults=data)
        if not created:
            # Update existing
            for key, value in data.items():
                setattr(article, key, value)
            article.save()
            
    print("Seed complete! 3 categories and 3 articles processed.")

if __name__ == '__main__':
    seed_blog()
