from datetime import datetime
import os

# Import the analytical functions we built in Part 2
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report combining all analytical metrics.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Prepare Data for sections
    total_rev = calculate_total_revenue(transactions)
    total_tx = len(transactions)
    avg_order = total_rev / total_tx if total_tx > 0 else 0
    
    trends = daily_sales_trend(transactions)
    dates = sorted(trends.keys())
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"
    
    regions = region_wise_sales(transactions)
    top_prods = top_selling_products(transactions, n=5)
    top_custs = customer_analysis(transactions) # This is already sorted descending
    peak_day = find_peak_sales_day(transactions)
    low_performers = low_performing_products(transactions, threshold=10)

    # API Enrichment Metrics
    enriched_count = sum(1 for tx in enriched_transactions if tx.get('API_Match'))
    success_rate = (enriched_count / total_tx * 100) if total_tx > 0 else 0
    failed_products = sorted(list(set(tx['ProductName'] for tx in enriched_transactions if not tx.get('API_Match'))))

    with open(output_file, 'w', encoding='utf-8') as f:
        # 1. HEADER
        f.write("=" * 60 + "\n")
        f.write(f"{'SALES ANALYTICS REPORT':^60}\n")
        f.write(f"{'Generated: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^60}\n")
        f.write(f"{'Records Processed: ' + str(total_tx):^60}\n")
        f.write("=" * 60 + "\n\n")

        # 2. OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total Revenue:       ${total_rev:,.2f}\n")
        f.write(f"Total Transactions:  {total_tx}\n")
        f.write(f"Average Order Value: ${avg_order:,.2f}\n")
        f.write(f"Date Range:          {date_range}\n\n")

        # 3. REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Region':<15} {'Sales':<15} {'% of Total':<15} {'Transactions':<10}\n")
        for reg, data in regions.items():
            f.write(f"{reg:<15} ${data['total_sales']:<14,.2f} {data['percentage']:<14}% {data['transaction_count']:<10}\n")
        f.write("\n")

        # 4. TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Rank':<6} {'Product Name':<25} {'Qty Sold':<12} {'Revenue':<15}\n")
        for i, (name, qty, rev) in enumerate(top_prods, 1):
            f.write(f"{i:<6} {name:<25} {qty:<12} ${rev:,.2f}\n")
        f.write("\n")

        # 5. TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<20} {'Orders':<10}\n")
        for i, (cid, data) in enumerate(list(top_custs.items())[:5], 1):
            f.write(f"{i:<6} {cid:<15} ${data['total_spent']:<19,.2f} {data['purchase_count']:<10}\n")
        f.write("\n")

        # 6. DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Date':<15} {'Revenue':<15} {'Transactions':<15} {'Customers':<10}\n")
        for date in dates:
            d = trends[date]
            f.write(f"{date:<15} ${d['revenue']:<14,.2f} {d['transaction_count']:<15} {d['unique_customers']:<10}\n")
        f.write("\n")

        # 7. PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 60 + "\n")
        if peak_day:
            f.write(f"Peak Sales Day: {peak_day[0]} (Revenue: ${peak_day[1]:,.2f}, TX: {peak_day[2]})\n")
        
        f.write(f"Low Performing Products (<10 units): ")
        if low_performers:
            f.write(", ".join([p[0] for p in low_performers]) + "\n")
        else:
            f.write("None\n")
        
        f.write("\nAvg Transaction Value per Region:\n")
        for reg, data in regions.items():
            atv = data['total_sales'] / data['transaction_count']
            f.write(f" - {reg}: ${atv:,.2f}\n")
        f.write("\n")

        # 8. API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate:            {success_rate:.2f}%\n")
        if failed_products:
            f.write(f"Products Not Found in API: {', '.join(failed_products)}\n")
        f.write("-" * 60 + "\n")

    print(f"Comprehensive report successfully generated at: {output_file}")