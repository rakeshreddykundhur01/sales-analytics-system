def calculate_total_revenue(transactions):
    
    total_revenue = 0.0

    for t in transactions:
        total_revenue += t['Quantity'] * t['UnitPrice']

    return total_revenue

def region_wise_sales(transactions):
    
    region_data = {}
    total_revenue = 0.0

    # Calculate total revenue
    for t in transactions:
        total_revenue += t['Quantity'] * t['UnitPrice']

    # Aggregate by region
    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1

    # Calculate percentages
    for region in region_data:
        region_data[region]['percentage'] = round(
            (region_data[region]['total_sales'] / total_revenue) * 100, 2
        )

    # Sort by total_sales descending
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda item: item[1]['total_sales'],
            reverse=True
        )
    )

    return sorted_regions

def top_selling_products(transactions, n=5):
    
    product_data = {}

    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']

        if name not in product_data:
            product_data[name] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_data[name]['total_quantity'] += qty
        product_data[name]['total_revenue'] += revenue

    # Convert to list of tuples
    product_list = [
        (name,
         data['total_quantity'],
         data['total_revenue'])
        for name, data in product_data.items()
    ]

    # Sort by total_quantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)

    return product_list[:n]

def customer_analysis(transactions):
    
    customer_data = {}

    for t in transactions:
        cid = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        product = t['ProductName']

        if cid not in customer_data:
            customer_data[cid] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }

        customer_data[cid]['total_spent'] += amount
        customer_data[cid]['purchase_count'] += 1
        customer_data[cid]['products_bought'].add(product)

    # Final formatting
    for cid in customer_data:
        total = customer_data[cid]['total_spent']
        count = customer_data[cid]['purchase_count']

        customer_data[cid]['avg_order_value'] = round(total / count, 2)
        customer_data[cid]['products_bought'] = list(customer_data[cid]['products_bought'])

    # Sort by total_spent descending
    sorted_customers = dict(
        sorted(
            customer_data.items(),
            key=lambda item: item[1]['total_spent'],
            reverse=True
        )
    )

    return sorted_customers

def daily_sales_trend(transactions):
    
    daily_data = {}

    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        customer = t['CustomerID']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }

        daily_data[date]['revenue'] += amount
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(customer)

    # Final formatting
    for date in daily_data:
        daily_data[date]['unique_customers'] = len(daily_data[date]['customers'])
        del daily_data[date]['customers']

    # Sort by date
    sorted_daily = dict(sorted(daily_data.items()))

    return sorted_daily

def find_peak_sales_day(transactions):
    
    daily_data = {}

    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']

        if date not in daily_data:
            daily_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0
            }

        daily_data[date]['revenue'] += amount
        daily_data[date]['transaction_count'] += 1

    peak_date = None
    max_revenue = 0.0
    peak_txn_count = 0

    for date, stats in daily_data.items():
        if stats['revenue'] > max_revenue:
            max_revenue = stats['revenue']
            peak_date = date
            peak_txn_count = stats['transaction_count']

    return peak_date, max_revenue, peak_txn_count

def low_performing_products(transactions, threshold=10):
    
    product_data = {}

    for t in transactions:
        name = t['ProductName']
        qty = t['Quantity']
        revenue = t['Quantity'] * t['UnitPrice']

        if name not in product_data:
            product_data[name] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_data[name]['total_quantity'] += qty
        product_data[name]['total_revenue'] += revenue

    low_products = []

    for name, data in product_data.items():
        if data['total_quantity'] < threshold:
            low_products.append(
                (name, data['total_quantity'], data['total_revenue'])
            )

    # Sort by total_quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products
