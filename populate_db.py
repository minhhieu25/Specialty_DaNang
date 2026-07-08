import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Product

def populate():
    products = [
        {"name": "Chả bò - Thơm tiêu đậm vị", "price": 215000, "is_best_seller": True},
        {"name": "Cá bò rim mè - dai ngọt đậm đà", "price": 65000, "is_best_seller": True},
        {"name": "Cá chỉ vàng khô nướng - ngọt thịt dai dai", "price": 210000, "is_best_seller": True},
        {"name": "Bò nguyên miếng - dai mềm đậm đà", "price": 119000, "is_best_seller": True},
        {"name": "Tré - dai ngon đậm đà", "price": 65000, "is_best_seller": True},
        {"name": "Mực rim me - Dai ngon khó cưỡng", "price": 66000, "is_best_seller": True},
    ]

    for p in products:
        Product.objects.get_or_create(name=p['name'], defaults={'price': p['price'], 'is_best_seller': p['is_best_seller']})
    print("Database populated with initial products.")

if __name__ == '__main__':
    populate()
