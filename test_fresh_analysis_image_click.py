#!/usr/bin/env python3
"""
Test script to run a fresh analysis and verify image click functionality works correctly.
This will generate a new report with the latest image click enhancement.
"""

import os
import sys
import webbrowser
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression

def run_fresh_analysis_test():
    """Run a fresh analysis to test image click functionality"""
    print("🧪 Running Fresh Analysis with Image Click Functionality...")
    
    # Configuration for the test
    config = {
        'url1': 'https://example.com',
        'url2': 'https://httpbin.org/html',
        'viewport_width': 1920,
        'viewport_height': 1080,
        'wait_time': 3,
        'screenshot_path': 'screenshots',
        'enable_ai_analysis': True,
        'generate_reports': True
    }
    
    print(f"📋 Test Configuration:")
    print(f"   URL 1: {config['url1']}")
    print(f"   URL 2: {config['url2']}")
    print(f"   Viewport: {config['viewport_width']}x{config['viewport_height']}")
    print(f"   AI Analysis: {config['enable_ai_analysis']}")
    
    try:
        # Create the regression testing instance
        regression_tester = VisualAIRegression()
        
        # Run the analysis
        print(f"\n🚀 Starting visual regression analysis...")
        analysis_results = regression_tester.run_analysis(config)
        
        if analysis_results:
            print(f"✅ Analysis completed successfully!")
            
            # Check if HTML report was generated
            reports = analysis_results.get('reports', {})
            html_report = reports.get('html')
            
            if html_report and os.path.exists(html_report):
                print(f"✅ HTML report generated: {html_report}")
                
                # Verify the HTML contains image click functionality
                with open(html_report, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Check for key components
                checks = {
                    'openImage function': 'function openImage(src)' in html_content,
                    'onclick handlers': 'onclick="openImage(this.src)"' in html_content,
                    'Modal CSS': 'z-index: 10000' in html_content,
                    'Close button': 'closeBtn.innerHTML = \'✕\'' in html_content,
                    'Image styling': 'cursor: pointer' in html_content,
                    'Image tags': '<img' in html_content
                }
                
                print(f"\n🔍 Image Click Functionality Verification:")
                all_passed = True
                for check_name, passed in checks.items():
                    status = "✅ PASS" if passed else "❌ FAIL"
                    print(f"   {status}: {check_name}")
                    if not passed:
                        all_passed = False
                
                if all_passed:
                    print(f"\n✅ All image click functionality checks passed!")
                    print(f"🌐 Opening report for manual testing...")
                    
                    try:
                        webbrowser.open(f'file://{os.path.abspath(html_report)}')
                        print(f"✅ Report opened in browser")
                        
                        print(f"\n📖 Manual Testing Instructions:")
                        print(f"1. Navigate to the 'Visual Comparison' tab")
                        print(f"2. Click on any image to test the modal functionality")
                        print(f"3. Verify:")
                        print(f"   - Images open in full-screen modal")
                        print(f"   - Dark overlay background (90% opacity)")
                        print(f"   - Close button (✕) in top-right corner")
                        print(f"   - Click outside image or close button to close")
                        print(f"   - Body scroll disabled when modal open")
                        
                    except Exception as e:
                        print(f"⚠️ Could not open browser: {e}")
                        print(f"📁 Manual open: {html_report}")
                
                else:
                    print(f"\n❌ Some image click functionality checks failed!")
                    print(f"📁 Report location: {html_report}")
                    
                    # Show specific missing components
                    if 'function openImage(src)' not in html_content:
                        print(f"   ❌ Missing openImage JavaScript function")
                    if 'onclick="openImage(this.src)"' not in html_content:
                        print(f"   ❌ Missing onclick handlers on images")
                    if '<img' not in html_content:
                        print(f"   ❌ No images found in HTML")
                
                return html_report, all_passed
                
            else:
                print(f"❌ HTML report not found or not generated")
                return None, False
                
        else:
            print(f"❌ Analysis failed to complete")
            return None, False
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return None, False

def main():
    """Main test function"""
    print("🚀 Fresh Analysis Test for Image Click Functionality")
    print("=" * 60)
    
    html_path, functionality_working = run_fresh_analysis_test()
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY:")
    
    if html_path and functionality_working:
        print("✅ SUCCESS: Image click functionality is working correctly!")
        print(f"📁 Report: {html_path}")
        print("🔧 Manual testing: Click on images in the Visual Comparison tab")
    elif html_path and not functionality_working:
        print("⚠️ PARTIAL: Report generated but image click functionality issues detected")
        print(f"📁 Report: {html_path}")
        print("🔧 Check the report manually and review the implementation")
    else:
        print("❌ FAILED: Unable to generate report or run analysis")
        print("🔧 Check the configuration and try again")

if __name__ == "__main__":
    main()
