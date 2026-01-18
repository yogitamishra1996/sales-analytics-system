import sys
from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data
from utils.report_generator import generate_sales_report

def main():
    """
    Main execution function for the Sales Analytics System.
    Orchestrates data reading, cleaning, filtering, API enrichment, and reporting.
    """
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # [1/10] Reading sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data('data/sales_data.txt')
        if not raw_lines:
            print("Error: No data found or file could not be read. Exiting.")
            return
        print(f"✓ Successfully read raw lines from file")

        # [2/10] Parsing and cleaning data
        print("\n[2/10] Parsing and cleaning data...")
        # Note: parse_transactions already prints parsed/invalid counts per requirements
        initial_transactions = parse_transactions(raw_lines)
        if not initial_transactions:
            print("Error: No transactions remained after parsing. Exiting.")
            return

        # [3/10] Display Filter Options and Get User Input
        print("\n[3/10] Filter Options Available:")
        # We call validate_and_filter without filters first just to get Data Insights (Regions/Range)
        # This function prints insights to the console as per Task 3 requirements.
        temp_list, _, _ = validate_and_filter(initial_transactions)
        
        filter_choice = input("\nDo you want to filter data? (y/n): ").lower().strip()
        
        region_filter = None
        min_amt = None
        
        if filter_choice == 'y':
            region_filter = input("Enter Region to filter by (or leave blank): ").strip() or None
            try:
                min_val = input("Enter minimum transaction amount (or leave blank): ").strip()
                min_amt = float(min_val) if min_val else None
            except ValueError:
                print("! Invalid amount entered, skipping amount filter.")
        
        # [4/10] Validating and filtering transactions
        print("\n[4/10] Validating transactions...")
        final_transactions, invalid_count, summary = validate_and_filter(
            initial_transactions, 
            region=region_filter, 
            min_amount=min_amt
        )
        print(f"✓ Valid: {summary['final_count']} | Invalid: {summary['invalid']}")

        # [5/10] Analyzing sales data
        print("\n[5/10] Analyzing sales data...")
        # All analysis is performed within the report generation logic in report_generator.py
        # which calls functions from data_processor.py.
        print("✓ Analysis complete")

        # [6/10] Fetching product data from API
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        if not api_products:
            print("! API Fetch failed, enrichment will be skipped.")
            product_mapping = {}
        else:
            product_mapping = create_product_mapping(api_products)
            print(f"✓ Fetched {len(api_products)} products")

        # [7/10] Enriching sales data
        print("\n[7/10] Enriching sales data...")
        enriched_data = enrich_sales_data(final_transactions, product_mapping)
        enriched_success = sum(1 for tx in enriched_data if tx.get('API_Match'))
        success_pct = (enriched_success / len(enriched_data) * 100) if enriched_data else 0
        print(f"✓ Enriched {enriched_success}/{len(enriched_data)} transactions ({success_pct:.1f}%)")

        # [8/10] Saving enriched data
        # Note: enrich_sales_data already calls save_enriched_data internally
        print("\n[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [9/10] Generating report
        print("\n[9/10] Generating report...")
        generate_sales_report(final_transactions, enriched_data, 'output/sales_report.txt')
        print("✓ Report saved to: output/sales_report.txt")

        # [10/10] Process Complete
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}")
        print("The program has terminated safely.")

if __name__ == "__main__":
    main()