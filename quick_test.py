#!/usr/bin/env python3
"""
Quick test to run a visual regression analysis and verify all functionality is working.
"""

import os
import sys
import time
import webbrowser
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_quick_test():
    """Run a quick test of the visual regression module"""
    print("🚀 Starting Quick Test of Visual AI Regression Module")
    print("=" * 60)
    
    # Import the visual_ai_regression module
    try:
        import visual_ai_regression
        print("✅ Module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import module: {e}")
        return False
    
    # Set up test URLs
    url1 = "https://example.com"
    url2 = "https://example.org"
    
    print(f"🌐 Testing URLs:")
    print(f"   Original: {url1}")
    print(f"   Comparison: {url2}")
    
    # Run the analysis
    try:
        print("🔍 Running visual regression analysis...")
        start_time = time.time()
        
        result = visual_ai_regression.run_analysis(
            url1=url1,
            url2=url2,
            analysis_options={
                'layout_analysis': True,
                'color_analysis': True,
                'element_analysis': True,
                'ai_analysis': True,
                'wcag_analysis': True,
                'screenshot_comparison': True
            }
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Analysis completed in {duration:.2f} seconds")
        
        if result and 'report_path' in result:
            print(f"📄 Report generated: {result['report_path']}")
            
            # Open the report
            if os.path.exists(result['report_path']):
                print("🌐 Opening report in browser...")
                webbrowser.open(f"file://{os.path.abspath(result['report_path'])}")
                print("✅ Report opened successfully")
                return True
            else:
                print("❌ Report file not found")
                return False
        else:
            print("❌ Analysis failed or no report generated")
            return False
            
    except Exception as e:
        print(f"❌ Analysis failed with error: {e}")
        return False

if __name__ == "__main__":
    success = run_quick_test()
    if success:
        print("\n🎉 Quick test completed successfully!")
        print("All functionality appears to be working correctly.")
    else:
        print("\n❌ Quick test failed!")
        print("Please check the error messages above.")
