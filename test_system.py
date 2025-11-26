#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System Test Script for FixHR GPT Local
This script tests the complete system functionality.
"""

import os
import sys
import json
from pathlib import Path

def test_file_structure():
    """Test if all required files exist"""
    print("🔍 Testing file structure...")
    
    required_files = [
        "core/views.py",
        "core/models.py", 
        "core/urls.py",
        "core/train_model.py",
        "core/model_inference.py",
        "core/templates/login_page.html",
        "core/templates/chat_page.html",
        "dataset/general_data.json",
        "dataset/fix_hr_data.json",
        "fixhr_gpt_local/settings.py",
        "fixhr_gpt_local/urls.py",
        "manage.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files exist")
        return True

def test_data_files():
    """Test if data files are properly formatted"""
    print("\n📊 Testing data files...")
    
    data_files = [
        "dataset/general_data.json",
        "dataset/fix_hr_data.json"
    ]
    
    for file_path in data_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "train" not in data:
                print(f"❌ {file_path}: Missing 'train' key")
                return False
            
            if not isinstance(data["train"], list):
                print(f"❌ {file_path}: 'train' should be a list")
                return False
            
            if len(data["train"]) == 0:
                print(f"❌ {file_path}: 'train' list is empty")
                return False
            
            # Check first item structure
            first_item = data["train"][0]
            if "instruction" not in first_item or "output" not in first_item:
                print(f"❌ {file_path}: Items should have 'instruction' and 'output' keys")
                return False
            
            print(f"✅ {file_path}: Valid format with {len(data['train'])} training examples")
            
        except json.JSONDecodeError as e:
            print(f"❌ {file_path}: Invalid JSON - {e}")
            return False
        except Exception as e:
            print(f"❌ {file_path}: Error - {e}")
            return False
    
    return True

def test_python_imports():
    """Test if Python modules can be imported"""
    print("\n🐍 Testing Python imports...")
    
    # Test Django imports
    try:
        import django
        print(f"✅ Django {django.get_version()}")
    except ImportError:
        print("❌ Django not installed")
        return False
    
    # Test ML imports
    ml_packages = [
        ('torch', 'PyTorch'),
        ('transformers', 'Transformers'),
        ('datasets', 'Datasets'),
        ('peft', 'PEFT'),
        ('accelerate', 'Accelerate')
    ]
    
    for package, name in ml_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} not installed")
            return False
    
    return True

def test_model_inference():
    """Test model inference system"""
    print("\n🤖 Testing model inference system...")
    
    try:
        # Test if the module can be imported
        sys.path.insert(0, os.getcwd())
        from core.model_inference import FixHRModelInference, is_model_available
        
        print("✅ Model inference module imported successfully")
        
        # Test model availability check
        available = is_model_available()
        print(f"📊 Model available: {'✅' if available else '❌'}")
        
        # Test inference class initialization
        inference = FixHRModelInference()
        print("✅ Model inference class initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Model inference test failed: {e}")
        return False

def test_django_setup():
    """Test Django project setup"""
    print("\n🌐 Testing Django setup...")
    
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixhr_gpt_local.settings')
        
        import django
        django.setup()
        
        print("✅ Django setup successful")
        
        # Test if views can be imported
        from core import views
        print("✅ Views module imported")
        
        # Test if URLs can be imported
        from core import urls
        print("✅ URLs module imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def main():
    print("🧪 FixHR GPT Local System Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Data Files", test_data_files),
        ("Python Imports", test_python_imports),
        ("Model Inference", test_model_inference),
        ("Django Setup", test_django_setup)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n📝 Next steps:")
        print("   1. Run: python manage.py runserver")
        print("   2. Train the model: python train_ai_model.py")
        print("   3. Access: http://localhost:8000")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
