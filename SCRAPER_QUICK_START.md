# 🚀 Quick Start - Product Scraper

## Step 1: Start the Backend

```powershell
cd "d:\Nexus AI"
python backend\app.py
```

Wait for: `🚀 Nexus AI Backend Starting...`

---

## Step 2: Open the Product Scraper

Open your browser and go to:
```
http://localhost:5000/scraper.html
```

Or click the **"🛍️ Product Scraper"** button from the main Nexus AI page.

---

## Step 3: Search for Products

### Example Searches:

1. **Laptops:**
   ```
   top 20 laptops under 60000
   ```

2. **Smartphones:**
   ```
   best smartphones under 30000
   ```

3. **Gaming:**
   ```
   gaming laptops 2025
   ```

---

## Step 4: View Results

- Results appear in **batches of 5**
- Each product shows:
  - ✅ Product title and URL
  - ✅ Price and rating (if available)
  - ✅ JSON preview
  - ✅ Full JSON data (click to expand)

---

## What You'll Get

For each product, you get structured JSON like this:

```json
{
  "url": "https://example.com/product",
  "title": "Product Name",
  "price": "₹55,999",
  "rating": "4.5/5",
  "headings": {
    "h1": ["Product Name"],
    "h2": ["Features", "Specifications"],
    "h3": []
  },
  "images": [
    {
      "src": "https://example.com/image.jpg",
      "alt": "Product image"
    }
  ],
  "product_info": {
    "brand": "Dell",
    "model": "XPS 15"
  }
}
```

---

## Configuration

### Change Number of Products
- **Default**: 20 products
- **Range**: 5-50 products
- Change in the input field labeled with a number

### Change Batch Size
- **Default**: 5 products per batch
- **Range**: 3-10 per batch
- Change in the second input field

---

## Saved Results

All scraping results are automatically saved in:
```
d:\Nexus AI\backend\agent_state\scrape_batch_*.json
```

Each batch is saved as a separate JSON file.

---

## Troubleshooting

### Backend not running?
```powershell
cd "d:\Nexus AI"
python backend\app.py
```

### Port 5000 already in use?
- Close other applications using port 5000
- Or change the port in `backend\app.py` (line 155)

### No results found?
- Try a more specific search query
- Check your internet connection
- Try different search terms

---

## API Usage (For Developers)

### Scrape Multiple Products

```bash
curl -X POST http://localhost:5000/scrape_products \
  -H "Content-Type: application/json" \
  -d '{"query": "top 20 laptops", "limit": 20, "batch_size": 5}'
```

### Scrape Single URL

```bash
curl -X POST http://localhost:5000/scrape_single \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

---

## Tips for Best Results

1. **Be Specific**: Use detailed search queries
2. **Start Small**: Test with 5-10 products first
3. **Check Batches**: Review first batch before scraping all
4. **Save Important Data**: Download JSON files you need

---

## Features

- ✅ **Batch Processing**: 5 products at a time
- ✅ **Progressive Display**: See results as they load
- ✅ **JSON Export**: All data in structured format
- ✅ **Auto-Save**: Results stored locally
- ✅ **Price Detection**: Automatically extracts prices
- ✅ **Rating Detection**: Finds product ratings
- ✅ **Image Extraction**: Gets product images

---

**That's it! Start scraping products now! 🛍️✨**
