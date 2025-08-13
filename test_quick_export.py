#!/usr/bin/env python3
"""
Quick test to verify that PDF and JSON export links are working in a real visual regression test
"""

import os
import sys
import logging
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression

def quick_export_test():
    """Quick test of export functionality"""
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    print("=== Quick Export Links Test ===")
    
    try:
        # Simple test configuration
        config = {
            'url1': 'https://httpbin.org/html',
            'url2': 'https://httpbin.org/forms/post',
            'browser': 'chrome',
            'resolution': '1280x720',
            'layout_shift': True,
            'font_color': True,
            'element_detection': True,
            'ai_analysis': True,
            'wcag_analysis': True
        }
        
        print("🚀 Running quick visual regression test...")
        regression = VisualAIRegression()
        results = regression.run_analysis(config)
        
        if not results or 'reports' not in results:
            print("❌ Test failed!")
            return False
        
        print("✅ Visual regression test completed successfully")
        
        # Check the reports that were generated
        reports_data = results.get('reports', {})
        
        if 'html' in reports_data:
            html_path = reports_data['html']
            print(f"📊 HTML Report: {html_path}")
            
            if os.path.exists(html_path):
                # Check for corresponding PDF, JSON, ZIP files
                base_name = html_path.replace('.html', '')
                
                pdf_path = base_name + '.pdf'
                json_path = base_name + '.json'
                zip_path = base_name + '_complete_package.zip'
                
                pdf_exists = os.path.exists(pdf_path)
                json_exists = os.path.exists(json_path)
                zip_exists = os.path.exists(zip_path)
                
                print(f"📄 PDF Report: {'✅' if pdf_exists else '❌'} {pdf_path}")
                print(f"📊 JSON Data: {'✅' if json_exists else '❌'} {json_path}")
                print(f"📦 ZIP Package: {'✅' if zip_exists else '❌'} {zip_path}")
                
                if pdf_exists and json_exists and zip_exists:
                    print("🎉 All export files generated successfully!")
                    
                    # Show file sizes
                    pdf_size = os.path.getsize(pdf_path)
                    json_size = os.path.getsize(json_path)
                    zip_size = os.path.getsize(zip_path)
                    
                    print(f"📏 File sizes: PDF({pdf_size:,}B), JSON({json_size:,}B), ZIP({zip_size:,}B)")
                    return True
                else:
                    print("❌ Some export files are missing")
                    return False
            else:
                print(f"❌ HTML report not found: {html_path}")
                return False
        else:
            print("❌ No HTML report in results")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = quick_export_test()
    if success:
        print("\n✅ Quick export test PASSED! PDF and JSON exports are working correctly.")
    else:
        print("\n❌ Quick export test FAILED!")
    
    sys.exit(0 if success else 1)
