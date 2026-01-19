import datetime

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    
    from utils.data_processor import (
        calculate_total_revenue,
        region_wise_sales,
        top_selling_products,
        customer_analysis,
        daily_sales_trend,
        find_peak_sales_day,
        low_performing_products
    )

    total_revenue = calculate_total_revenue(transactions)
    total_txns = len(transactions)
    avg_order = total_revenue / total_txns if total_txns else 0

    date_range = sorted([t['Date'] for t in transactions])
    start_date = date_range[0] if date_range else ''
    end_date = date_range[-1] if date_range else ''

    region_stats = region_wise_sales(transactions)
    top_products = top_selling_products(transactions)
    top_customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day, peak_revenue, peak_count = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    # API enrichment stats
    enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
    total_enriched = len(enriched_transactions)
    success_rate = round((enriched_count / total_enriched) * 100, 2) if total_enriched else 0
    failed_products = [t['ProductID'] for t in enriched_transactions if not t.get('API_Match')]

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*50 + "\n")
        f.write("       SALES ANALYTICS REPORT\n")
        f.write(f"     Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"     Records Processed: {total_txns}\n")
        f.write("="*50 + "\n\n")

        # Overall Summary
        f.write("OVERALL SUMMARY\n")
        f.write("-"*50 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_txns}\n")
        f.write(f"Average Order Value:  ₹{avg_order:,.2f}\n")
        f.write(f"Date Range:           {start_date} to {end_date}\n\n")

        # Region-wise
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-"*50 + "\n")
        f.write(f"{'Region':10}{'Sales':15}{'% of Total':12}{'Transactions':12}\n")
        for region, stats in region_stats.items():
            f.write(f"{region:10}₹{stats['total_sales']:,.2f}{stats['percentage']:12.2f}%{stats['transaction_count']:12}\n")
        f.write("\n")

        # Top Products
        f.write("TOP 5 PRODUCTS\n")
        f.write("-"*50 + "\n")
        f.write(f"{'Rank':5}{'Product':20}{'Quantity':10}{'Revenue':12}\n")
        for i, (name, qty, rev) in enumerate(top_products, 1):
            f.write(f"{i:<5}{name:20}{qty:<10}₹{rev:<12,.2f}\n")
        f.write("\n")

        # Top Customers
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-"*50 + "\n")
        f.write(f"{'Rank':5}{'CustomerID':12}{'Total Spent':15}{'Orders':10}\n")
        for i, (cid, data) in enumerate(list(top_customers.items())[:5], 1):
            f.write(f"{i:<5}{cid:12}₹{data['total_spent']:<15,.2f}{data['purchase_count']:<10}\n")
        f.write("\n")

        # Daily Trend
        f.write("DAILY SALES TREND\n")
        f.write("-"*50 + "\n")
        f.write(f"{'Date':12}{'Revenue':15}{'Transactions':15}{'Unique Customers':15}\n")
        for date, stats in daily_trend.items():
            f.write(f"{date:12}₹{stats['revenue']:<15,.2f}{stats['transaction_count']:<15}{stats['unique_customers']:<15}\n")
        f.write("\n")

        # Product Performance
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-"*50 + "\n")
        f.write(f"Peak Sales Day: {peak_day} | Revenue: ₹{peak_revenue:,.2f} | Transactions: {peak_count}\n")
        f.write("Low Performing Products:\n")
        for name, qty, rev in low_products:
            f.write(f"{name:20} Qty: {qty:<5} Revenue: ₹{rev:,.2f}\n")
        f.write("\n")

        # API Enrichment
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-"*50 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}/{total_enriched}\n")
        f.write(f"Success Rate: {success_rate}%\n")
        f.write(f"Products not enriched: {', '.join(failed_products)}\n")

    print(f"✓ Report saved to {output_file}")
