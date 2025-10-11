"""
Nexus AI Backend - Simple Flask API
Connects your beautiful frontend with agent_step3.py
"""

from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from agent_step3
from agent_step3 import call_ollama_answer, run_search_with_chrome, extract_answer_from_results
from playwright.sync_api import sync_playwright

# Import web scraper
from web_scraper import scrape_search_results, extract_structured_data

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Nexus AI Backend is running'}), 200


@app.route('/ask', methods=['POST', 'OPTIONS'])
def ask():
    """Main question answering endpoint - Optimized for speed"""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        print(f"\n{'='*60}")
        print(f"🔵 Question: {question}")
        print(f"{'='*60}")
        
        # SMART MODE: Mistral for simple/fast, Web for complex/large
        print("🧠 Step 1: Trying Mistral 7B first (fast for simple questions)...")
        ollama_answer, ollama_confident = call_ollama_answer(question)
        
        if ollama_confident and ollama_answer:
            print("✅ Mistral answered from its knowledge base!")
            print(f"   Answer length: {len(ollama_answer)} characters")
            return jsonify({
                'answer': ollama_answer,
                'method': 'mistral_7b',
                'sources': []
            }), 200
        
        # Step 2: Use web search for complex/large queries
        print("🌐 Step 2: Using web search for detailed/current information...")

        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel="chrome",
                headless=True,  # Faster in headless mode
                args=[
                    '--disable-gpu',  # Safe GPU usage
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            # Anti-detection
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.navigator.chrome = {runtime: {}};
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
            """)
            
            try:
                # Reduced to 5 results for speed (was 10)
                search_results = run_search_with_chrome(context, question, limit=5)
            finally:
                context.close()
                browser.close()
        
        if search_results and len(search_results) > 0:
            print(f"✅ Found {len(search_results)} search results")
            
            # Extract the final formatted answer (same as terminal version)
            final_answer = extract_answer_from_results(question, search_results)
            
            # Get source links
            sources = []
            for r in search_results[:5]:
                if r.get('link') and r.get('title'):
                    sources.append({
                        'title': r['title'],
                        'link': r['link'],
                        'snippet': r.get('snippet', '')[:200]
                    })
            
            print("✅ Web search completed")
            print(f"\n💡 Answer:\n{final_answer[:200]}...")
            
            return jsonify({
                'answer': final_answer,
                'method': 'web',
                'sources': sources
            }), 200
        else:
            return jsonify({
                'answer': "I searched the web but couldn't find reliable information. Please try rephrasing your question.",
                'method': 'none',
                'sources': []
            }), 200
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'answer': f"I encountered an error: {str(e)}. Please try again or rephrase your question.",
            'method': 'error',
            'sources': []
        }), 200  # Return 200 so frontend can display the error message


@app.route('/scrape_products', methods=['POST', 'OPTIONS'])
def scrape_products():
    """
    Scrape product data from search results in batches
    Progressive loading: Returns batches of products
    For Wikipedia: Extracts ALL tables with structured data
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        limit = int(data.get('limit', 100))  # Increased default: 100 results to get MORE data
        batch_size = int(data.get('batch_size', 10))  # Increased batch: 10 per batch
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        print(f"\n{'='*60}")
        print(f"🛍️ Product Scrape Request: {query}")
        print(f"📊 Limit: {limit} | Batch: {batch_size}")
        print(f"{'='*60}")
        
        # Import query optimizer
        from agent_step3 import optimize_query_for_wikipedia
        
        # Optimize query for Wikipedia (e.g., convert year ranges to individual searches)
        optimized_queries = optimize_query_for_wikipedia(query)
        print(f"🔍 Optimized queries: {optimized_queries}")
        
        # Collect all search results from all optimized queries
        all_search_results = []
        
        # Get search results first
        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel="chrome",
                headless=True,
                args=[
                    '--disable-gpu',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.navigator.chrome = {runtime: {}};
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
            """)
            
            try:
                # Search for each optimized query
                for opt_query in optimized_queries[:10]:  # Limit to 10 queries max
                    print(f"  🔎 Searching: {opt_query}")
                    results = run_search_with_chrome(context, opt_query, limit=5)  # Get top 5 per query
                    if results:
                        all_search_results.extend(results)
            finally:
                context.close()
                browser.close()
        
        if not all_search_results:
            return jsonify({
                'error': 'No search results found',
                'batches': []
            }), 404
        
        print(f"✅ Found {len(all_search_results)} total search results from {len(optimized_queries)} queries")
        
        # Scrape in batches and collect all results
        all_batches = []
        for batch_result in scrape_search_results(all_search_results, batch_size):
            all_batches.append(batch_result)
        
        return jsonify({
            'success': True,
            'query': query,
            'optimized_queries': optimized_queries,
            'total_items': len(all_search_results),
            'total_batches': len(all_batches),
            'batches': all_batches
        }), 200
        
    except Exception as e:
        print(f"\n❌ Scraping Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'batches': []
        }), 500


@app.route('/scrape_single', methods=['POST', 'OPTIONS'])
def scrape_single():
    """
    Scrape a single URL and return structured JSON data
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        print(f"\n🌐 Scraping single URL: {url}")
        
        # Extract structured data
        structured_data = extract_structured_data(url)
        
        return jsonify({
            'success': True,
            'data': structured_data
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Nexus AI Backend Starting...")
    print("="*60)
    print("📍 Server: http://localhost:5000")
    print("🔧 Health: http://localhost:5000/health")
    print("💬 Endpoint: POST /ask")
    print("="*60 + "\n")
    
    # Use Flask with proper settings
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True, use_reloader=False)
