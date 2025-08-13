#!/usr/bin/env python3
"""
Test WCAG Refresh Button Functionality
Diagnose and fix issues with the "Refresh WCAG Results" button
"""

import tkinter as tk
from tkinter import ttk
import json
import os
import glob
from datetime import datetime

# Import the GUI class
from main import VisualRegressionGUI

def test_wcag_refresh_functionality():
    """Test the WCAG refresh button functionality"""
    print("🧪 Testing WCAG Refresh Button Functionality")
    print("=" * 50)
    
    # Create a test GUI instance
    root = tk.Tk()
    root.withdraw()  # Hide the window for testing
    
    try:
        app = VisualRegressionGUI(root)
        
        # Test 1: Check if refresh method exists
        print("1️⃣ Testing refresh method existence...")
        if hasattr(app, 'refresh_wcag_display'):
            print("✅ refresh_wcag_display method exists")
        else:
            print("❌ refresh_wcag_display method missing")
            return False
        
        # Test 2: Create mock WCAG data for testing
        print("\n2️⃣ Creating mock WCAG data...")
        mock_wcag_data = {
            'url1': {
                'compliance_score': 85.5,
                'compliance_level': 'AA',
                'total_issues': 12,
                'critical_issues': 3,
                'categories': {
                    'perceivable': {'score': 88, 'issues': ['Missing alt text', 'Low contrast']},
                    'operable': {'score': 92, 'issues': ['Keyboard navigation issue']},
                    'understandable': {'score': 80, 'issues': ['Complex language', 'No error instructions']},
                    'robust': {'score': 95, 'issues': ['HTML validation error']}
                }
            },
            'url2': {
                'compliance_score': 78.2,
                'compliance_level': 'A',
                'total_issues': 18,
                'critical_issues': 7,
                'categories': {
                    'perceivable': {'score': 75, 'issues': ['Missing alt text', 'Poor color contrast', 'No focus indicators']},
                    'operable': {'score': 82, 'issues': ['Keyboard trap', 'Small click targets']},
                    'understandable': {'score': 76, 'issues': ['Complex language', 'No error help', 'Unclear labels']},
                    'robust': {'score': 90, 'issues': ['Invalid HTML', 'Compatibility issues']}
                }
            },
            'comparison': {
                'score_difference': -7.3,
                'assessment': 'URL1 has better accessibility than URL2',
                'level_comparison': {'url1': 'AA', 'url2': 'A'}
            }
        }
        
        mock_results = {
            'wcag_analysis': mock_wcag_data,
            'timestamp': datetime.now().isoformat(),
            'urls': {'url1': 'https://example.com', 'url2': 'https://test.example.com'},
            'analysis_results': {
                'wcag_analysis': mock_wcag_data
            }
        }
        
        print("✅ Mock WCAG data created")
        
        # Test 3: Set last_results and test refresh
        print("\n3️⃣ Testing refresh with last_results...")
        app.last_results = mock_results
        
        try:
            app.refresh_wcag_display()
            print("✅ Refresh method executed without errors")
        except Exception as e:
            print(f"❌ Refresh method failed: {e}")
            return False
        
        # Test 4: Test refresh without last_results (simulating empty state)
        print("\n4️⃣ Testing refresh without last_results...")
        app.last_results = None
        
        try:
            app.refresh_wcag_display()
            print("✅ Refresh method handled empty state correctly")
        except Exception as e:
            print(f"❌ Refresh method failed on empty state: {e}")
            return False
        
        # Test 5: Create a mock report file and test loading from file
        print("\n5️⃣ Testing refresh from report file...")
        
        # Ensure reports directory exists
        os.makedirs('reports', exist_ok=True)
        
        # Create a mock report file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        mock_report_path = f'reports/visual_regression_report_{timestamp}_test.json'
        
        with open(mock_report_path, 'w') as f:
            json.dump(mock_results, f, indent=2)
        
        print(f"📁 Created mock report: {os.path.basename(mock_report_path)}")
        
        # Clear last_results and test file loading
        app.last_results = None
        
        try:
            app.refresh_wcag_display()
            print("✅ Refresh method loaded from report file successfully")
        except Exception as e:
            print(f"❌ Refresh method failed to load from file: {e}")
            # Clean up
            if os.path.exists(mock_report_path):
                os.remove(mock_report_path)
            return False
        
        # Test 6: Test WCAG display update
        print("\n6️⃣ Testing WCAG display update...")
        
        try:
            app.update_wcag_display(mock_wcag_data)
            print("✅ WCAG display update successful")
        except Exception as e:
            print(f"❌ WCAG display update failed: {e}")
            # Clean up
            if os.path.exists(mock_report_path):
                os.remove(mock_report_path)
            return False
        
        # Clean up mock report file
        if os.path.exists(mock_report_path):
            os.remove(mock_report_path)
            print(f"🗑️ Cleaned up mock report file")
        
        print("\n✅ All WCAG refresh tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        return False
    finally:
        root.destroy()

def check_wcag_button_configuration():
    """Check if the WCAG refresh button is properly configured"""
    print("\n🔍 Checking WCAG Button Configuration")
    print("=" * 40)
    
    # Read the main.py file to check button configuration
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for refresh button
        if '🔄 Refresh WCAG Results' in content:
            print("✅ Refresh button text found")
        else:
            print("❌ Refresh button text missing")
            return False
        
        # Check for command binding
        if 'command=self.refresh_wcag_display' in content:
            print("✅ Button command binding found")
        else:
            print("❌ Button command binding missing")
            return False
        
        # Check for method definition
        if 'def refresh_wcag_display(self):' in content:
            print("✅ Refresh method definition found")
        else:
            print("❌ Refresh method definition missing")
            return False
        
        print("✅ WCAG button configuration is correct")
        return True
        
    except Exception as e:
        print(f"❌ Failed to check configuration: {e}")
        return False

def suggest_improvements():
    """Suggest improvements for WCAG refresh functionality"""
    print("\n💡 Suggested Improvements")
    print("=" * 30)
    
    improvements = [
        "1. Add visual feedback when refresh button is clicked",
        "2. Show timestamp of last WCAG analysis",
        "3. Add auto-refresh option",
        "4. Improve error handling for missing data",
        "5. Add status indicator for WCAG data availability",
        "6. Cache WCAG results for faster refresh",
        "7. Add progress indicator for refresh operation"
    ]
    
    for improvement in improvements:
        print(f"💡 {improvement}")

if __name__ == "__main__":
    print("🔧 WCAG Refresh Button Diagnostic Tool")
    print("=" * 60)
    
    # Run tests
    config_ok = check_wcag_button_configuration()
    refresh_ok = test_wcag_refresh_functionality()
    
    print(f"\n📊 Test Results:")
    print(f"Configuration Check: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"Functionality Test: {'✅ PASS' if refresh_ok else '❌ FAIL'}")
    
    if config_ok and refresh_ok:
        print("\n🎉 WCAG Refresh functionality is working correctly!")
        print("💡 The issue might be in the data flow or timing.")
    else:
        print("\n⚠️ Issues detected with WCAG Refresh functionality")
        suggest_improvements()
    
    print("\n📝 Diagnostic complete!")
