"""
Standalone CLI script to generate sale records.
Usage: python generate_sale.py [--total 200000] [--batch-size 500]
"""

import argparse
import os
import random
import sys
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wichit2s.settings')
django.setup()

from django.contrib.auth.models import User

from marketing.sales.models import Category, Product, Order, OrderItem


def ensure_products():
    products = Product.objects.all()
    if products.exists():
        print(f'Using {products.count()} existing products')
        return list(products)

    print('Creating sample products...')
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
    print(f'Created {products.count()} products')
    return list(products)


def ensure_cashiers():
    cashiers = User.objects.filter(is_staff=True)
    if cashiers.exists():
        print(f'Using {cashiers.count()} existing cashiers')
        return list(cashiers)

    print('Creating sample cashiers...')
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
    print(f'Created {cashiers.count()} cashiers')
    return list(cashiers)


def generate_sales(total=200000, batch_size=500):
    products = ensure_products()
    cashiers = ensure_cashiers()

    if not products:
        print('No products available. Aborting.', file=sys.stderr)
        return

    start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    date_span = (end_date - start_date).total_seconds()

    payment_methods = ['CASH', 'CREDIT_CARD', 'PROMPTPAY', 'OTHER']
    statuses = ['COMPLETED', 'PENDING', 'CANCELLED']
    status_weights = [0.80, 0.12, 0.08]

    print(f'Generating {total} sales transactions (80% completed)...')
    sys.stdout.flush()

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
        print(f'  Created {created}/{total}')
        sys.stdout.flush()

        order_batch.clear()
        item_batch.clear()

    print(f'Done: {total} transactions generated.')


def main():
    parser = argparse.ArgumentParser(description='Generate fake sale records')
    parser.add_argument('--total', type=int, default=200000, help='Total transactions (default: 200000)')
    parser.add_argument('--batch-size', type=int, default=500, help='Batch size (default: 500)')
    args = parser.parse_args()

    generate_sales(total=args.total, batch_size=args.batch_size)


if __name__ == '__main__':
    main()
