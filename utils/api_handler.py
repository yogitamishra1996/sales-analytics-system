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