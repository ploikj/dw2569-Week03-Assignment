import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wichit2s.settings')
django.setup()

from storefront.models import Category, Product

def populate():
    print("Clearing old data...")
    Product.objects.all().delete()
    Category.objects.all().delete()

    print("Creating categories...")
    categories_data = [
        {"name": "อิเล็กทรอนิกส์", "icon": "💻"},
        {"name": "เสื้อผ้าแฟชั่น", "icon": "👕"},
        {"name": "เครื่องใช้ในบ้าน", "icon": "🏠"},
        {"name": "กีฬา", "icon": "⚽"},
        {"name": "ความงาม", "icon": "💄"},
    ]
    
    cats = {}
    for c in categories_data:
        cats[c["name"]] = Category.objects.create(name=c["name"], icon=c["icon"])

    print("Creating products...")
    products_data = [
        {"cat": "อิเล็กทรอนิกส์", "name": "สมาร์ทโฟน X Pro Max", "price": 25900, "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&q=80"},
        {"cat": "อิเล็กทรอนิกส์", "name": "หูฟังไร้สาย Noise Cancelling", "price": 4500, "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"},
        {"cat": "อิเล็กทรอนิกส์", "name": "สมาร์ทวอทช์ Series 5", "price": 8900, "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80"},
        {"cat": "เสื้อผ้าแฟชั่น", "name": "เสื้อยืดคอตตอน 100% สไตล์มินิมอล", "price": 350, "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&q=80"},
        {"cat": "เสื้อผ้าแฟชั่น", "name": "กางเกงยีนส์ทรงวินเทจคลาสสิก", "price": 1200, "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500&q=80"},
        {"cat": "เครื่องใช้ในบ้าน", "name": "โคมไฟตั้งโต๊ะ LED ถนอมสายตา", "price": 590, "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500&q=80"},
        {"cat": "เครื่องใช้ในบ้าน", "name": "เก้าอี้ทำงานเพื่อสุขภาพ Ergo", "price": 3500, "image": "https://images.unsplash.com/photo-1505843490538-5133c6c7d0e1?w=500&q=80"},
        {"cat": "กีฬา", "name": "รองเท้าวิ่งมาราธอน Pro Series", "price": 4200, "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80"},
        {"cat": "กีฬา", "name": "ดัมเบลปรับน้ำหนักได้ 24kg", "price": 1500, "image": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=500&q=80"},
        {"cat": "ความงาม", "name": "เซรั่มบำรุงผิวหน้า Vitamin C", "price": 890, "image": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500&q=80"},
    ]

    for p in products_data:
        Product.objects.create(
            category=cats[p["cat"]],
            name=p["name"],
            description="รายละเอียดสินค้าคุณภาพดี: " + p["name"],
            price=p["price"],
            image_url=p["image"],
            stock=random.randint(20, 100),
            sold=random.randint(5, 50)
        )

    print(f"Successfully generated {len(products_data)} products in {len(categories_data)} categories!")

if __name__ == '__main__':
    populate()
