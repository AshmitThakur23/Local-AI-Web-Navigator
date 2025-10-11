"""
Web Scraper Module - Extract structured product data from websites
Batch processing: Scrape 5 products at a time, store and display progressively
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse
import time
from pathlib import Path

# Storage - Use absolute path relative to this script
SCRIPT_DIR = Path(__file__).resolve().parent
SCRAPER_DIR = SCRIPT_DIR / "agent_state"
SCRAPER_DIR.mkdir(parents=True, exist_ok=True)


def extract_wikipedia_tables(url, timeout=10):
    """
    Extract Wikipedia tables as structured key-value pairs
    Perfect for movie lists, car specs, phone comparisons, etc.
    Returns list of tables with clean data
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        tables_data = []
        
        # Find all tables
        tables = soup.find_all('table', class_=['wikitable', 'sortable', 'infobox'])
        
        for table_idx, table in enumerate(tables):
            # Get table caption/title
            caption = table.find('caption')
            table_title = caption.get_text().strip() if caption else f"Table {table_idx + 1}"
            
            # Find headers
            headers_row = table.find('tr')
            if not headers_row:
                continue
                
            headers = []
            for th in headers_row.find_all(['th', 'td']):
                header_text = th.get_text().strip()
                # Clean up references like [1], [2]
                header_text = re.sub(r'\[\d+\]', '', header_text)
                if header_text:
                    headers.append(header_text)
            
            if not headers:
                continue
            
            # Extract rows
            rows_data = []
            for row in table.find_all('tr')[1:]:  # Skip header row
                cells = row.find_all(['td', 'th'])
                if not cells:
                    continue
                
                row_dict = {}
                for idx, cell in enumerate(cells):
                    if idx < len(headers):
                        cell_text = cell.get_text().strip()
                        # Clean up references like [1], [2]
                        cell_text = re.sub(r'\[\d+\]', '', cell_text)
                        # Clean up newlines
                        cell_text = ' '.join(cell_text.split())
                        row_dict[headers[idx]] = cell_text
                
                if row_dict:
                    rows_data.append(row_dict)
            
            if rows_data:
                tables_data.append({
                    "table_title": table_title,
                    "row_count": len(rows_data),
                    "columns": headers,
                    "data": rows_data
                })
        
        return tables_data
        
    except Exception as e:
        print(f"❌ Error extracting Wikipedia tables: {e}")
        return []


def extract_structured_data(url, timeout=10):
    """
    Extract structured JSON data from a webpage
    Similar to the example format you provided
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic metadata
        data = {
            "url": url,
            "title": "",
            "meta_description": "",
            "headings": {
                "h1": [],
                "h2": [],
                "h3": []
            },
            "links": [],
            "paragraphs": [],
            "json_ld": [],
            "product_info": {},
            "images": [],
            "price": None,
            "rating": None
        }
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            data["title"] = title_tag.get_text().strip()
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc:
            data["meta_description"] = meta_desc.get('content', '').strip()
        
        # Headings
        for h1 in soup.find_all('h1'):
            text = h1.get_text().strip()
            if text:
                data["headings"]["h1"].append(text)
        
        for h2 in soup.find_all('h2'):
            text = h2.get_text().strip()
            if text:
                data["headings"]["h2"].append(text)
        
        for h3 in soup.find_all('h3'):
            text = h3.get_text().strip()
            if text:
                data["headings"]["h3"].append(text)
        
        # Links (top 10 most relevant)
        link_count = 0
        for a in soup.find_all('a', href=True):
            if link_count >= 10:
                break
            href = a.get('href', '')
            text = a.get_text().strip()
            
            # Make absolute URL
            if href and not href.startswith('javascript:') and not href.startswith('#'):
                full_url = urljoin(url, href)
                if text and full_url:
                    data["links"].append({
                        "text": text[:100],  # Limit text length
                        "href": full_url
                    })
                    link_count += 1
        
        # Paragraphs (first 5)
        para_count = 0
        for p in soup.find_all('p'):
            if para_count >= 5:
                break
            text = p.get_text().strip()
            if text and len(text) > 20:  # Only meaningful paragraphs
                data["paragraphs"].append(text[:300])  # Limit length
                para_count += 1
        
        # JSON-LD structured data
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                json_data = json.loads(script.string)
                data["json_ld"].append(json_data)
            except:
                continue
        
        # Product-specific extraction
        data["product_info"] = extract_product_info(soup)
        
        # Images (product images)
        for img in soup.find_all('img')[:5]:
            src = img.get('src') or img.get('data-src')
            if src:
                full_img_url = urljoin(url, src)
                alt = img.get('alt', '')
                data["images"].append({
                    "src": full_img_url,
                    "alt": alt
                })
        
        # Price extraction (multiple patterns)
        data["price"] = extract_price(soup)
        
        # Rating extraction
        data["rating"] = extract_rating(soup)
        
        # WIKIPEDIA TABLES - Extract structured data as key-value pairs
        if 'wikipedia.org' in url.lower():
            print(f"📊 Wikipedia detected - extracting tables...")
            data["wikipedia_tables"] = extract_wikipedia_tables(url, timeout)
        
        return data
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {
            "url": url,
            "error": str(e),
            "title": "Error loading page",
            "meta_description": "",
            "headings": {"h1": [], "h2": [], "h3": []},
            "links": [],
            "paragraphs": [],
            "json_ld": [],
            "product_info": {},
            "images": [],
            "price": None,
            "rating": None
        }


def extract_product_info(soup):
    """Extract product-specific information"""
    product_info = {}
    
    # Common product info patterns
    patterns = {
        "brand": ["brand", "manufacturer", "company"],
        "model": ["model", "model number", "sku"],
        "specifications": ["specs", "specifications", "features"],
        "availability": ["availability", "in stock", "stock"],
        "color": ["color", "colour"],
        "size": ["size", "dimensions"]
    }
    
    for key, keywords in patterns.items():
        for keyword in keywords:
            # Try to find in meta tags
            meta = soup.find('meta', attrs={'name': re.compile(keyword, re.I)})
            if not meta:
                meta = soup.find('meta', attrs={'property': re.compile(keyword, re.I)})
            
            if meta:
                product_info[key] = meta.get('content', '')
                break
            
            # Try to find in common product info sections
            elem = soup.find(['span', 'div', 'p'], class_=re.compile(keyword, re.I))
            if elem:
                product_info[key] = elem.get_text().strip()[:100]
                break
    
    return product_info


def extract_price(soup):
    """Extract price from page"""
    # Common price patterns
    price_patterns = [
        {'class': re.compile(r'price', re.I)},
        {'itemprop': 'price'},
        {'class': re.compile(r'cost', re.I)},
        {'class': re.compile(r'amount', re.I)}
    ]
    
    for pattern in price_patterns:
        price_elem = soup.find(['span', 'div', 'p', 'strong'], pattern)
        if price_elem:
            price_text = price_elem.get_text().strip()
            # Extract numeric price
            price_match = re.search(r'[₹$€£]\s*[\d,]+(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?', price_text)
            if price_match:
                return price_match.group(0)
    
    # Try meta tags
    meta_price = soup.find('meta', attrs={'property': 'og:price:amount'})
    if meta_price:
        return meta_price.get('content', '')
    
    return None


def extract_rating(soup):
    """Extract rating from page"""
    # Common rating patterns
    rating_patterns = [
        {'itemprop': 'ratingValue'},
        {'class': re.compile(r'rating', re.I)},
        {'class': re.compile(r'stars', re.I)}
    ]
    
    for pattern in rating_patterns:
        rating_elem = soup.find(['span', 'div', 'p'], pattern)
        if rating_elem:
            rating_text = rating_elem.get_text().strip()
            # Extract numeric rating
            rating_match = re.search(r'\d+\.?\d*\s*(?:out of|/|\|)?\s*\d*', rating_text)
            if rating_match:
                return rating_match.group(0)
    
    return None


def scrape_search_results(search_results, batch_size=5):
    """
    Scrape websites from search results in batches
    
    Args:
        search_results: List of search results from DuckDuckGo/Bing
        batch_size: Number of sites to scrape per batch (default: 5)
    
    Returns:
        Generator yielding batches of scraped data
    """
    total_results = len(search_results)
    
    for batch_start in range(0, total_results, batch_size):
        batch_end = min(batch_start + batch_size, total_results)
        batch = search_results[batch_start:batch_end]
        
        batch_data = []
        
        print(f"\n📦 Processing batch {batch_start//batch_size + 1} (items {batch_start+1}-{batch_end})...")
        
        for idx, result in enumerate(batch):
            url = result.get('link', '')
            if not url:
                continue
            
            print(f"   🌐 Scraping {idx+1}/{len(batch)}: {result.get('title', 'Unknown')[:50]}...")
            
            # Extract structured data
            structured_data = extract_structured_data(url)
            
            # Add search result context
            structured_data['search_snippet'] = result.get('snippet', '')
            structured_data['search_title'] = result.get('title', '')
            structured_data['batch_number'] = batch_start // batch_size + 1
            structured_data['item_number'] = batch_start + idx + 1
            
            batch_data.append(structured_data)
            
            # Be polite - small delay between requests
            time.sleep(0.5)
        
        # Save this batch
        batch_filename = SCRAPER_DIR / f"scrape_batch_{batch_start//batch_size + 1}_{int(time.time())}.json"
        with open(batch_filename, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Batch {batch_start//batch_size + 1} complete! Saved to {batch_filename.name}")
        
        # Yield this batch for progressive updates
        yield {
            'batch_number': batch_start // batch_size + 1,
            'total_batches': (total_results + batch_size - 1) // batch_size,
            'items': batch_data,
            'progress': f"{batch_end}/{total_results}"
        }


def scrape_products_progressive(query, search_function, limit=20, batch_size=5):
    """
    Main function to scrape products progressively
    
    Args:
        query: User search query (e.g., "top 20 laptops under 60000")
        search_function: Function to get search results (from agent_step3.py)
        limit: Total number of products to scrape
        batch_size: Products per batch
    
    Returns:
        Generator yielding batches of product data
    """
    print(f"🔍 Searching for: {query}")
    print(f"📊 Will scrape {limit} results in batches of {batch_size}")
    
    # Get search results
    search_results = search_function(query, limit=limit)
    
    if not search_results:
        print("❌ No search results found")
        return
    
    print(f"✅ Found {len(search_results)} search results")
    
    # Scrape in batches
    for batch_result in scrape_search_results(search_results, batch_size):
        yield batch_result
    
    print(f"\n🎉 All batches complete!")


# Test function
if __name__ == "__main__":
    # Test with example.com
    print("Testing web scraper...")
    data = extract_structured_data("https://example.com")
    print(json.dumps(data, indent=2))
