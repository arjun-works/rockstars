#!/usr/bin/env python3
"""
Test script for WCAG Compliance functionality
"""

import sys
import os

def test_wcag_imports():
    """Test if WCAG-related imports work"""
    print("🧪 Testing WCAG Compliance Module Imports...")
    
    try:
        from wcag_checker import WCAGCompliantChecker
        print("✅ WCAGCompliantChecker import: OK")
        
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup import: OK")
        
        import requests
        print("✅ Requests import: OK")
        
        # Test initialization
        checker = WCAGCompliantChecker()
        print("✅ WCAGCompliantChecker initialization: OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

def test_wcag_html_analysis():
    """Test WCAG HTML analysis functions"""
    print("\n🧪 Testing WCAG HTML Analysis...")
    
    try:
        from wcag_checker import WCAGCompliantChecker
        from bs4 import BeautifulSoup
        
        checker = WCAGCompliantChecker()
        
        # Test HTML with accessibility issues
        test_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Page</title>
        </head>
        <body>
            <h1>Main Heading</h1>
            <img src="test.jpg">
            <input type="text">
            <h3>Skipped H2</h3>
            <table>
                <tr><td>Cell 1</td><td>Cell 2</td></tr>
            </table>
        </body>
        </html>
        """
        
        soup = BeautifulSoup(test_html, 'html.parser')
        
        # Test individual check methods
        text_alt_issues = checker._check_text_alternatives(soup)
        print(f"✅ Text alternatives check: Found {len(text_alt_issues)} issues")
        
        adaptable_issues = checker._check_adaptable(soup)
        print(f"✅ Adaptable content check: Found {len(adaptable_issues)} issues")
        
        navigable_issues = checker._check_navigable(soup)
        print(f"✅ Navigable content check: Found {len(navigable_issues)} issues")
        
        readable_issues = checker._check_readable(soup)
        print(f"✅ Readable content check: Found {len(readable_issues)} issues")
        
        compatible_issues = checker._check_compatible(soup)
        print(f"✅ Compatible content check: Found {len(compatible_issues)} issues")
        
        return True
        
    except Exception as e:
        print(f"❌ WCAG HTML analysis failed: {e}")
        return False

def test_main_integration():
    """Test WCAG integration with main application"""
    print("\n🧪 Testing Main Application Integration...")
    
    try:
        from visual_ai_regression import VisualAIRegression
        
        # Test initialization with WCAG checker
        regression = VisualAIRegression()
        print("✅ VisualAIRegression with WCAG: OK")
        
        # Check if WCAG checker is initialized
        if hasattr(regression, 'wcag_checker'):
            print("✅ WCAG checker integration: OK")
        else:
            print("❌ WCAG checker not found in main application")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Main integration test failed: {e}")
        return False

def test_gui_integration():
    """Test WCAG integration with GUI"""
    print("\n🧪 Testing GUI Integration...")
    
    try:
        import tkinter as tk
        import sys
        import os
        
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        from main import VisualRegressionGUI
        
        # Create test root (but don't show)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test GUI initialization
        app = VisualRegressionGUI(root)
        print("✅ GUI initialization with WCAG: OK")
        
        # Check if WCAG analysis variable exists
        if hasattr(app, 'wcag_analysis_var'):
            print("✅ WCAG analysis option: OK")
        else:
            print("❌ WCAG analysis option not found")
            return False
        
        # Check if WCAG tab setup method exists
        if hasattr(app, 'setup_wcag_tab'):
            print("✅ WCAG tab setup method: OK")
        else:
            print("❌ WCAG tab setup method not found")
            return False
        
        # Check if WCAG display methods exist
        if hasattr(app, 'update_wcag_display'):
            print("✅ WCAG display methods: OK")
        else:
            print("❌ WCAG display methods not found")
            return False
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ GUI integration test failed: {e}")
        return False

def main():
    """Run all WCAG tests"""
    print("🚀 WCAG Compliance Module Test Suite")
    print("=" * 50)
    
    tests = [
        test_wcag_imports,
        test_wcag_html_analysis,
        test_main_integration,
        test_gui_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✅ PASSED")
            else:
                print("❌ FAILED")
        except Exception as e:
            print(f"💥 ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All WCAG tests passed! The module is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
