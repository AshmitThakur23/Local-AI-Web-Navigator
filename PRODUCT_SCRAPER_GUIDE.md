# 🛍️ Product Scraper Feature - Complete Guide

## Overview

The **Product Scraper** is a powerful feature that allows you to search for products online and extract structured JSON data from multiple websites in batches. Perfect for price comparisons, product research, and data collection.

---

## 🎯 What It Does

When you search for products (e.g., "top 20 laptops under 60000"), the scraper will:

1. **Search the web** using your query (via DuckDuckGo/Bing)
2. **Extract structured data** from each product page
3. **Process in batches** of 5 items at a time
4. **Display JSON data** progressively on the frontend
5. **Store results** locally for later access

---

## 📦 Batch Processing

### Why Batches?
- **Progressive Loading**: See results as they come in (5 at a time)
- **Better Performance**: Avoid overwhelming your browser
- **Rate Limiting**: Be polite to websites (avoid getting blocked)
- **Error Recovery**: If one batch fails, others continue

### Default Settings
- **Batch Size**: 5 products per batch
- **Total Limit**: 20 products (configurable)
- **Delay**: 0.5 seconds between requests

---

## 🔍 Extracted Data Structure

Each scraped product returns a JSON object with:

```json
{
  "url": "https://example.com/product",
  "title": "Product Name",
  "meta_description": "Product description from meta tags",
  "headings": {
    "h1": ["Main Heading"],
    "h2": ["Subheading 1", "Subheading 2"],
    "h3": ["Feature 1", "Feature 2"]
  },
  "links": [
    {
      "text": "More Info",
      "href": "https://example.com/more"
    }
  ],
  "paragraphs": [
    "Product description paragraph...",
    "Features and specifications..."
  ],
  "json_ld": [
    {
      "context": "https://schema.org",
      "type": "Product",
      "name": "Product Name"
    }
  ],
  "product_info": {
    "brand": "Dell",
    "model": "XPS 15",
    "specifications": "Intel i7, 16GB RAM..."
  },
  "images": [
    {
      "src": "https://example.com/image.jpg",
      "alt": "Product image"
    }
  ],
  "price": "₹55,999",
  "rating": "4.5/5",
  "search_snippet": "Original search result snippet",
  "search_title": "Original search result title",
  "batch_number": 1,
  "item_number": 1
}
```

---

## 🚀 How to Use

### Method 1: Via Web Interface

1. **Open the Product Scraper**
   - From main Nexus AI page, click **"🛍️ Product Scraper"** button
   - Or navigate directly to: `http://localhost:5000/scraper.html`

2. **Enter Your Query**
   ```
   top 20 laptops under 60000
   best smartphones under 30000
   gaming laptops 2025
   ```

3. **Configure Settings** (optional)
   - **Total Items**: 5-50 (default: 20)
   - **Batch Size**: 3-10 (default: 5)

4. **Click "Start Scraping"**

5. **View Results**
   - Results appear in batches
   - Each product card shows:
     - Product title and URL
     - Price and rating (if found)
     - Image count
     - JSON preview
   - Click **"View Full JSON"** to expand

### Method 2: Via API

#### Scrape Multiple Products

```bash
POST http://localhost:5000/scrape_products
Content-Type: application/json

{
  "query": "top 20 laptops under 60000",
  "limit": 20,
  "batch_size": 5
}
```

**Response:**
```json
{
  "success": true,
  "query": "top 20 laptops under 60000",
  "total_items": 20,
  "total_batches": 4,
  "batches": [
    {
      "batch_number": 1,
      "total_batches": 4,
      "items": [ /* 5 product objects */ ],
      "progress": "5/20"
    },
    // ... more batches
  ]
}
```

#### Scrape Single URL

```bash
POST http://localhost:5000/scrape_single
Content-Type: application/json

{
  "url": "https://example.com/product"
}
```

**Response:**
```json
{
  "success": true,
  "data": { /* structured product data */ }
}
```

---

## 📁 File Structure

```
backend/
├── app.py              # Flask API with scraping endpoints
├── web_scraper.py      # Core scraping logic
└── agent_state/        # Stored scraping results
    ├── scrape_batch_1_timestamp.json
    ├── scrape_batch_2_timestamp.json
    └── ...

frontend/
├── scraper.html        # Product scraper UI
└── index.html          # Main app (with link to scraper)
```

---

## 🛠️ Technical Details

### Backend Components

#### `web_scraper.py`
- **`extract_structured_data(url)`**: Scrapes a single URL
- **`scrape_search_results(results, batch_size)`**: Processes multiple URLs in batches
- **`extract_product_info(soup)`**: Extracts product-specific fields
- **`extract_price(soup)`**: Smart price detection
- **`extract_rating(soup)`**: Smart rating detection

#### `app.py` - New Endpoints
- **`POST /scrape_products`**: Main scraping endpoint
- **`POST /scrape_single`**: Single URL scraping

### Frontend Components

#### `scraper.html`
- Modern, responsive UI
- Real-time progress tracking
- Batch-by-batch display
- JSON preview/expand functionality
- Example queries for quick start

---

## ⚙️ Configuration

### Batch Size
Controls how many products to scrape at once:
```python
batch_size = 5  # Recommended: 5
```

**Trade-offs:**
- **Smaller (3)**: Slower but more frequent updates
- **Larger (10)**: Faster but less frequent updates

### Request Delay
Delay between scraping requests (in seconds):
```python
time.sleep(0.5)  # 500ms delay
```

### Timeout
How long to wait for each page:
```python
timeout = 10  # 10 seconds
```

---

## 🎨 Customization

### Add More Data Extraction

Edit `web_scraper.py` to extract additional fields:

```python
def extract_structured_data(url, timeout=10):
    # ... existing code ...
    
    # Add custom extraction
    data["discount"] = extract_discount(soup)
    data["availability"] = extract_availability(soup)
    data["reviews_count"] = extract_reviews_count(soup)
    
    return data
```

### Customize Display

Edit `scraper.html` to change product card layout:

```javascript
function createProductCard(item) {
    // Customize HTML structure
    card.innerHTML = `
        <!-- Your custom layout -->
    `;
    return card;
}
```

---

## 🔧 Installation

### Install Dependencies

```powershell
# Install Python packages
pip install -r requirements.txt
```

**New dependencies added:**
- `beautifulsoup4==4.12.3` - HTML parsing
- `lxml==5.1.0` - Fast XML/HTML parser

---

## 🚦 Usage Examples

### Example 1: Laptop Search
```
Query: "top 20 laptops under 60000"
Limit: 20
Batch Size: 5
Result: 4 batches, each with 5 laptops
```

### Example 2: Smartphone Research
```
Query: "best smartphones under 30000"
Limit: 15
Batch Size: 5
Result: 3 batches, each with 5 phones
```

### Example 3: Gaming Products
```
Query: "gaming laptops 2025"
Limit: 10
Batch Size: 5
Result: 2 batches, each with 5 gaming laptops
```

---

## 📊 Data Storage

### Batch Files
Each batch is saved as a separate JSON file:

```
agent_state/scrape_batch_1_1704123456.json
agent_state/scrape_batch_2_1704123467.json
agent_state/scrape_batch_3_1704123478.json
```

### File Naming Convention
```
scrape_batch_{batch_number}_{timestamp}.json
```

---

## 🎯 Best Practices

1. **Start Small**: Test with 5-10 products first
2. **Use Specific Queries**: Better results with specific terms
3. **Check Results**: Review first batch before scraping all
4. **Respect Rate Limits**: Don't scrape too aggressively
5. **Save JSON**: Download important results before clearing

---

## 🐛 Troubleshooting

### "No search results found"
- **Issue**: Query too specific or no results
- **Fix**: Try broader search terms

### "Scraping taking too long"
- **Issue**: Websites slow to respond
- **Fix**: Reduce limit or increase timeout

### "Error loading page"
- **Issue**: Website blocking requests
- **Fix**: Add delay between requests (already implemented)

### Missing price/rating
- **Issue**: Website structure different from patterns
- **Fix**: Normal - not all sites have standard structure

---

## 🔮 Future Enhancements

- [ ] Export results to CSV/Excel
- [ ] Price change tracking
- [ ] Product comparison view
- [ ] Custom extraction rules
- [ ] Scheduled scraping
- [ ] Filter and sort results
- [ ] Save favorites
- [ ] Share results via link

---

## 🎉 Summary

The Product Scraper feature provides:
- ✅ **Batch processing** (5 products at a time)
- ✅ **Structured JSON output** (complete metadata)
- ✅ **Progressive display** (see results as they load)
- ✅ **Local storage** (saved in JSON files)
- ✅ **Beautiful UI** (responsive and modern)
- ✅ **Easy to use** (one-click scraping)

Perfect for product research, price comparisons, and data collection! 🚀

---

## 📞 Support

For issues or questions:
1. Check console logs (F12 in browser)
2. Review stored JSON files in `agent_state/`
3. Test with `/scrape_single` endpoint first
4. Verify backend is running on port 5000

---

**Happy Scraping! 🛍️✨**
