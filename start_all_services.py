#!/usr/bin/env python3
"""
Nexus AI - Complete Service Starter
Starts all required services: Ollama, Backend, Frontend
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

def check_port(port):
    """Check if a port is in use"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def start_ollama():
    """Start Ollama service"""
    print("🤖 Starting Ollama...")
    try:
        # Check if already running
        if check_port(11434):
            print("   ✅ Ollama already running on port 11434")
            return True
        
        # Start Ollama
        subprocess.Popen(['ollama', 'serve'], 
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
        
        # Wait for it to start
        for i in range(10):
            time.sleep(1)
            try:
                response = requests.get('http://localhost:11434/api/tags', timeout=2)
                if response.status_code == 200:
                    print("   ✅ Ollama started successfully")
                    return True
            except:
                continue
        
        print("   ⚠️  Ollama may not be responding")
        return False
    except Exception as e:
        print(f"   ❌ Error starting Ollama: {e}")
        return False

def start_backend():
    """Start Flask backend"""
    print("\n🔧 Starting Backend...")
    try:
        if check_port(5000):
            print("   ✅ Backend already running on port 5000")
            return True
        
        backend_dir = Path(__file__).parent / 'backend'
        process = subprocess.Popen([sys.executable, 'app.py'],
                                  cwd=backend_dir,
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL,
                                  creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
        
        # Wait for backend
        for i in range(10):
            time.sleep(1)
            try:
                response = requests.get('http://localhost:5000/health', timeout=2)
                if response.status_code == 200:
                    print("   ✅ Backend started successfully")
                    return True
            except:
                continue
        
        print("   ⚠️  Backend may not be responding")
        return False
    except Exception as e:
        print(f"   ❌ Error starting Backend: {e}")
        return False

def start_frontend():
    """Start frontend HTTP server"""
    print("\n🌐 Starting Frontend...")
    try:
        if check_port(8080):
            print("   ✅ Frontend already running on port 8080")
            return True
        
        frontend_dir = Path(__file__).parent / 'frontend'
        process = subprocess.Popen([sys.executable, '-m', 'http.server', '8080'],
                                  cwd=frontend_dir,
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL,
                                  creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
        
        time.sleep(2)
        print("   ✅ Frontend started successfully")
        return True
    except Exception as e:
        print(f"   ❌ Error starting Frontend: {e}")
        return False

def main():
    print("\n" + "="*50)
    print("🚀 NEXUS AI - STARTING ALL SERVICES")
    print("="*50 + "\n")
    
    # Start all services
    ollama_ok = start_ollama()
    backend_ok = start_backend()
    frontend_ok = start_frontend()
    
    # Summary
    print("\n" + "="*50)
    print("📊 SERVICE STATUS")
    print("="*50)
    print(f"🤖 Ollama:   {'✅ RUNNING' if ollama_ok else '❌ FAILED'}")
    print(f"🔧 Backend:  {'✅ RUNNING' if backend_ok else '❌ FAILED'}")
    print(f"🌐 Frontend: {'✅ RUNNING' if frontend_ok else '❌ FAILED'}")
    print("="*50)
    
    if all([ollama_ok, backend_ok, frontend_ok]):
        print("\n✅ ALL SERVICES STARTED SUCCESSFULLY!")
        print("\n🎯 Open your browser: http://localhost:8080")
        print("\n💡 Press Ctrl+C to stop all services")
        
        # Open browser
        try:
            import webbrowser
            time.sleep(1)
            webbrowser.open('http://localhost:8080')
        except:
            pass
        
        # Keep script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down...")
    else:
        print("\n⚠️  Some services failed to start. Please check the logs.")
        sys.exit(1)

if __name__ == '__main__':
    main()
