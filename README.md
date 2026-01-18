# Sales Data Analytics System

A Python-based data processing system designed for e-commerce sales analysis. The system reads messy transaction data from localized files, enriches it with real-time product information from an external API, performs advanced business analytics, and generates a detailed performance report.

## 📁 Project Structure

```text
sales-analytics-system/
├── data/
│   ├── sales_data.txt          # Input transaction data
│   └── enriched_sales_data.txt # Output of API enrichment
├── output/
│   └── sales_report.txt        # Final comprehensive business report
├── utils/
│   ├── __init__.py             # Package initializer
│   ├── api_handler.py          # DummyJSON API integration
│   ├── data_processor.py       # Sales metrics and trend analysis
│   ├── file_handler.py         # File I/O and data cleaning
│   └── report_generator.py     # Professional report formatting
├── main.py                     # Main execution script
├── requirements.txt            # Project dependencies
└── README.md                   # System documentation
```

## 🚀 Key Features

- [cite_start]**Robust Data Cleaning:** Handles non-UTF-8 encodings, removes commas from numeric strings, and filters out invalid records (e.g., negative prices, zero quantities)[cite: 1, 3, 20].
- [cite_start]**Dynamic Filtering:** Allows users to filter analysis results by region or minimum transaction amount via interactive console prompts.
- [cite_start]**API Enrichment:** Integrates with the `DummyJSON` API to fetch product brands, categories, and ratings based on transaction IDs[cite: 1, 2].
- [cite_start]**Comprehensive Analytics:** Calculates total revenue, regional performance, top-selling products, customer purchase patterns, and daily trends[cite: 1].
- [cite_start]**Professional Reporting:** Generates a structured `.txt` report including 8 distinct business sections with formatted tables[cite: 1, 2].

---

## 🛠️ Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yogitamishra1996/sales-analytics-system
   cd sales-analytics-system
   ```
