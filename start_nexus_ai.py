#!/usr/bin/env python3
"""
Nexus AI - One-Click Startup Script
Starts Ollama, Backend, and Frontend automatically
"""

import os
import sys
import time
import subprocess
import webbrowser
import requests
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Print Nexus AI banner"""
    print("=" * 70)
    print(f"{Colors.BOLD}{Colors.OKCYAN}    NEXUS AI - ONE-CLICK STARTUP{Colors.ENDC}")
    print("=" * 70)
    print()

def check_ollama():
    """Check if Ollama is running, start if not"""
    print(f"{Colors.OKBLUE}[1/3] 🧠 Checking Ollama...{Colors.ENDC}")
    
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print(f"{Colors.OKGREEN}   ✅ Ollama is already running!{Colors.ENDC}")
            return True
    except:
        pass
    
    print(f"{Colors.WARNING}   ⚠️  Ollama is not running!{Colors.ENDC}")
    print(f"{Colors.OKCYAN}   🚀 Starting Ollama...{Colors.ENDC}")
    
    try:
        if sys.platform == 'win32':
            # Windows
            subprocess.Popen(
                ['cmd', '/c', 'start', 'cmd', '/k', 'ollama serve'],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Linux/Mac
            subprocess.Popen(['ollama', 'serve'], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
        
        print(f"{Colors.OKCYAN}   ⏳ Waiting 5 seconds for Ollama to start...{Colors.ENDC}")
        time.sleep(5)
        
        # Verify Ollama started
        try:
            response = requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
            if response.status_code == 200:
                print(f"{Colors.OKGREEN}   ✅ Ollama started successfully!{Colors.ENDC}")
                return True
        except:
            print(f"{Colors.FAIL}   ❌ Failed to start Ollama{Colors.ENDC}")
            print(f"{Colors.WARNING}   💡 Please start Ollama manually: ollama serve{Colors.ENDC}")
            return False
            
    except Exception as e:
        print(f"{Colors.FAIL}   ❌ Error starting Ollama: {e}{Colors.ENDC}")
        print(f"{Colors.WARNING}   💡 Install Ollama from: https://ollama.ai{Colors.ENDC}")
        return False
    
    print()

def start_backend():
    """Start Flask backend server"""
    print(f"{Colors.OKBLUE}[2/3] 🔧 Starting Flask Backend Server...{Colors.ENDC}")
    
    backend_path = Path(__file__).parent / "backend"
    
    if not backend_path.exists():
        print(f"{Colors.FAIL}   ❌ Backend directory not found!{Colors.ENDC}")
        return None
    
    try:
        if sys.platform == 'win32':
            # Windows - open in new window
            process = subprocess.Popen(
                ['cmd', '/c', 'start', 'cmd', '/k', 
                 f'cd /d "{backend_path}" && echo Starting Nexus AI Backend... && python app.py'],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Linux/Mac
            process = subprocess.Popen(
                ['python', 'app.py'],
                cwd=backend_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
        print(f"{Colors.OKGREEN}   ✅ Backend server starting on http://localhost:5000{Colors.ENDC}")
        print(f"{Colors.OKCYAN}   ⏳ Waiting 3 seconds for server to initialize...{Colors.ENDC}")
        time.sleep(3)
        
        # Verify backend started
        try:
            response = requests.get("http://localhost:5000/health", timeout=2)
            if response.status_code == 200:
                print(f"{Colors.OKGREEN}   ✅ Backend is ready!{Colors.ENDC}")
            else:
                print(f"{Colors.WARNING}   ⚠️  Backend may need more time to start{Colors.ENDC}")
        except:
            print(f"{Colors.WARNING}   ⚠️  Backend is starting (check backend window for status){Colors.ENDC}")
        
        print()
        return process
        
    except Exception as e:
        print(f"{Colors.FAIL}   ❌ Error starting backend: {e}{Colors.ENDC}")
        print()
        return None

def open_frontend():
    """Open frontend in browser"""
    print(f"{Colors.OKBLUE}[3/3] 🌐 Opening Frontend Interface...{Colors.ENDC}")
    
    frontend_path = Path(__file__).parent / "frontend" / "index.html"
    
    if not frontend_path.exists():
        print(f"{Colors.FAIL}   ❌ Frontend file not found!{Colors.ENDC}")
        return False
    
    try:
        # Open in default browser
        webbrowser.open(f'file://{frontend_path.absolute()}')
        print(f"{Colors.OKGREEN}   ✅ Frontend opened in browser!{Colors.ENDC}")
        print()
        return True
        
    except Exception as e:
        print(f"{Colors.FAIL}   ❌ Error opening frontend: {e}{Colors.ENDC}")
        print(f"{Colors.WARNING}   💡 Open manually: {frontend_path}{Colors.ENDC}")
        print()
        return False

def print_status():
    """Print final status"""
    print("=" * 70)
    print(f"{Colors.BOLD}{Colors.OKGREEN}              ✅ NEXUS AI IS READY! ✅{Colors.ENDC}")
    print("=" * 70)
    print()
    print(f"{Colors.BOLD}📊 Status:{Colors.ENDC}")
    print(f"   🧠 Ollama Server   : {Colors.OKGREEN}Running{Colors.ENDC}")
    print(f"   🔧 Backend API     : {Colors.OKCYAN}http://localhost:5000{Colors.ENDC}")
    print(f"   🌐 Frontend        : {Colors.OKGREEN}Opened in browser{Colors.ENDC}")
    print()
    print(f"{Colors.BOLD}💡 Quick Tips:{Colors.ENDC}")
    print("   • Backend server is running in separate window")
    print("   • Keep the backend window open")
    print("   • Close backend window to stop the server")
    print("   • Run this script again anytime to restart")
    print()
    print(f"{Colors.BOLD}{Colors.OKGREEN}🎉 Start asking questions in the browser!{Colors.ENDC}")
    print()

def main():
    """Main startup function"""
    print_banner()
    
    # Step 1: Check/Start Ollama
    ollama_ok = check_ollama()
    if not ollama_ok:
        print(f"{Colors.WARNING}⚠️  Warning: Ollama may not be running properly{Colors.ENDC}")
        print(f"{Colors.WARNING}   You can continue, but local AI won't work{Colors.ENDC}")
        print()
        
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            print(f"{Colors.FAIL}Startup cancelled.{Colors.ENDC}")
            return
        print()
    
    # Step 2: Start Backend
    backend_process = start_backend()
    if backend_process is None:
        print(f"{Colors.FAIL}❌ Failed to start backend. Startup cancelled.{Colors.ENDC}")
        return
    
    # Step 3: Open Frontend
    frontend_ok = open_frontend()
    if not frontend_ok:
        print(f"{Colors.WARNING}⚠️  Frontend didn't open, but backend is running{Colors.ENDC}")
        print()
    
    # Print final status
    print_status()
    
    # Wait for user input
    print(f"{Colors.BOLD}Press Enter to exit (backend will keep running)...{Colors.ENDC}")
    input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  Startup interrupted by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)
