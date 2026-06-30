from django.db import models
from django.conf import settings
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="ชื่อหมวดหมู่")
    description = models.TextField(blank=True, verbose_name="รายละเอียด")
    is_active = models.BooleanField(default=True, verbose_name="เปิดใช้งาน")

    class Meta:
        verbose_name = "หมวดหมู่สินค้า"
        verbose_name_plural = "หมวดหมู่สินค้า"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="หมวดหมู่")
    name = models.CharField(max_length=200, verbose_name="ชื่อสินค้า")
    sku = models.CharField(max_length=50, unique=True, verbose_name="รหัสสินค้า (SKU)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคา")
    stock_quantity = models.IntegerField(default=0, verbose_name="จำนวนคงเหลือ")
    is_active = models.BooleanField(default=True, verbose_name="พร้อมขาย")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="แก้ไขล่าสุด")

    class Meta:
        verbose_name = "สินค้า"
        verbose_name_plural = "สินค้า"

    def __str__(self):
        return f"{self.name} ({self.sku})"

class Order(models.Model):
    PAYMENT_METHODS = (
        ('CASH', 'เงินสด'),
        ('CREDIT_CARD', 'บัตรเครดิต'),
        ('PROMPTPAY', 'พร้อมเพย์ / โอนเงิน'),
        ('OTHER', 'อื่นๆ'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'รอชำระเงิน'),
        ('COMPLETED', 'ชำระเงินแล้ว'),
        ('CANCELLED', 'ยกเลิก'),
    )

    receipt_number = models.CharField(max_length=50, unique=True, editable=False, verbose_name="เลขที่ใบเสร็จ")
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="พนักงานขาย")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="ยอดรวมก่อนภาษี")
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="ภาษีมูลค่าเพิ่ม (VAT)")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="ยอดสุทธิ")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='CASH', verbose_name="วิธีชำระเงิน")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COMPLETED', verbose_name="สถานะ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่ทำรายการ")
    
    class Meta:
        verbose_name = "ใบเสร็จรับเงิน / ออเดอร์"
        verbose_name_plural = "ใบเสร็จรับเงิน / ออเดอร์"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            # Generate a simple receipt number (e.g. REC-12345ABCD)
            self.receipt_number = f"REC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt: {self.receipt_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="ออเดอร์")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="สินค้า")
    quantity = models.IntegerField(default=1, verbose_name="จำนวน")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคาต่อหน่วย")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคารวม")

    class Meta:
        verbose_name = "รายการสินค้าในบิล"
        verbose_name_plural = "รายการสินค้าในบิล"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
