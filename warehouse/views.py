from django.shortcuts import render
import clickhouse_connect
from decimal import Decimal
import json

def get_clickhouse_client():
    try:
        return clickhouse_connect.get_client(host='localhost', port=8123, username='default', password='clickhouse')
    except Exception:
        return None

def dashboard(request):
    client = get_clickhouse_client()
    
    context = {
        'total_revenue': 0,
        'total_orders': 0,
        'top_categories': [],
        'monthly_revenue_labels': [],
        'monthly_revenue_data': []
    }

    if client:
        try:
            # Key Metrics
            metrics_result = client.query("SELECT sum(total_price), count(distinct order_id) FROM dw_sales")
            if metrics_result.result_rows and metrics_result.result_rows[0]:
                context['total_revenue'] = f"{metrics_result.result_rows[0][0] or 0:,.2f}"
                context['total_orders'] = f"{metrics_result.result_rows[0][1] or 0:,}"

            # Top Categories
            cat_result = client.query("SELECT category_name, sum(total_price) as rev FROM dw_sales GROUP BY category_name ORDER BY rev DESC LIMIT 5")
            context['top_categories'] = [{'name': row[0], 'revenue': f"{row[1]:,.2f}"} for row in cat_result.result_rows]

            # Monthly Revenue Trend
            trend_result = client.query("SELECT toStartOfMonth(created_at) as month, sum(total_price) as rev FROM dw_sales GROUP BY month ORDER BY month")
            
            labels = []
            data = []
            for row in trend_result.result_rows:
                # row[0] is a datetime object
                labels.append(row[0].strftime("%b %Y"))
                data.append(float(row[1]))
                
            context['monthly_revenue_labels'] = json.dumps(labels)
            context['monthly_revenue_data'] = json.dumps(data)

        except Exception as e:
            print(f"ClickHouse Query Error: {e}")

    return render(request, 'warehouse/dashboard.html', context)
