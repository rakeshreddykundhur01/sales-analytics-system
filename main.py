from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data, save_enriched_data
from utils.report_generator import generate_sales_report 

def main():
    try:
        print("="*40)
        print("         SALES ANALYTICS SYSTEM")
        print("="*40, "\n")

        # Step 1: Read & Parse
        print("[1/10] Reading sales data...")
        raw = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw)} transactions\n")

        print("[2/10] Parsing and cleaning data...")
        parsed = parse_transactions(raw)
        print(f"✓ Parsed {len(parsed)} records\n")

        # Step 2: Validate & Filter
        print("[3/10] Validating transactions...")
        valid, invalid_count, summary = validate_and_filter(parsed)
        print(f"✓ Valid: {len(valid)} | Invalid: {invalid_count}\n")

        # Step 3: Data Analysis
        print("[4/10] Analyzing sales data...")
        total_revenue = calculate_total_revenue(valid)
        region_stats = region_wise_sales(valid)
        top_products = top_selling_products(valid)
        top_customers = customer_analysis(valid)
        daily_trend = daily_sales_trend(valid)
        peak_day, peak_revenue, peak_count = find_peak_sales_day(valid)
        low_products = low_performing_products(valid)
        print("✓ Analysis complete\n")

        # Step 4: API Integration
        print("[5/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_map = create_product_mapping(api_products)
        print("✓ Product mapping created\n")

        print("[6/10] Enriching sales data...")
        enriched = enrich_sales_data(valid, product_map)
        save_enriched_data(enriched)
        print("✓ Enrichment complete\n")

        # Step 5: Generate report
        print("[7/10] Generating report...")
        generate_sales_report(valid, enriched)
        print("✓ Report generation complete\n")

        print("[8/10] Process Complete!")
        print("="*40)

    except Exception as e:
        print("❌ An error occurred:", e)

if __name__ == "__main__":
    main()
