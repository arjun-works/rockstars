#!/usr/bin/env python3
"""
Test the updated screenshot path fix that looks for copied files in reports directory
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from report_generator import ReportGenerator

def test_screenshot_path_fix():
    """Test the updated screenshot path handling"""
    print("🧪 Testing updated screenshot path fix...")
    
    # Create a mock reports directory structure like we see in real analysis
    test_reports_dir = "test_reports"
    os.makedirs(test_reports_dir, exist_ok=True)
    
    # Create mock screenshot files with the actual naming pattern
    mock_screenshot1 = os.path.join(test_reports_dir, "visual_regression_report_20250813_085253_url1_screenshot.png")
    mock_screenshot2 = os.path.join(test_reports_dir, "visual_regression_report_20250813_085253_url2_screenshot.png")
    
    # Create dummy files
    with open(mock_screenshot1, 'w') as f:
        f.write("dummy image content")
    with open(mock_screenshot2, 'w') as f:
        f.write("dummy image content")
    
    # Create mock analysis results
    mock_analysis_results = {
        'screenshots': {
            'url1': 'screenshots/20250813_085253/url1_screenshot.png',
            'url2': 'screenshots/20250813_085253/url2_screenshot.png'
        }
    }
    
    # Create report generator with test output directory
    report_gen = ReportGenerator(output_dir=test_reports_dir)
    
    # Test image HTML generation
    print("\n🔍 Testing image HTML generation:")
    
    url1_html = report_gen._generate_image_html(mock_analysis_results, 'url1_screenshot', 'Original screenshot')
    url2_html = report_gen._generate_image_html(mock_analysis_results, 'url2_screenshot', 'Comparison screenshot')
    
    # Check if the correct filenames are used
    if 'visual_regression_report_20250813_085253_url1_screenshot.png' in url1_html:
        print("✅ URL1 screenshot correctly references copied file")
    else:
        print("❌ URL1 screenshot not using correct filename")
        print(f"   Generated HTML: {url1_html[:200]}...")
    
    if 'visual_regression_report_20250813_085253_url2_screenshot.png' in url2_html:
        print("✅ URL2 screenshot correctly references copied file")
    else:
        print("❌ URL2 screenshot not using correct filename")
        print(f"   Generated HTML: {url2_html[:200]}...")
    
    # Check if 'not available' messages are gone
    if 'not available' not in url1_html and 'not available' not in url2_html:
        print("✅ No 'not available' messages found")
    else:
        print("❌ 'Not available' messages still present")
    
    # Clean up test files
    try:
        os.remove(mock_screenshot1)
        os.remove(mock_screenshot2)
        os.rmdir(test_reports_dir)
        print("\n🧹 Test files cleaned up")
    except:
        pass
    
    print("\n🎯 Fix should now work for real HTML reports!")

if __name__ == "__main__":
    test_screenshot_path_fix()
