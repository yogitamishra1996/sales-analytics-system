import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API using limit=100.
    Returns: list of product dictionaries or an empty list if API fails.
    """
    url = "https://dummyjson.com/products?limit=100"
    try:
        response = requests.get(url, timeout=10)
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"Success: Fetched {len(products)} products from API.")
            return products
        else:
            print(f"Failure: API returned status code {response.status_code}.")
            return []
    except requests.exceptions.RequestException as e:
        # Handles connection errors, timeouts, etc.
        print(f"Failure: A connection error occurred: {e}")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.
    """
    mapping = {}
    for product in api_products:
        # Using the structure: {id: {'title': ..., 'category': ..., 'brand': ..., 'rating': ...}}
        mapping[product['id']] = {
            'title': product.get('title'),
            'category': product.get('category'),
            'brand': product.get('brand'),
            'rating': product.get('rating')
        }
    return mapping


import os

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.
    """
    enriched_list = []
    
    for tx in transactions:
        # Extract numeric ID from ProductID (e.g., P101 -> 101)
        raw_id = tx.get('ProductID', '')
        # Remove the 'P' prefix and convert to int
        numeric_id = None
        try:
            numeric_id = int(''.join(filter(str.isdigit, raw_id)))
        except ValueError:
            pass

        # Enrich based on mapping
        if numeric_id in product_mapping:
            info = product_mapping[numeric_id]
            tx['API_Category'] = info['category']
            tx['API_Brand'] = info['brand']
            tx['API_Rating'] = info['rating']
            tx['API_Match'] = True
        else:
            # Set to None if no match found
            tx['API_Category'] = None
            tx['API_Brand'] = None
            tx['API_Rating'] = None
            tx['API_Match'] = False
            
        enriched_list.append(tx)
    
    # Save the data after enrichment
    save_enriched_data(enriched_list)
    return enriched_list

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to a pipe-delimited file.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    headers = ['TransactionID', 'Date', 'ProductID', 'ProductName', 'Quantity', 
               'UnitPrice', 'CustomerID', 'Region', 'API_Category', 'API_Brand', 
               'API_Rating', 'API_Match']
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Write Header
            f.write('|'.join(headers) + '\n')
            
            # Write Records
            for tx in enriched_transactions:
                row = []
                for h in headers:
                    val = tx.get(h, '')
                    # Handle None values appropriately by converting to empty string or 'None'
                    row.append(str(val) if val is not None else "None")
                f.write('|'.join(row) + '\n')
        print(f"Successfully saved enriched data to {filename}")
    except Exception as e:
        print(f"Error saving enriched data: {e}")