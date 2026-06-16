from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="ชื่อหมวดหมู่")
    icon = models.CharField(max_length=50, default="📦", verbose_name="ไอคอน")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "หมวดหมู่"
        verbose_name_plural = "หมวดหมู่ทั้งหมด"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="หมวดหมู่")
    name = models.CharField(max_length=255, verbose_name="ชื่อสินค้า")
    description = models.TextField(blank=True, verbose_name="รายละเอียดสินค้า")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคา")
    image_url = models.URLField(max_length=500, blank=True, verbose_name="ลิงก์รูปภาพ")
    stock = models.IntegerField(default=0, verbose_name="จำนวนคงเหลือ")
    sold = models.IntegerField(default=0, verbose_name="ขายแล้ว")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "สินค้า"
        verbose_name_plural = "สินค้าทั้งหมด"

class Cart(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True, verbose_name="Session Key")
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default='Pending', verbose_name="สถานะ")

    class Meta:
        verbose_name = "คำสั่งซื้อ"
        verbose_name_plural = "คำสั่งซื้อทั้งหมด"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
