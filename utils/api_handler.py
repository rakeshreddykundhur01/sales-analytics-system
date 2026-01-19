import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = []

        for item in data.get('products', []):
            products.append({
                'id': item.get('id'),
                'title': item.get('title'),
                'category': item.get('category'),
                'brand': item.get('brand'),
                'price': item.get('price'),
                'rating': item.get('rating')
            })

        print(f"✓ Successfully fetched {len(products)} products from API")
        return products

    except requests.exceptions.RequestException as e:
        print("❌ Failed to fetch products from API:", e)
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """
    mapping = {}

    for product in api_products:
        pid = product.get('id')
        if pid is not None:
            mapping[pid] = {
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'rating': product.get('rating')
            }

    return mapping

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """
    enriched = []

    for t in transactions:
        try:
            numeric_id = int(t['ProductID'][1:])  # e.g., P101 -> 101
            product_info = product_mapping.get(numeric_id, None)

            if product_info:
                t['API_Category'] = product_info.get('category')
                t['API_Brand'] = product_info.get('brand')
                t['API_Rating'] = product_info.get('rating')
                t['API_Match'] = True
            else:
                t['API_Category'] = None
                t['API_Brand'] = None
                t['API_Rating'] = None
                t['API_Match'] = False

        except Exception:
            t['API_Category'] = None
            t['API_Brand'] = None
            t['API_Rating'] = None
            t['API_Match'] = False

        enriched.append(t)

    return enriched

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """
    header = [
        'TransactionID', 'Date', 'ProductID', 'ProductName', 'Quantity',
        'UnitPrice', 'CustomerID', 'Region', 'API_Category', 'API_Brand',
        'API_Rating', 'API_Match'
    ]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write('|'.join(header) + '\n')
        for t in enriched_transactions:
            row = [
                t.get('TransactionID', ''),
                t.get('Date', ''),
                t.get('ProductID', ''),
                t.get('ProductName', ''),
                str(t.get('Quantity', '')),
                str(t.get('UnitPrice', '')),
                t.get('CustomerID', ''),
                t.get('Region', ''),
                str(t.get('API_Category', '')),
                str(t.get('API_Brand', '')),
                str(t.get('API_Rating', '')),
                str(t.get('API_Match', ''))
            ]
            f.write('|'.join(row) + '\n')

    print(f"✓ Enriched data saved to {filename}")
