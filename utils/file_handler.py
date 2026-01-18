import os

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.

    Returns: list of raw lines (strings)

    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    raw_lines = []

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        return []

    for encoding in encodings:
        try:
            with open(filename, mode='r', encoding=encoding) as file:
                # Read all lines from the file
                lines = file.readlines()
                
                # If we successfully read lines, process them
                if lines:
                    # Skip header (index 0) and filter out empty strings/whitespace-only lines
                    raw_lines = [line.strip() for line in lines[1:] if line.strip()]
                    break  # Exit loop if encoding works
        except (UnicodeDecodeError, UnicodeError):
            continue  # Try the next encoding if this one fails
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    return raw_lines

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.
    
    Returns: list of dictionaries with clean data and correct types.
    """
    cleaned_data = []
    total_parsed = 0
    invalid_removed = 0

    for line in raw_lines:
        total_parsed += 1
        # Split by pipe delimiter '|' 
        parts = line.split('|')

        # Skip rows with incorrect number of fields (Expected: 8) 
        if len(parts) != 8:
            invalid_removed += 1
            continue

        try:
            # Extract fields
            transaction_id = parts[0].strip()
            date = parts[1].strip()
            product_id = parts[2].strip()
            
            # 1. Handle commas within ProductName (Remove commas)
            product_name = parts[3].replace(',', '').strip()
            
            # 2. Handle commas in numeric fields (Remove commas)
            # 3. Convert Quantity to int
            quantity_str = parts[4].replace(',', '').strip()
            quantity = int(quantity_str)
            
            # 4. Convert UnitPrice to float
            unit_price_str = parts[5].replace(',', '').strip()
            unit_price = float(unit_price_str)
            
            customer_id = parts[6].strip()
            region = parts[7].strip()

            # Data Validation Criteria:
            # - TransactionID must start with 'T'
            # - Quantity > 0
            # - UnitPrice > 0
            # - CustomerID and Region must not be empty
            if (not transaction_id.startswith('T') or 
                quantity <= 0 or 
                unit_price <= 0 or 
                not customer_id or 
                not region):
                invalid_removed += 1
                continue

            # Build record dictionary
            record = {
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Region': region
            }
            cleaned_data.append(record)

        except (ValueError, IndexError):
            # Handles cases where conversion fails (e.g., non-numeric strings)
            invalid_removed += 1
            continue

    # Validation Output Required
    print(f"Total records parsed: {total_parsed}")
    print(f"Invalid records removed: {invalid_removed}")
    print(f"Valid records after cleaning: {len(cleaned_data)}")

    return cleaned_data

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    
    Returns: tuple (filtered_transactions, invalid_count, filter_summary)
    """
    # 1. Validation Logic
    valid_transactions = []
    invalid_count = 0
    
    required_keys = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
                     'Quantity', 'UnitPrice', 'CustomerID', 'Region']

    for tx in transactions:
        # Check all required fields are present
        if not all(key in tx for key in required_keys):
            invalid_count += 1
            continue
            
        # Validation Rules
        is_valid = (
            tx['Quantity'] > 0 and
            tx['UnitPrice'] > 0 and
            tx['TransactionID'].startswith('T') and
            tx['ProductID'].startswith('P') and
            tx['CustomerID'].startswith('C')
        )
        
        if is_valid:
            valid_transactions.append(tx)
        else:
            invalid_count += 1

    # 2. Display Information to User
    available_regions = sorted(list(set(tx['Region'] for tx in valid_transactions)))
    total_amounts = [tx['Quantity'] * tx['UnitPrice'] for tx in valid_transactions]
    
    print("\n--- Data Insights ---")
    print(f"Available Regions: {', '.join(available_regions)}")
    if total_amounts:
        print(f"Transaction Amount Range: ${min(total_amounts):,.2f} - ${max(total_amounts):,.2f}")

    # 3. Apply Filters
    filtered_list = valid_transactions
    
    # Filter by Region
    region_filtered_count = 0
    if region:
        initial_count = len(filtered_list)
        filtered_list = [tx for tx in filtered_list if tx['Region'].lower() == region.lower()]
        region_filtered_count = initial_count - len(filtered_list)
        print(f"Records after region filter: {len(filtered_list)}")

    # Filter by Amount
    amount_filtered_count = 0
    if min_amount is not None or max_amount is not None:
        initial_count = len(filtered_list)
        temp_list = []
        for tx in filtered_list:
            total = tx['Quantity'] * tx['UnitPrice']
            if (min_amount is None or total >= min_amount) and \
               (max_amount is None or total <= max_amount):
                temp_list.append(tx)
        
        amount_filtered_count = initial_count - len(temp_list)
        filtered_list = temp_list
        print(f"Records after amount filter: {len(filtered_list)}")

    # 4. Prepare Summary
    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': region_filtered_count,
        'filtered_by_amount': amount_filtered_count,
        'final_count': len(filtered_list)
    }

    return filtered_list, invalid_count, filter_summary