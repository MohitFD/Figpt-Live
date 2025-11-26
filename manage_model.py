#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FixHR Model Management Script
This script helps manage the AI model for FixHR command generation.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'torch', 'transformers', 'datasets', 'peft', 'accelerate'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install torch transformers datasets peft accelerate")
        return False
    
    print("✅ All dependencies are installed")
    return True

def check_data_files():
    """Check if training data files exist"""
    data_files = [
        "dataset/general_data.json",
        "dataset/fix_hr_data.json"
    ]
    
    missing_files = []
    for file_path in data_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing data files: {', '.join(missing_files)}")
        return False
    
    print("✅ All data files exist")
    return True

def train_model():
    """Train the model"""
    print("🚀 Starting model training...")
    
    if not check_dependencies():
        return False
    
    if not check_data_files():
        return False
    
    try:
        # Import and run training
        from core.train_model import *
        print("✅ Model training completed successfully")
        return True
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

def test_model():
    """Test the trained model"""
    print("🧪 Testing model...")
    
    try:
        from core.model_inference import model_inference
        
        if not model_inference.load_model():
            print("❌ Failed to load model")
            return False
        
        # Test with sample inputs
        test_inputs = [
            "How do I apply for leave?",
            "What is my leave balance?",
            "Show me today's holiday",
            "Apply leave for tomorrow for personal work"
        ]
        
        for test_input in test_inputs:
            print(f"\n📝 Input: {test_input}")
            result = model_inference.extract_command(test_input)
            print(f"🤖 Command Type: {result.get('command_type')}")
            print(f"📋 Extracted Commands: {result.get('extracted_commands')}")
            print(f"💬 Response: {result.get('model_response')[:100]}...")
        
        print("\n✅ Model testing completed")
        return True
        
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        return False

def check_model_status():
    """Check model status"""
    print("📊 Checking model status...")
    
    status = {
        "model_path_exists": os.path.exists("fixhr_model"),
        "data_files_exist": check_data_files(),
        "dependencies_installed": check_dependencies()
    }
    
    print(f"Model path exists: {'✅' if status['model_path_exists'] else '❌'}")
    print(f"Data files exist: {'✅' if status['data_files_exist'] else '❌'}")
    print(f"Dependencies installed: {'✅' if status['dependencies_installed'] else '❌'}")
    
    return status

def main():
    parser = argparse.ArgumentParser(description="FixHR Model Management")
    parser.add_argument("command", choices=["train", "test", "status", "check"], 
                       help="Command to execute")
    
    args = parser.parse_args()
    
    if args.command == "train":
        success = train_model()
        sys.exit(0 if success else 1)
    
    elif args.command == "test":
        success = test_model()
        sys.exit(0 if success else 1)
    
    elif args.command == "status":
        check_model_status()
    
    elif args.command == "check":
        print("🔍 Checking system requirements...")
        deps_ok = check_dependencies()
        data_ok = check_data_files()
        
        if deps_ok and data_ok:
            print("\n✅ System is ready for training!")
        else:
            print("\n❌ System is not ready. Please fix the issues above.")
            sys.exit(1)

if __name__ == "__main__":
    main()
