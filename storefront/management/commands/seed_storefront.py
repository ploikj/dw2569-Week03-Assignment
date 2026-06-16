from django.core.management.base import BaseCommand
from storefront.models import Category, Product

class Command(BaseCommand):
    help = 'Seed database with initial storefront data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Categories
        cat_names = [
            ("เสื้อผ้าแฟชั่น", "👕"), ("เครื่องใช้ไฟฟ้า", "🔌"), ("ความงาม", "💄"),
            ("ของใช้ในบ้าน", "🏠"), ("มือถือและอุปกรณ์", "📱"), ("คอมพิวเตอร์", "💻"),
            ("กีฬาและยานยนต์", "⚽"), ("อาหารเสริม", "💊")
        ]
        
        categories = {}
        for name, icon in cat_names:
            cat, created = Category.objects.get_or_create(name=name, defaults={'icon': icon})
            categories[name] = cat
        
        # Products
        products_data = [
            # Original 5
            {"category_name": "มือถือและอุปกรณ์", "name": "หูฟังบลูทูธไร้สาย เสียงดี เบสแน่น ตัดเสียงรบกวน", "price": "450.00", "stock": 100, "sold": 1200, "image_url": "https://picsum.photos/seed/earbuds/300/300"},
            {"category_name": "เครื่องใช้ไฟฟ้า", "name": "สมาร์ทวอทช์ วัดชีพจร กันน้ำ ใส่ใส่ออกกำลังกาย", "price": "890.00", "stock": 50, "sold": 500, "image_url": "https://picsum.photos/seed/watch/300/300"},
            {"category_name": "มือถือและอุปกรณ์", "name": "เคสโทรศัพท์ซิลิโคนใส กันกระแทกได้ดีเยี่ยม", "price": "59.00", "stock": 500, "sold": 3500, "image_url": "https://picsum.photos/seed/case/300/300"},
            {"category_name": "เสื้อผ้าแฟชั่น", "name": "กระเป๋าเป้สะพายหลัง จุของได้เยอะ ดีไซน์เกาหลี", "price": "299.00", "stock": 200, "sold": 850, "image_url": "https://picsum.photos/seed/bag/300/300"},
            {"category_name": "เครื่องใช้ไฟฟ้า", "name": "ลำโพงพกพา เสียงดัง คุ้มราคา แบตเตอรี่อึด", "price": "399.00", "stock": 30, "sold": 2100, "image_url": "https://picsum.photos/seed/speaker/300/300"},
            
            # 20 New Products
            {"category_name": "เสื้อผ้าแฟชั่น", "name": "เสื้อแจ็คเก็ตกันลม สไตล์เกาหลี ทรงสปอร์ต", "price": "490.00", "stock": 80, "sold": 320, "image_url": "https://picsum.photos/seed/jacket/300/300"},
            {"category_name": "เสื้อผ้าแฟชั่น", "name": "กางเกงยีนส์ ทรงขากระบอก เอวสูง", "price": "350.00", "stock": 120, "sold": 890, "image_url": "https://picsum.photos/seed/jeans/300/300"},
            {"category_name": "เสื้อผ้าแฟชั่น", "name": "รองเท้าผ้าใบ พื้นนุ่ม ใส่สบายตลอดวัน", "price": "590.00", "stock": 150, "sold": 1150, "image_url": "https://picsum.photos/seed/sneakers/300/300"},
            {"category_name": "เสื้อผ้าแฟชั่น", "name": "หมวกแก๊ป ปักลายมินิมอล ใส่กันแดด", "price": "120.00", "stock": 300, "sold": 2400, "image_url": "https://picsum.photos/seed/cap/300/300"},
            
            {"category_name": "คอมพิวเตอร์", "name": "เมาส์ไร้สาย เสียงเงียบ จับถนัดมือ", "price": "199.00", "stock": 200, "sold": 1400, "image_url": "https://picsum.photos/seed/mouse/300/300"},
            {"category_name": "คอมพิวเตอร์", "name": "คีย์บอร์ดเกมมิ่ง ไฟ RGB กดสนุก", "price": "790.00", "stock": 60, "sold": 450, "image_url": "https://picsum.photos/seed/keyboard/300/300"},
            {"category_name": "คอมพิวเตอร์", "name": "แผ่นรองเมาส์ ขนาดใหญ่พิเศษ เย็บขอบ", "price": "89.00", "stock": 400, "sold": 3800, "image_url": "https://picsum.photos/seed/mousepad/300/300"},
            {"category_name": "คอมพิวเตอร์", "name": "หน้าจอมอนิเตอร์ 24 นิ้ว 144Hz สำหรับเล่นเกม", "price": "3990.00", "stock": 20, "sold": 120, "image_url": "https://picsum.photos/seed/monitor/300/300"},
            
            {"category_name": "ความงาม", "name": "ลิปสติก เนื้อแมตต์ สีชัด ติดทนตลอดวัน", "price": "250.00", "stock": 150, "sold": 5600, "image_url": "https://picsum.photos/seed/lipstick/300/300"},
            {"category_name": "ความงาม", "name": "เซรั่มบำรุงผิวหน้า สูตรกระจ่างใส ลดรอย", "price": "490.00", "stock": 80, "sold": 900, "image_url": "https://picsum.photos/seed/serum/300/300"},
            {"category_name": "ความงาม", "name": "ครีมกันแดด SPF50 PA+++ เนื้อบางเบา", "price": "320.00", "stock": 100, "sold": 2100, "image_url": "https://picsum.photos/seed/sunscreen/300/300"},
            {"category_name": "ความงาม", "name": "แชมพูสูตรสมุนไพร ลดผมร่วง เร่งผมยาว", "price": "180.00", "stock": 250, "sold": 1800, "image_url": "https://picsum.photos/seed/shampoo/300/300"},
            
            {"category_name": "ของใช้ในบ้าน", "name": "ชุดเครื่องนอน ผ้าปูที่นอน 6 ฟุต นุ่มสบาย", "price": "890.00", "stock": 40, "sold": 350, "image_url": "https://picsum.photos/seed/bed/300/300"},
            {"category_name": "ของใช้ในบ้าน", "name": "ไม้ถูพื้น รีดน้ำอัตโนมัติ หมุนได้ 360 องศา", "price": "150.00", "stock": 300, "sold": 4200, "image_url": "https://picsum.photos/seed/mop/300/300"},
            {"category_name": "ของใช้ในบ้าน", "name": "กล่องเก็บของพับได้ ประหยัดพื้นที่จัดเก็บ", "price": "99.00", "stock": 500, "sold": 6000, "image_url": "https://picsum.photos/seed/box/300/300"},
            {"category_name": "ของใช้ในบ้าน", "name": "โคมไฟตั้งโต๊ะ LED ถนอมสายตา ปรับแสงได้", "price": "290.00", "stock": 120, "sold": 850, "image_url": "https://picsum.photos/seed/lamp/300/300"},
            
            {"category_name": "เครื่องใช้ไฟฟ้า", "name": "เครื่องปั่นน้ำผลไม้ พกพาสะดวก ชาร์จ USB", "price": "350.00", "stock": 90, "sold": 1100, "image_url": "https://picsum.photos/seed/blender/300/300"},
            {"category_name": "เครื่องใช้ไฟฟ้า", "name": "หม้อทอดไร้น้ำมัน 5 ลิตร ทรงสวย ทำความสะอาดง่าย", "price": "1290.00", "stock": 30, "sold": 420, "image_url": "https://picsum.photos/seed/airfryer/300/300"},
            {"category_name": "เครื่องใช้ไฟฟ้า", "name": "ไดร์เป่าผม ลมแรง แห้งไว ผมไม่เสีย", "price": "450.00", "stock": 100, "sold": 1300, "image_url": "https://picsum.photos/seed/hairdryer/300/300"},
            
            {"category_name": "อาหารเสริม", "name": "วิตามินซี 1000mg บำรุงร่างกาย ภูมิคุ้มกัน", "price": "250.00", "stock": 200, "sold": 3400, "image_url": "https://picsum.photos/seed/vitamin/300/300"}
        ]

        for p_data in products_data:
            cat = categories[p_data["category_name"]]
            Product.objects.get_or_create(
                name=p_data["name"],
                defaults={
                    "category": cat,
                    "price": p_data["price"],
                    "stock": p_data["stock"],
                    "sold": p_data["sold"],
                    "image_url": p_data["image_url"],
                    "description": "รายละเอียดแบบเต็มสำหรับ " + p_data["name"]
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with 25 products!'))
