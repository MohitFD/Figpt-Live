#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick Start Script for FixHR GPT Local
This script helps you get started quickly with the system.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    print("🚀 FixHR GPT Local - Quick Start")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_django():
    """Setup Django project"""
    print("\n🌐 Setting up Django...")
    
    try:
        # Run migrations
        subprocess.run([sys.executable, "manage.py", "migrate"], 
                      check=True, capture_output=True)
        print("✅ Django migrations completed")
        
        # Create superuser (optional)
        print("   Note: You can create a superuser later with: python manage.py createsuperuser")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_system():
    """Run system tests"""
    print("\n🧪 Running system tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_system.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ System tests passed")
            return True
        else:
            print("❌ System tests failed")
            print(result.stdout)
            return False
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def show_next_steps():
    """Show next steps to the user"""
    print("\n🎯 Next Steps:")
    print("=" * 30)
    
    print("\n1. 🚀 Start the server:")
    print("   python manage.py runserver")
    
    print("\n2. 🤖 Train the AI model (optional but recommended):")
    print("   python train_ai_model.py")
    
    print("\n3. 🌐 Access the application:")
    print("   http://localhost:8000")
    
    print("\n4. 🔑 Login with your FixHR credentials")
    
    print("\n5. 💬 Start chatting with the AI assistant!")
    
    print("\n📚 For more information, see README.md")

def main():
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  You may need to install dependencies manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Setup Django
    if not setup_django():
        print("\n⚠️  Django setup failed. You may need to run migrations manually:")
        print("   python manage.py migrate")
        sys.exit(1)
    
    # Test system
    if not test_system():
        print("\n⚠️  Some tests failed, but you can still try running the system")
    
    # Show next steps
    show_next_steps()
    
    print("\n🎉 Quick start completed!")
    print("   The system is ready to use.")

if __name__ == "__main__":
    main()
