#!/usr/bin/env python3
"""
Test the screenshot fix with a real analysis run
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from visual_ai_regression import VisualAIRegression

def test_real_screenshot_fix():
    """Test the screenshot fix with real analysis"""
    print("🚀 Testing screenshot fix with real analysis...")
    
    analyzer = VisualAIRegression()
    
    # Simple config for quick test
    config = {
        'url1': 'https://www.example.com',
        'url2': 'https://www.google.com',
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True
    }
    
    def progress_callback(message):
        print(f"📊 {message}")
    
    try:
        print("🔍 Running analysis...")
        results = analyzer.run_analysis(config, progress_callback)
        
        print("\n📊 Checking screenshot paths in results:")
        screenshots = results.get('analysis_results', {}).get('screenshots', {})
        print(f"   URL1 screenshot: {screenshots.get('url1', 'NOT FOUND')}")
        print(f"   URL2 screenshot: {screenshots.get('url2', 'NOT FOUND')}")
        
        # Check if HTML report was generated
        html_report = results.get('reports', {}).get('html', '')
        if html_report and os.path.exists(html_report):
            print(f"\n✅ HTML report generated: {html_report}")
            
            # Check the HTML content for screenshot references
            with open(html_report, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            url1_found = 'url1_screenshot.png' in html_content
            url2_found = 'url2_screenshot.png' in html_content
            not_available = 'not available' in html_content
            
            print(f"📊 Screenshot reference check:")
            print(f"   URL1 screenshot in HTML: {'✅' if url1_found else '❌'}")
            print(f"   URL2 screenshot in HTML: {'✅' if url2_found else '❌'}")
            print(f"   'Not available' messages: {'❌ Still present' if not_available else '✅ Removed'}")
            
            if url1_found and url2_found and not not_available:
                print("\n🎉 SUCCESS: Screenshot fix is working in real analysis!")
            else:
                print("\n⚠️  Issue may still exist - check the HTML report manually")
                
        else:
            print("❌ HTML report not found")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_real_screenshot_fix()
