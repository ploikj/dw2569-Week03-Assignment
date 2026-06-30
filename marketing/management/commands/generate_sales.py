import random
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from marketing.sales.models import Category, Product, Order, OrderItem


class Command(BaseCommand):
    help = "Generate fake sales transactions from 2024 to 2026"

    def add_arguments(self, parser):
        parser.add_argument('--total', type=int, default=200000, help='Total transactions')
        parser.add_argument('--batch-size', type=int, default=500, help='Batch size')

    def handle(self, *args, **options):
        total = options['total']
        batch_size = options['batch_size']

        products = list(self._ensure_products())
        cashiers = list(self._ensure_cashiers())

        if not products:
            self.stderr.write(self.style.ERROR('No products available. Aborting.'))
            return

        start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
        end_date = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        date_span = (end_date - start_date).total_seconds()

        payment_methods = ['CASH', 'CREDIT_CARD', 'PROMPTPAY', 'OTHER']
        statuses = ['COMPLETED', 'PENDING', 'CANCELLED']
        status_weights = [0.85, 0.10, 0.05]

        self.stdout.write(f'Generating {total} sales transactions...')
        self.stdout.flush()

        created = 0
        order_batch = []
        item_batch = []

        while created < total:
            current_batch = min(batch_size, total - created)

            for _ in range(current_batch):
                cashier = random.choice(cashiers)
                payment_method = random.choice(payment_methods)
                status = random.choices(statuses, weights=status_weights, k=1)[0]

                order_batch.append(Order(
                    receipt_number=f"REC-{uuid.uuid4().hex[:16].upper()}",
                    cashier=cashier,
                    subtotal=Decimal('0'),
                    tax=Decimal('0'),
                    total_amount=Decimal('0'),
                    payment_method=payment_method,
                    status=status,
                ))

            Order.objects.bulk_create(order_batch)

            # bulk_create overrides auto_now_add fields, so fix created_at
            for order in order_batch:
                random_seconds = random.randint(0, int(date_span))
                order.created_at = start_date + timedelta(seconds=random_seconds)
            Order.objects.bulk_update(order_batch, ['created_at'])

            for order in order_batch:
                num_items = random.randint(1, 5)
                order_subtotal = Decimal('0')
                for _ in range(num_items):
                    product = random.choice(products)
                    quantity = random.randint(1, 10)
                    unit_price = product.price
                    total_price = (quantity * unit_price).quantize(Decimal('0.00'))
                    order_subtotal += total_price
                    item_batch.append(OrderItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                    ))

                tax = (order_subtotal * Decimal('0.07')).quantize(Decimal('0.00'))
                total_amount = order_subtotal + tax
                Order.objects.filter(pk=order.pk).update(
                    subtotal=order_subtotal,
                    tax=tax,
                    total_amount=total_amount,
                )

            OrderItem.objects.bulk_create(item_batch)

            created += current_batch
            self.stdout.write(f'  Created {created}/{total}')
            self.stdout.flush()

            order_batch.clear()
            item_batch.clear()

        self.stdout.write(self.style.SUCCESS(f'Done: {total} transactions generated.'))

    def _ensure_products(self):
        products = Product.objects.all()
        if products.exists():
            self.stdout.write(f'Using {products.count()} existing products')
            return products

        self.stdout.write('Creating sample products...')
        cat, _ = Category.objects.get_or_create(
            name='General',
            defaults={'description': 'General products', 'is_active': True},
        )

        sample_products = [
            {'name': 'Coffee', 'price': 55},
            {'name': 'Tea', 'price': 35},
            {'name': 'Sandwich', 'price': 80},
            {'name': 'Cake', 'price': 120},
            {'name': 'Juice', 'price': 45},
            {'name': 'Cookie', 'price': 25},
            {'name': 'Muffin', 'price': 60},
            {'name': 'Salad', 'price': 95},
            {'name': 'Pasta', 'price': 150},
            {'name': 'Pizza', 'price': 200},
        ]

        for sp in sample_products:
            Product.objects.get_or_create(
                name=sp['name'],
                defaults={
                    'category': cat,
                    'sku': f'SKU-{uuid.uuid4().hex[:6].upper()}',
                    'price': sp['price'],
                    'stock_quantity': random.randint(50, 500),
                    'is_active': True,
                },
            )

        products = Product.objects.all()
        self.stdout.write(f'Created {products.count()} products')
        return products

    def _ensure_cashiers(self):
        cashiers = User.objects.filter(is_staff=True)
        if cashiers.exists():
            self.stdout.write(f'Using {cashiers.count()} existing cashiers')
            return cashiers

        self.stdout.write('Creating sample cashiers...')
        names = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve']
        for name in names:
            User.objects.get_or_create(
                username=name.lower(),
                defaults={
                    'first_name': name,
                    'last_name': 'Staff',
                    'is_staff': True,
                    'email': f'{name.lower()}@shop.local',
                },
            )

        cashiers = User.objects.filter(is_staff=True)
        self.stdout.write(f'Created {cashiers.count()} cashiers')
        return cashiers
