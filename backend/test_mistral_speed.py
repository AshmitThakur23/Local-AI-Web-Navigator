"""
Quick test to check Mistral response time
"""
import requests
import time

OLLAMA_API = "http://127.0.0.1:11434/api/generate"
MODEL = "mistral"

def test_mistral_speed():
    question = "What is the capital of France?"
    
    print("🧪 Testing Mistral Speed...")
    print(f"Question: {question}\n")
    
    start_time = time.time()
    
    try:
        resp = requests.post(
            OLLAMA_API,
            json={
                "model": MODEL,
                "prompt": f"Answer this question briefly: {question}",
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 50,  # Very short answer
                    "num_gpu": 99,  # All GPU
                    "num_ctx": 512  # Minimal context
                }
            },
            timeout=30
        )
        
        elapsed = time.time() - start_time
        
        if resp.status_code == 200:
            data = resp.json()
            answer = data.get("response", "").strip()
            
            print(f"✅ Success!")
            print(f"⏱️  Time: {elapsed:.2f} seconds")
            print(f"📝 Answer: {answer}")
            
            if elapsed < 10:
                print("\n✅ Speed is GOOD! (< 10 seconds)")
            elif elapsed < 20:
                print("\n⚠️  Speed is OK but could be better (10-20 seconds)")
            else:
                print("\n❌ Speed is TOO SLOW! (> 20 seconds)")
                print("   Consider: ollama run mistral --num-gpu 99")
        else:
            print(f"❌ Error: Status {resp.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT after 30 seconds!")
        print("   Mistral is too slow - check Ollama configuration")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_mistral_speed()
