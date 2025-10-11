# agent_step3.py
# Autonomous AI Agent: Local Reasoning (Mistral) + Web Search (Edge)
# Flow: Try Mistral first → If uncertain, search web → Return verified answer
# Run: python agent_step3.py

import os
import time
import json
import re
import urllib.parse
import traceback
import base64
from pathlib import Path

import requests
from playwright.sync_api import sync_playwright

# -------- CONFIG --------
OLLAMA_API = "http://127.0.0.1:11434/api/generate"
MODEL = "mistral"

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).resolve().parent
STATE_DIR = SCRIPT_DIR / "agent_state"
STATE_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_FILE = STATE_DIR / "agent_results.json"
STATE_FILE = STATE_DIR / "agent_state.json"

# Prompt for answering questions with confidence check
ANSWER_PROMPT = """You are Mistral 7B, a highly capable and knowledgeable AI assistant with extensive training data up to 2023.

Your task: Answer the following question directly, accurately, and comprehensively using your vast knowledge base.

Instructions:
- Provide detailed, well-structured answers
- Use your training data and knowledge confidently
- If you have ANY information about the topic, share it completely
- Only say "I don't know" if you truly have NO information at all
- For questions about general knowledge, history, science, technology, culture - answer from your training
- For lists (top movies, countries, facts) - provide complete detailed lists
- Be confident in your existing knowledge!

ONLY use "I don't know" or "I cannot provide" if:
- The question asks for information from after 2023
- The question requires real-time data (current weather, stock prices, today's news)
- You genuinely have zero information about the topic

Question: {question}

Provide your detailed answer now:"""

# -------- Helpers: LLM interaction --------
def check_ollama_running():
    """Check if Ollama server is running"""
    try:
        resp = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        return resp.status_code == 200
    except Exception:
        return False

def call_ollama_answer(question: str, timeout=30):
    """Ask Ollama Mistral - SMART MODE: Fast for simple, defer to web for complex
    
    Mistral answers simple/short questions from its knowledge.
    For complex/large questions, defers to web search.
    """
    # Check if Ollama is running
    if not check_ollama_running():
        print("⚠️  Ollama not running, will use web search")
        return None, False
    
    print("🧠 Asking Mistral 7B (optimized for speed)...")
    
    # Shorter, faster prompt for quick answers
    simple_prompt = f"""Answer this question briefly and accurately from your knowledge. If you don't know or need current information, say "I need to search the web for this."

Question: {question}

Answer:"""
    
    try:
        resp = requests.post(
            OLLAMA_API, 
            json={
                "model": MODEL, 
                "prompt": simple_prompt, 
                "stream": False,
                "options": {
                    "temperature": 0.2,  # Focused answers
                    "top_p": 0.8,
                    "top_k": 30,
                    "num_predict": 400,  # SHORTER for speed (was 600)
                    "num_gpu": 99,  # Use ALL GPU
                    "num_thread": 8,
                    "repeat_penalty": 1.1,
                    "num_batch": 512,
                    "num_ctx": 1024  # SMALLER context = FASTER (was 2048)
                }
            }, 
            timeout=timeout  # 30 seconds max for fast answers
        )
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("response", "").strip()
        
        # Check if answer exists
        if not answer or len(answer) < 5:
            print("⚠️  Mistral gave very short answer, using web search...")
            return None, False
        
        # Check if Mistral says to use web
        answer_lower = answer.lower()
        web_keywords = [
            "i need to search",
            "search the web",
            "i don't know",
            "i do not know",
            "i cannot provide current",
            "i don't have access to",
            "beyond my knowledge",
            "i cannot access",
            "current information",
            "real-time",
            "latest",
            "today's",
            "recent news"
        ]
        
        for keyword in web_keywords:
            if keyword in answer_lower:
                print(f"⚠️  Mistral says to use web: '{keyword}' found")
                return None, False
        
        # Good answer from Mistral!
        print(f"✅ Mistral answered! Length: {len(answer)} chars")
        return answer, True
        
    except requests.exceptions.Timeout:
        print("⏱️  Mistral timeout (30s), using web search...")
        return None, False
    except Exception as e:
        print(f"❌ Mistral error: {e}, using web search...")
        return None, False

# -------- Helpers: persistence --------
def save_results_append(new_items):
    data = []
    if RESULTS_FILE.exists():
        try:
            with RESULTS_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
    data.extend(new_items)
    with RESULTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_state(obj):
    try:
        with STATE_FILE.open("w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Failed saving state:", e)

def load_state():
    if STATE_FILE.exists():
        try:
            return json.load(STATE_FILE.open("r", encoding="utf-8"))
        except Exception:
            return {}
    return {}

# -------- Helpers: query cleaning & link decoding --------
def _clean_query(instruction: str):
    q = instruction.strip()
    q = re.sub(r'^(search\s+for|find|look for)\s+', '', q, flags=re.I)
    return q

def _maybe_base64_decode(s: str) -> str:
    if not s or not isinstance(s, str):
        return s
    payload = s
    if payload.startswith("a1"):
        payload = payload[2:]
    payload = payload.replace("-", "+").replace("_", "/")
    pad = (-len(payload)) % 4
    if pad:
        payload += "=" * pad
    try:
        decoded = base64.b64decode(payload)
        text = decoded.decode("utf-8", errors="ignore")
        if text.startswith("http://") or text.startswith("https://"):
            return text
    except Exception:
        pass
    return s

# -------- Query Optimizer for Wikipedia and Lists --------
def optimize_query_for_wikipedia(query: str):
    """
    Convert user queries into Wikipedia-friendly searches
    Examples:
    - "bollywood movies from 2012 to 2025" → Searches for each year separately
    - "smartphones from 2012 to 2025" → Searches for phone lists by year
    - "cars all brands" → Searches for car comparisons
    """
    query_lower = query.lower()
    optimized_queries = []
    
    # MOVIE QUERIES - Extract year ranges
    if any(word in query_lower for word in ['movie', 'film', 'bollywood', 'hollywood', 'cinema']):
        year_match = re.search(r'(\d{4})\s*(?:to|-)\s*(\d{4})', query_lower)
        if year_match:
            start_year = int(year_match.group(1))
            end_year = int(year_match.group(2))
            
            if 'bollywood' in query_lower or 'hindi' in query_lower:
                for year in range(start_year, min(end_year + 1, 2026)):  # Cap at 2025
                    optimized_queries.append(f"List of Hindi films of {year} Wikipedia")
                    optimized_queries.append(f"Bollywood movies {year} box office")
            elif 'hollywood' in query_lower:
                for year in range(start_year, min(end_year + 1, 2026)):
                    optimized_queries.append(f"List of American films of {year} Wikipedia")
            else:
                for year in range(start_year, min(end_year + 1, 2026)):
                    optimized_queries.append(f"List of films {year} Wikipedia")
        
        # Single year
        single_year = re.search(r'\b(20\d{2}|19\d{2})\b', query_lower)
        if single_year and not year_match:
            year = single_year.group(1)
            if 'bollywood' in query_lower or 'hindi' in query_lower:
                optimized_queries.append(f"List of Hindi films of {year} Wikipedia")
            else:
                optimized_queries.append(f"List of films {year} Wikipedia")
    
    # SONGS QUERIES
    if any(word in query_lower for word in ['song', 'songs', 'music', 'album']):
        year_match = re.search(r'(\d{4})\s*(?:to|-)\s*(\d{4})', query_lower)
        if year_match:
            start_year = int(year_match.group(1))
            end_year = int(year_match.group(2))
            
            for year in range(start_year, min(end_year + 1, 2026), 2):  # Every 2 years for songs
                if 'bollywood' in query_lower or 'hindi' in query_lower:
                    optimized_queries.append(f"List of Hindi songs {year} Wikipedia")
                    optimized_queries.append(f"Bollywood music {year}")
    
    # SMARTPHONE/PHONE QUERIES
    if any(word in query_lower for word in ['smartphone', 'phone', 'mobile']):
        year_match = re.search(r'(\d{4})\s*(?:to|-)\s*(\d{4})', query_lower)
        if year_match:
            start_year = int(year_match.group(1))
            end_year = int(year_match.group(2))
            
            for year in range(start_year, min(end_year + 1, 2026), 2):  # Every 2 years
                optimized_queries.append(f"List of smartphones {year}")
                optimized_queries.append(f"Best phones {year} comparison")
        else:
            optimized_queries.append("Comparison of smartphones Wikipedia")
            optimized_queries.append("List of best selling mobile phones")
    
    # LAPTOP QUERIES
    if 'laptop' in query_lower:
        optimized_queries.append("Comparison of laptops Wikipedia")
        optimized_queries.append("List of laptop brands and manufacturers")
        optimized_queries.append("Best laptops 2024 2025")
    
    # CAR QUERIES
    if any(word in query_lower for word in ['car', 'cars', 'vehicle', 'automobile']):
        if 'india' in query_lower:
            optimized_queries.append("List of cars in India Wikipedia")
            optimized_queries.append("Car prices India comparison")
            optimized_queries.append("Best cars under 30 lakh India")
        else:
            optimized_queries.append("Comparison of cars Wikipedia")
            optimized_queries.append("List of automobile manufacturers")
    
    # SPORTS/CRICKET QUERIES
    if any(word in query_lower for word in ['cricket', 'batsman', 'player']):
        if 'india' in query_lower or 'indian' in query_lower:
            optimized_queries.append("List of Indian cricketers Wikipedia")
            optimized_queries.append("India national cricket team records")
            optimized_queries.append("Indian cricket players all time")
    
    # CITIES/PLACES QUERIES
    if 'cities' in query_lower or 'city' in query_lower:
        if 'india' in query_lower:
            optimized_queries.append("List of cities in India by population")
            optimized_queries.append("List of million-plus cities in India")
        elif 'europe' in query_lower:
            optimized_queries.append("List of cities in Europe Wikipedia")
            optimized_queries.append("Largest cities in Europe")
        else:
            optimized_queries.append(f"List of cities {query}")
    
    # COUNTRIES QUERIES
    if 'countries' in query_lower or 'country' in query_lower:
        optimized_queries.append("List of countries Wikipedia")
        optimized_queries.append("List of sovereign states")
    
    # If no optimization found, return original query
    if not optimized_queries:
        optimized_queries = [query]
    
    return optimized_queries

# -------- Playwright route handler to block heavy resources --------
def _route_handler(route, request):
    try:
        if request.resource_type in ("image", "stylesheet", "font", "media"):
            return route.abort()
    except Exception:
        pass
    try:
        return route.continue_()
    except Exception:
        # sometimes route.continue_ fails on closed contexts; ignore
        return

# -------- Core: Web search using Chrome (DuckDuckGo - No CAPTCHA!) --------
def run_search_with_chrome(context, query: str, limit: int = 10, timeout_ms: int = 30000):
    """Search DuckDuckGo (no CAPTCHA!) using Chrome to get comprehensive results"""
    results = []
    page = None
    
    try:
        page = context.new_page()
        
        # Enhance query for current/today information
        enhanced_query = query.lower()
        
        # Check if user is asking for historical/range data (e.g., "2019 to 2023", "2001-2006")
        is_historical_range = any(pattern in enhanced_query for pattern in [
            " to ", " - ", "from ", "between ", 
            "2019 to 2023", "2020 to 2025", "2001 to 2006",
            "2010-2020", "1990-2000", "2000-2010"
        ])
        
        # Extract year ranges
        import re
        year_range_match = re.search(r'(19|20)\d{2}\s*(to|-|through|till)\s*(19|20)\d{2}', enhanced_query)
        
        # Check if user already specified a specific date
        has_specific_date = any(pattern in enhanced_query for pattern in [
            "10 oct", "11 oct", "12 oct", "january", "february", "march", 
            "april", "may", "june", "july", "august", "september", "october",
            "november", "december", "jan ", "feb ", "mar ", "apr ", "may ",
            "jun ", "jul ", "aug ", "sep ", "oct ", "nov ", "dec ",
            "/2025", "/2024", "-2025", "-2024"
        ])
        
        # Detect time-sensitive queries (weather, current events, today's info)
        is_current = any(word in enhanced_query for word in [
            "today", "current", "now", "latest", "weather", "temperature",
            "this week", "this month", "recent", "present"
        ])
        
        # PRIORITY 1: Historical range queries - Wikipedia is best!
        if is_historical_range or year_range_match:
            print(f"   📚 Historical range detected - prioritizing Wikipedia...")
            query = f"{query} wikipedia"
        # PRIORITY 2: Add time context for current queries (only if no specific date given)
        elif is_current and not has_specific_date:
            if "weather" in enhanced_query or "temperature" in enhanced_query:
                # Only add "today" if not already specified
                if "today" not in enhanced_query:
                    query = f"{query} today October 10 2025"
                else:
                    query = f"{query} October 10 2025"
            elif any(word in enhanced_query for word in ["current", "now", "latest", "present"]):
                query = query  # Keep as is, DuckDuckGo prioritizes recent
            else:
                query = f"{query} 2025"
        elif has_specific_date and "weather" in enhanced_query:
            # User specified date, just ensure we get that specific day
            query = f"{query} forecast"
        
        q = urllib.parse.quote_plus(_clean_query(query))
        
        # Use DuckDuckGo - NO CAPTCHA!
        url = f"https://duckduckgo.com/?q={q}"
        
        print(f"   Searching DuckDuckGo (no CAPTCHA!): {query}")

        # Navigate with human-like behavior
        try:
            page.goto(url, timeout=timeout_ms)
            time.sleep(2)  # Human-like pause
            
            # Wait for results
            page.wait_for_load_state("domcontentloaded", timeout=10000)
            time.sleep(1)
            
        except Exception as e:
            print(f"   Page load issue: {e}")
            print(f"   Trying alternative method...")
            time.sleep(1)

        # Extract DuckDuckGo search results
        try:
            # Wait for search results container
            try:
                page.wait_for_selector("[data-testid='result'], .result, #links", timeout=8000)
            except:
                print("   Waiting for results to load...")
                time.sleep(2)
            
            # DuckDuckGo uses different selectors
            result_selectors = [
                "[data-testid='result']",
                "article[data-testid='result']",
                ".result",
                "#links .result"
            ]
            
            result_items = []
            for selector in result_selectors:
                try:
                    items = page.query_selector_all(selector)
                    if items and len(items) > 0:
                        result_items = items
                        print(f"   Found {len(result_items)} results using selector: {selector}")
                        break
                except:
                    continue
            
            if not result_items:
                print("   Trying fallback extraction...")
                result_items = page.query_selector_all("div[data-result-index], .results_links")
            
            # Extract information from each result
            for item in result_items[:limit]:
                try:
                    # Get title
                    title = ""
                    title_selectors = ["h2", "[data-testid='result-title']", ".result__title", "a.result__a"]
                    
                    for sel in title_selectors:
                        try:
                            title_elem = item.query_selector(sel)
                            if title_elem:
                                title = title_elem.inner_text().strip()
                                if title:
                                    break
                        except:
                            continue
                    
                    # Get link
                    link = ""
                    link_selectors = ["a[href]", "[data-testid='result-title-a']", ".result__url"]
                    
                    for sel in link_selectors:
                        try:
                            link_elem = item.query_selector(sel)
                            if link_elem:
                                link = link_elem.get_attribute("href") or ""
                                if link and link.startswith("http"):
                                    break
                        except:
                            continue
                    
                    # Get snippet
                    snippet = ""
                    snippet_selectors = [
                        "[data-testid='result-snippet']",
                        ".result__snippet",
                        "[data-result='snippet']",
                        "div[data-testid='result-extras']"
                    ]
                    
                    for sel in snippet_selectors:
                        try:
                            snippet_elem = item.query_selector(sel)
                            if snippet_elem:
                                snippet = snippet_elem.inner_text().strip()
                                if snippet and len(snippet) > 20:
                                    break
                        except:
                            continue
                    
                    # Use title as snippet if no snippet found
                    if not snippet and title:
                        snippet = title
                    
                    # Validate and add result
                    if title and link and link.startswith("http"):
                        # Skip DuckDuckGo's own links
                        if "duckduckgo.com" not in link:
                            # Check if Wikipedia
                            is_wikipedia = "wikipedia.org" in link
                            
                            # Detect date indicators for recency scoring
                            is_recent = False
                            has_exact_date = False
                            lower_text = (snippet + title).lower()
                            
                            # Check for exact date match (October 10, Oct 10, 10 October, etc.)
                            exact_date_patterns = [
                                "october 10", "oct 10", "10 october", "10 oct",
                                "10th october", "october 10th", "10/10/2025",
                                "2025-10-10", "10-10-2025"
                            ]
                            for pattern in exact_date_patterns:
                                if pattern in lower_text:
                                    has_exact_date = True
                                    is_recent = True
                                    break
                            
                            # Check for recent time indicators
                            if not has_exact_date:
                                recent_indicators = [
                                    "today", "yesterday", "hours ago", "minutes ago",
                                    "this morning", "this evening", "tonight",
                                    "october 2025", "oct 2025", "2025",
                                    "this week", "this month", "latest", "breaking"
                                ]
                                
                                for indicator in recent_indicators:
                                    if indicator in lower_text:
                                        is_recent = True
                                        break
                            
                            # Detect OLD date indicators (to deprioritize)
                            is_old = False
                            old_indicators = [
                                "days ago", "weeks ago", "months ago", "years ago",
                                "2024", "2023", "2022", "2021", "2020",
                                "last year", "last month"
                            ]
                            
                            for indicator in old_indicators:
                                if indicator in lower_text:
                                    is_old = True
                                    break
                            
                            results.append({
                                "title": title,
                                "link": link,
                                "snippet": snippet,
                                "is_wikipedia": is_wikipedia,
                                "is_recent": is_recent,
                                "is_old": is_old,
                                "has_exact_date": has_exact_date
                            })
                            
                            # Visual indicators
                            markers = []
                            if has_exact_date:
                                markers.append("📅 Oct 10")
                            if is_wikipedia:
                                markers.append("📚 Wikipedia")
                            if is_recent and not has_exact_date:
                                markers.append("🔥 Recent")
                            if is_old:
                                markers.append("⏳ Old")
                            
                            marker_text = " | ".join(markers) if markers else ""
                            prefix = f"   [{marker_text}] " if marker_text else "   "
                            
                            print(f"   ✓ Result {len(results)}: {prefix}{title[:60]}...")
                
                except Exception as e:
                    continue
            
            # If still no results, try Bing as ultimate fallback
            if len(results) < 2:
                print("   Few results from DuckDuckGo, trying Bing...")
                
                try:
                    bing_url = f"https://www.bing.com/search?q={q}"
                    page.goto(bing_url, timeout=timeout_ms)
                    time.sleep(3)
                    
                    bing_results = page.query_selector_all("li.b_algo")
                    
                    for item in bing_results[:limit]:
                        try:
                            title_elem = item.query_selector("h2 a, h2")
                            title = title_elem.inner_text().strip() if title_elem else ""
                            
                            link_elem = item.query_selector("a")
                            link = link_elem.get_attribute("href") if link_elem else ""
                            link = _maybe_base64_decode(link)
                            
                            snippet_elem = item.query_selector("p, .b_caption p")
                            snippet = snippet_elem.inner_text().strip() if snippet_elem else title
                            
                            if title and link and link.startswith("http"):
                                if "bing.com" not in link and "microsoft.com" not in link:
                                    is_wikipedia = "wikipedia.org" in link
                                    
                                    # Detect recency for Bing results too
                                    is_recent = any(ind in (snippet + title).lower() for ind in [
                                        "today", "hours ago", "minutes ago", "october 2025", "2025", "latest"
                                    ])
                                    is_old = any(ind in (snippet + title).lower() for ind in [
                                        "days ago", "weeks ago", "months ago", "2024", "2023"
                                    ])
                                    
                                    results.append({
                                        "title": title,
                                        "link": link,
                                        "snippet": snippet,
                                        "is_wikipedia": is_wikipedia,
                                        "is_recent": is_recent,
                                        "is_old": is_old
                                    })
                                    print(f"   ✓ Result {len(results)}: {title[:60]}...")
                                    
                                    if len(results) >= limit:
                                        break
                        except:
                            continue
                except Exception as bing_error:
                    print(f"   Bing fallback failed: {bing_error}")
            
            # Check if this is a historical/range query
            import re
            is_historical_range = any(pattern in query.lower() for pattern in [
                " to ", " - ", "from ", "between "
            ])
            year_range_match = re.search(r'(19|20)\d{2}\s*(to|-|through|till)\s*(19|20)\d{2}', query.lower())
            
            # If STILL no good results, OR if historical range query, try Wikipedia directly
            if len(results) < 3 or is_historical_range or year_range_match:
                if is_historical_range or year_range_match:
                    print("   📚 Historical range query - fetching comprehensive Wikipedia data...")
                else:
                    print("   Trying Wikipedia directly for better context...")
                try:
                    # Extract key terms from query
                    wiki_query = query.replace("today", "").replace("current", "").replace("latest", "").replace("wikipedia", "").strip()
                    wiki_q = urllib.parse.quote_plus(wiki_query)
                    wiki_url = f"https://en.wikipedia.org/wiki/Special:Search?search={wiki_q}"
                    
                    page.goto(wiki_url, timeout=timeout_ms)
                    time.sleep(2)
                    
                    # Try to get first search result or main article
                    wiki_results = page.query_selector_all(".mw-search-result, .searchresult")
                    
                    if not wiki_results:
                        # Maybe we're on the article directly
                        wiki_results = page.query_selector_all("#mw-content-text p")
                    
                    for i, item in enumerate(wiki_results[:3]):
                        try:
                            # Get text content
                            text = item.inner_text().strip()
                            
                            # Get link if available
                            link_elem = item.query_selector("a")
                            if link_elem:
                                wiki_link = link_elem.get_attribute("href") or ""
                                if wiki_link.startswith("/"):
                                    wiki_link = f"https://en.wikipedia.org{wiki_link}"
                            else:
                                wiki_link = wiki_url
                            
                            if text and len(text) > 50:
                                results.append({
                                    "title": f"Wikipedia: {query}",
                                    "link": wiki_link,
                                    "snippet": text[:500],
                                    "is_wikipedia": True,
                                    "is_recent": False,
                                    "is_old": False
                                })
                                print(f"   ✓ Wikipedia result added: {text[:60]}...")
                                
                        except:
                            continue
                            
                except Exception as wiki_error:
                    print(f"   Wikipedia fallback note: {wiki_error}")
            
            print(f"   ✓ Total results extracted: {len(results)}")
            
        except Exception as e:
            print(f"   Error during extraction: {e}")
            import traceback
            traceback.print_exc()
    
    except Exception as e:
        print(f"   Browser error: {e}")
    
    finally:
        if page:
            try:
                page.close()
            except:
                pass
    
    return results

def extract_answer_from_results(question: str, results: list) -> str:
    """Extract comprehensive answer from search results, prioritizing recent and Wikipedia"""
    if not results:
        return "I cannot find a confirmed answer in available sources."
    
    # Check if question has a specific date
    question_lower = question.lower()
    has_specific_date = any(pattern in question_lower for pattern in [
        "10 oct", "11 oct", "12 oct", "1 oct", "2 oct", "3 oct",
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ])
    
    # Check if question asks for historical range data (e.g., "2019 to 2023")
    import re
    is_historical_range = any(pattern in question_lower for pattern in [
        " to ", " - ", "from ", "between "
    ])
    year_range_match = re.search(r'(19|20)\d{2}\s*(to|-|through|till)\s*(19|20)\d{2}', question_lower)
    is_range_query = is_historical_range or year_range_match is not None
    
    # Check if question asks for current/today information
    is_current_question = any(word in question_lower for word in [
        "today", "current", "now", "latest", "weather", "temperature",
        "this week", "this month", "recent", "present"
    ])
    
    # Check if question asks for a list
    is_list_question = any(word in question_lower for word in [
        "list", "top", "best", "all", "movies", "countries", "names", 
        "which", "what are", "give me"
    ])
    
    # Sort results by priority:
    # 1. Historical range queries → Wikipedia SUPREME
    # 2. Specific date match (for date queries)
    # 3. Recent results first (for current questions)
    # 4. Wikipedia (for factual questions)
    # 5. Non-old results
    def result_priority(r):
        score = 0
        
        # ⭐ SUPREME: Wikipedia for historical/range queries (2019 to 2023, etc.)
        if is_range_query and r.get("is_wikipedia", False):
            score += 5000  # SUPREME PRIORITY for Wikipedia on range queries!
            print(f"   ⭐ Wikipedia result boosted for range query: {r.get('title', '')[:60]}")
        
        # SUPER HIGHEST: Exact date match (e.g., "October 10" in result for "10 oct" query)
        if r.get("has_exact_date", False):
            score += 3000  # ULTIMATE PRIORITY for exact date match
        
        # VERY HIGH: Specific date in content
        if has_specific_date:
            snippet_text = (r.get("snippet", "") + r.get("title", "")).lower()
            # Look for the specific date in the result
            if "10 oct" in question_lower or "october 10" in question_lower:
                if "october 10" in snippet_text or "oct 10" in snippet_text or "10 october" in snippet_text:
                    score += 2000  # HIGH PRIORITY for date match
            # Check for other specific dates
            for pattern in ["january", "february", "march", "april", "may", "june",
                          "july", "august", "september", "october", "november", "december"]:
                if pattern in question_lower and pattern in snippet_text:
                    score += 1500
        
        # HIGH: Wikipedia for range queries (even if not first)
        if is_range_query and r.get("is_wikipedia", False):
            score += 2000  # Extra boost for Wikipedia on historical data
        
        # HIGHEST: Recent info for current questions
        if is_current_question and r.get("is_recent", False):
            score += 1000
        
        # HIGH: Wikipedia for factual info (normal priority)
        if r.get("is_wikipedia", False):
            score += 500
        
        # MEDIUM: Any recent info
        if r.get("is_recent", False):
            score += 300
        
        # PENALTY: Old info for current questions
        if is_current_question and r.get("is_old", False):
            score -= 800
        
        # Small penalty for old info in general
        if r.get("is_old", False):
            score -= 200
        
        return score
    
    # Sort results by priority
    priority_results = sorted(results, key=result_priority, reverse=True)
    
    # Special handling for historical/range queries - prefer comprehensive Wikipedia answers
    if is_range_query:
        print(f"   📚 Historical range query - prioritizing comprehensive Wikipedia data...")
        
        # Get all Wikipedia results
        wiki_results = [r for r in priority_results if r.get("is_wikipedia", False)]
        other_results = [r for r in priority_results if not r.get("is_wikipedia", False)]
        
        if wiki_results:
            # Build comprehensive answer from Wikipedia + supplementary sources
            answer_parts = []
            sources_used = []
            
            # Start with Wikipedia (comprehensive historical data)
            for i, result in enumerate(wiki_results[:2], 1):
                snippet = result.get("snippet", "").strip()
                title = result.get("title", "")
                link = result.get("link", "")
                
                if snippet and len(snippet) > 50:
                    answer_parts.append(snippet)
                    sources_used.append(f"📚 Wikipedia: {title}\n{link}")
            
            # Add supplementary sources
            for i, result in enumerate(other_results[:2], 1):
                snippet = result.get("snippet", "").strip()
                title = result.get("title", "")
                
                if snippet and len(snippet) > 50:
                    answer_parts.append(snippet)
                    sources_used.append(f"{i+len(wiki_results)}. {title}")
            
            if answer_parts:
                main_answer = "\n\n".join(answer_parts)
                
                if sources_used:
                    source_text = f"\n\n📚 Sources:\n1. {sources_used[0]}"
                    if len(sources_used) > 1:
                        for i, src in enumerate(sources_used[1:], 2):
                            source_text += f"\n{i}. {src}"
                    main_answer += source_text
                
                return main_answer
    
    if is_list_question:
        # For list questions, compile information from multiple sources
        answer_parts = []
        sources_used = []
        clean_list = []  # Extract clean names/items
        
        for i, result in enumerate(priority_results[:5], 1):
            snippet = result.get("snippet", "").strip()
            title = result.get("title", "")
            link = result.get("link", "")
            
            if snippet and len(snippet) > 30:
                # Try to extract clean list items from snippet
                import re
                
                # Method 1: Look for numbered lists (1., 2., etc.)
                list_items = re.findall(r'(?:^|\n)\s*(\d+)\.\s*([^\n]+?)(?:\n|$|:)', snippet, re.MULTILINE)
                if list_items:
                    clean_list.extend([f"{item[1].strip()}" for item in list_items[:10]])
                
                # Method 2: Look for bullet points
                if not list_items:
                    bullet_items = re.findall(r'(?:^|\n)\s*[•\-\*]\s*([^\n]+)', snippet, re.MULTILINE)
                    if bullet_items:
                        clean_list.extend([item.strip() for item in bullet_items[:10]])
                
                # Method 3: Look for comma-separated names (for "names" queries)
                if "name" in question_lower and not clean_list:
                    # Split by comma and clean
                    potential_names = [n.strip() for n in snippet.split(',')]
                    # Filter for likely names (2-30 chars, contains letters)
                    likely_names = [n for n in potential_names if 2 < len(n) < 30 and any(c.isalpha() for c in n)]
                    if likely_names:
                        clean_list.extend(likely_names[:10])
                
                # Add numbered info from each source
                if i == 1:
                    answer_parts.append(snippet)
                    sources_used.append(f"{title}\n{link}")
                elif len(answer_parts) < 3:
                    # Add more context from other sources
                    answer_parts.append(snippet)
                    sources_used.append(f"{title}")
        
        if answer_parts:
            # Start with clean list if found
            main_answer = ""
            if clean_list and len(clean_list) >= 3:
                # Remove duplicates while preserving order
                seen = set()
                unique_list = []
                for item in clean_list:
                    item_lower = item.lower()
                    if item_lower not in seen and len(item) > 2:
                        seen.add(item_lower)
                        unique_list.append(item)
                
                if unique_list:
                    main_answer = "**Quick List:**\n"
                    for idx, item in enumerate(unique_list[:10], 1):
                        main_answer += f"{idx}. {item}\n"
                    main_answer += "\n---\n\n**Detailed Information:**\n\n"
            
            # Add comprehensive answer
            main_answer += "\n\n".join(answer_parts[:2])
            
            if sources_used:
                source_text = f"\n\n📚 Sources:\n1. {sources_used[0]}"
                if len(sources_used) > 1:
                    for i, src in enumerate(sources_used[1:3], 2):
                        source_text += f"\n{i}. {src}"
                main_answer += source_text
            
            return main_answer
    
    # For non-list questions, find the best single answer
    best_snippet = ""
    best_source = ""
    best_link = ""
    best_priority = -999999
    
    for result in priority_results[:5]:
        snippet = result.get("snippet", "").strip()
        title = result.get("title", "")
        link = result.get("link", "")
        
        if len(snippet) < 30:
            continue
        
        # Calculate priority for this result
        priority = result_priority(result)
        
        # Longer snippets are better (but priority matters more)
        priority += len(snippet) / 10
        
        if priority > best_priority:
            best_snippet = snippet
            best_source = title
            best_link = link
            best_priority = priority
    
    if best_snippet:
        answer = best_snippet
        if best_source and best_link:
            # Add appropriate marker
            if "wikipedia" in best_link.lower():
                marker = "📚 Wikipedia: "
            elif is_current_question:
                marker = "🔥 Latest: "
            else:
                marker = "Source: "
            
            answer += f"\n\n{marker}{best_source}\n{best_link}"
        return answer
    
    # Fallback: show first result
    if results:
        return f"Found information at:\n{results[0].get('title', 'Source')}\n{results[0].get('link', '')}"
    
    return "I cannot find a confirmed answer in available sources."

# -------- Main flow --------
def main():
    print("=" * 70)
    print("🤖 AI Agent - Your Personal Assistant")
    print("    Powered by Mistral + Chrome Browser Search")
    print("=" * 70)
    
    question = input("\n❓ Ask me anything:\n> ").strip()
    if not question:
        print("No question provided. Exiting.")
        return

    start_time = time.time()
    final_answer = ""
    sources = []
    method = "local"

    # STEP 1: Try answering with local Mistral model
    print("\n🧠 Checking Mistral knowledge base...", end=" ", flush=True)
    answer, is_confident = call_ollama_answer(question)
    
    if is_confident and answer:
        # Mistral has a confident answer
        print("✓")
        final_answer = answer
        method = "local"
        print(f"\n💡 Answer:\n{final_answer}")
    else:
        # STEP 2: Mistral is uncertain, search the web
        print("\n🌐 Searching the web with Chrome...")
        
        try:
            with sync_playwright() as p:
                # Launch Chrome with anti-detection settings
                print("   Opening Chrome browser...")
                try:
                    # Try Google Chrome with stealth mode
                    browser = p.chromium.launch(
                        channel="chrome",
                        headless=False,  # Must be visible to avoid CAPTCHA
                        args=[
                            "--no-sandbox",
                            "--disable-blink-features=AutomationControlled",
                            "--disable-dev-shm-usage",
                            "--disable-web-security",
                            "--disable-features=IsolateOrigins,site-per-process",
                            "--disable-site-isolation-trials",
                            "--start-maximized"
                        ]
                    )
                except Exception:
                    print("   Chrome not found, using Chromium...")
                    try:
                        browser = p.chromium.launch(
                            headless=False,
                            args=[
                                "--no-sandbox",
                                "--disable-blink-features=AutomationControlled",
                                "--start-maximized"
                            ]
                        )
                    except Exception as e:
                        print(f"   Browser launch failed: {e}")
                        raise
                
                # Create context with realistic settings (anti-detection)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={"width": 1920, "height": 1080},
                    locale="en-US",
                    timezone_id="Asia/Kolkata",
                    permissions=["geolocation"],
                    geolocation={"latitude": 17.385044, "longitude": 78.486671},  # Hyderabad
                    color_scheme="light",
                    accept_downloads=True,
                    java_script_enabled=True,
                    has_touch=False,
                    is_mobile=False,
                    device_scale_factor=1
                )
                
                # Add extra JavaScript to hide automation
                context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en']
                    });
                    
                    window.chrome = {
                        runtime: {}
                    };
                """)
                
                # Set longer timeout for context
                context.set_default_timeout(40000)
                
                try:
                    # Search with Chrome (DuckDuckGo - No CAPTCHA!)
                    # Reduced to 5 for faster, focused results
                    results = run_search_with_chrome(context, question, limit=5, timeout_ms=30000)
                    
                    if results:
                        # Extract ONE BEST natural answer from results
                        final_answer = extract_answer_from_results(question, results)
                        sources = [r["link"] for r in results if r.get("link")]
                        method = "web"
                        
                        print(f"\n💡 Answer:\n{final_answer}")
                        
                        # Show additional sources if available
                        if len(results) > 1:
                            print(f"\n📚 Additional sources:")
                            for i, r in enumerate(results[1:4], 2):
                                if r.get('title') and r.get('link'):
                                    print(f"   {i}. {r['title'][:80]}")
                        
                        # Save results
                        save_results_append(results)
                    else:
                        final_answer = "I searched the web but couldn't find reliable information. Please try rephrasing your question."
                        method = "web"
                        print(f"\n⚠️  {final_answer}")
                
                except Exception as e:
                    print(f"   Search error: {e}")
                    traceback.print_exc()
                    final_answer = "I encountered an error while searching. Please try again."
                    method = "web"
                    print(f"\n⚠️  {final_answer}")
                
                finally:
                    try:
                        context.close()
                    except Exception:
                        pass
                    try:
                        browser.close()
                    except Exception:
                        pass
        
        except Exception as e:
            print(f"   Browser error: {e}")
            final_answer = "I encountered an error accessing the browser. Please try again."
            method = "web"
            print(f"\n⚠️  {final_answer}")

    elapsed = round(time.time() - start_time, 2)
    
    # Save result for logging (still keep JSON for records)
    output = {
        "question": question,
        "answer": final_answer,
        "sources": sources if sources else [],
        "method": method,
        "timestamp": time.time()
    }
    
    try:
        result_file = STATE_DIR / f"result_{int(time.time())}.json"
        with result_file.open("w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
    
    print(f"\n⏱️  Answered in {elapsed}s")
    print("=" * 70)

if __name__ == "__main__":
    main()