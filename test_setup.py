"""
Quick test script to verify Nexus AI setup
"""

import sys
import os

print("=" * 60)
print("🔍 Nexus AI Setup Verification")
print("=" * 60)
print()

# Test 1: Python version
print("✓ Testing Python version...")
version = sys.version_info
if version.major == 3 and version.minor >= 10:
    print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
else:
    print(f"  ⚠️ Python {version.major}.{version.minor}.{version.micro} (Recommend 3.10+)")
print()

# Test 2: Required modules
print("✓ Testing required modules...")
required_modules = ['flask', 'flask_cors', 'playwright', 'requests']
missing = []

for module in required_modules:
    try:
        __import__(module)
        print(f"  ✅ {module}")
    except ImportError:
        print(f"  ❌ {module} (missing)")
        missing.append(module)
print()

# Test 3: Check Ollama
print("✓ Testing Ollama connection...")
try:
    import requests
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "mistral", "prompt": "Hi", "stream": False},
        timeout=5
    )
    if response.status_code == 200:
        print("  ✅ Ollama is running")
        print("  ✅ Mistral model available")
    else:
        print("  ⚠️ Ollama responded but may have issues")
except requests.exceptions.ConnectionError:
    print("  ❌ Ollama is not running")
    print("  💡 Start with: ollama serve")
except Exception as e:
    print(f"  ⚠️ Error testing Ollama: {str(e)}")
print()

# Test 4: Check file structure
print("✓ Testing file structure...")
files_to_check = [
    'backend/agent_step3.py',
    'backend/app.py',
    'frontend/index.html',
    'frontend/styles.css',
    'frontend/script.js',
    'start_backend.bat'
]

for file_path in files_to_check:
    full_path = os.path.join(os.path.dirname(__file__), '..', file_path)
    if os.path.exists(full_path):
        print(f"  ✅ {file_path}")
    else:
        print(f"  ❌ {file_path} (missing)")
print()

# Summary
print("=" * 60)
print("📊 Summary")
print("=" * 60)

if missing:
    print(f"❌ Missing modules: {', '.join(missing)}")
    print(f"   Install with: pip install {' '.join(missing)}")
    print()

print("📝 Next Steps:")
print("   1. Start Ollama: ollama serve")
print("   2. Start Backend: python backend/app.py")
print("   3. Open Frontend: frontend/index.html in browser")
print()
print("🌐 Frontend will connect to: http://localhost:5000")
print("=" * 60)
