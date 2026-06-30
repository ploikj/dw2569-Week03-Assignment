import clickhouse_connect
from django.core.management.base import BaseCommand
from marketing.sales.models import OrderItem, Order
from django.db.models import F

class Command(BaseCommand):
    help = "Sync operational sales data from SQLite to ClickHouse Data Warehouse"

    def handle(self, *args, **options):
        self.stdout.write("Connecting to ClickHouse...")
        
        try:
            client = clickhouse_connect.get_client(host='localhost', port=8123, username='default', password='clickhouse')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to connect to ClickHouse: {e}"))
            return

        self.stdout.write("Creating Data Warehouse table...")
        client.command("""
            CREATE TABLE IF NOT EXISTS dw_sales (
                order_id UInt64,
                receipt_number String,
                created_at DateTime,
                cashier_name String,
                payment_method String,
                status String,
                product_id UInt64,
                product_name String,
                product_sku String,
                category_name String,
                quantity Int32,
                unit_price Float32,
                total_price Float32,
                tax Float32,
                order_total_amount Float32
            ) ENGINE = MergeTree()
            ORDER BY (created_at, category_name, product_name)
        """)

        # To support multiple syncs cleanly for this demo, we'll truncate first
        client.command("TRUNCATE TABLE dw_sales")

        self.stdout.write("Extracting data from SQLite...")
        # Optimize with select_related
        items = OrderItem.objects.select_related(
            'order', 'order__cashier', 'product', 'product__category'
        ).all().iterator(chunk_size=10000)

        batch = []
        batch_size = 50000
        total_synced = 0

        self.stdout.write("Transforming and Loading data to ClickHouse...")
        
        for item in items:
            cashier_name = item.order.cashier.username if item.order.cashier else 'Unknown'
            category_name = item.product.category.name if item.product.category else 'Uncategorized'
            
            row = [
                item.order.id,
                item.order.receipt_number,
                item.order.created_at,
                cashier_name,
                item.order.payment_method,
                item.order.status,
                item.product.id,
                item.product.name,
                item.product.sku,
                category_name,
                item.quantity,
                float(item.unit_price),
                float(item.total_price),
                float(item.order.tax),
                float(item.order.total_amount)
            ]
            batch.append(row)

            if len(batch) >= batch_size:
                client.insert('dw_sales', batch)
                total_synced += len(batch)
                self.stdout.write(f"  Inserted {total_synced} rows...")
                batch.clear()

        if batch:
            client.insert('dw_sales', batch)
            total_synced += len(batch)
            self.stdout.write(f"  Inserted {total_synced} rows...")

        self.stdout.write(self.style.SUCCESS(f"Successfully synced {total_synced} sales records to ClickHouse Data Warehouse!"))
