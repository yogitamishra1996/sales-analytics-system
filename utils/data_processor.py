def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    Returns: float (total revenue)
    """
    # Sum of (Quantity * UnitPrice) for all records
    return sum(tx['Quantity'] * tx['UnitPrice'] for tx in transactions)


def region_wise_sales(transactions):
    """
    Analyzes sales by region, sorted by total_sales descending.
    """
    total_overall_revenue = calculate_total_revenue(transactions)
    region_stats = {}

    # Aggregate data by region
    for tx in transactions:
        region = tx['Region']
        revenue = tx['Quantity'] * tx['UnitPrice']
        
        if region not in region_stats:
            region_stats[region] = {'total_sales': 0.0, 'transaction_count': 0}
        
        region_stats[region]['total_sales'] += revenue
        region_stats[region]['transaction_count'] += 1

    # Calculate percentages and format
    for region, data in region_stats.items():
        # Correct percentage calculation: (Region Sales / Total Sales) * 100
        data['percentage'] = round((data['total_sales'] / total_overall_revenue) * 100, 2)

    # Sort by total_sales in descending order
    sorted_regions = dict(sorted(region_stats.items(), 
                                 key=lambda x: x[1]['total_sales'], 
                                 reverse=True))
    return sorted_regions


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue)
    """
    product_data = {}

    # Aggregate by ProductName
    for tx in transactions:
        name = tx['ProductName']
        qty = tx['Quantity']
        rev = qty * tx['UnitPrice']
        
        if name not in product_data:
            product_data[name] = {'qty': 0, 'rev': 0.0}
        
        product_data[name]['qty'] += qty
        product_data[name]['rev'] += rev

    # Convert to list of tuples for sorting
    product_list = [(name, data['qty'], data['rev']) for name, data in product_data.items()]

    # Sort by TotalQuantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Return top n products
    return product_list[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns, sorted by total_spent descending.
    """
    cust_data = {}

    for tx in transactions:
        cid = tx['CustomerID']
        revenue = tx['Quantity'] * tx['UnitPrice']
        product = tx['ProductName']
        
        if cid not in cust_data:
            cust_data[cid] = {
                'total_spent': 0.0, 
                'purchase_count': 0, 
                'products': set() # Use a set to ensure unique products
            }
        
        cust_data[cid]['total_spent'] += revenue
        cust_data[cid]['purchase_count'] += 1
        cust_data[cid]['products'].add(product)

    # Calculate metrics and format output
    final_analysis = {}
    for cid, data in cust_data.items():
        final_analysis[cid] = {
            'total_spent': round(data['total_spent'], 2),
            'purchase_count': data['purchase_count'],
            # Avg Order Value = Total Spent / Number of Purchases
            'avg_order_value': round(data['total_spent'] / data['purchase_count'], 2),
            'products_bought': sorted(list(data['products'])) # Unique product list
        }

    # Sort by total_spent descending
    sorted_customers = dict(sorted(final_analysis.items(), 
                                   key=lambda x: x[1]['total_spent'], 
                                   reverse=True))
    return sorted_customers

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date, sorted chronologically.
    
    Returns: dictionary sorted by date with revenue, count, and unique customers.
    """
    trend_data = {}

    for tx in transactions:
        date = tx['Date']
        revenue = tx['Quantity'] * tx['UnitPrice']
        customer = tx['CustomerID']
        
        if date not in trend_data:
            trend_data[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()  # Use set for unique count
            }
        
        trend_data[date]['revenue'] += revenue
        trend_data[date]['transaction_count'] += 1
        trend_data[date]['unique_customers'].add(customer)

    # Format the metrics and sort by date key
    sorted_trend = {}
    for date in sorted(trend_data.keys()):
        stats = trend_data[date]
        sorted_trend[date] = {
            'revenue': round(stats['revenue'], 2),
            'transaction_count': stats['transaction_count'],
            'unique_customers': len(stats['unique_customers'])
        }
    
    return sorted_trend


def find_peak_sales_day(transactions):
    """
    Identifies the date with the highest total revenue.
    
    Returns: tuple (date, revenue, transaction_count)
    """
    # Reuse the trend function to get daily metrics
    daily_stats = daily_sales_trend(transactions)
    
    if not daily_stats:
        return None

    # Find the date where revenue is the maximum
    peak_date = max(daily_stats, key=lambda d: daily_stats[d]['revenue'])
    peak_info = daily_stats[peak_date]
    
    return (peak_date, peak_info['revenue'], peak_info['transaction_count'])

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with total quantity sold below the threshold.
    
    Returns: list of tuples (ProductName, TotalQuantity, TotalRevenue) 
             sorted by TotalQuantity ascending.
    """
    perf_data = {}

    # Aggregate by ProductName
    for tx in transactions:
        name = tx['ProductName']
        qty = tx['Quantity']
        rev = qty * tx['UnitPrice']
        
        if name not in perf_data:
            perf_data[name] = {'qty': 0, 'rev': 0.0}
        
        perf_data[name]['qty'] += qty
        perf_data[name]['rev'] += rev

    # Filter by threshold and convert to list of tuples
    low_performers = [
        (name, data['qty'], round(data['rev'], 2)) 
        for name, data in perf_data.items() 
        if data['qty'] < threshold
    ]

    # Sort by TotalQuantity ascending
    low_performers.sort(key=lambda x: x[1])

    return low_performers