#!/usr/bin/env python3
"""
Test script to verify that original screenshots are now properly loading in HTML reports.
This test will generate a new analysis and check that screenshots are available.
"""

import os
import sys
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression

def test_screenshot_loading_fix():
    """Test that original screenshots now load properly in HTML reports"""
    print("🔧 Testing Screenshot Loading Fix...")
    
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
    print(f"   Testing screenshot copying and HTML accessibility")
    
    try:
        # Create the regression testing instance
        regression_tester = VisualAIRegression()
        
        # Run the analysis
        print(f"\n🚀 Starting analysis to test screenshot loading...")
        analysis_results = regression_tester.run_analysis(config)
        
        if analysis_results:
            print(f"✅ Analysis completed successfully!")
            
            # Check if HTML report was generated
            reports = analysis_results.get('reports', {})
            html_report = reports.get('html')
            
            if html_report and os.path.exists(html_report):
                print(f"✅ HTML report generated: {html_report}")
                
                # Check for copied screenshot files in reports directory
                report_dir = os.path.dirname(html_report)
                base_name = os.path.splitext(os.path.basename(html_report))[0]
                
                print(f"\n📁 Checking for copied screenshot files in {report_dir}:")
                
                # Expected screenshot file patterns
                expected_files = [
                    f"{base_name}_url1_screenshot.png",
                    f"{base_name}_url2_screenshot.png"
                ]
                
                found_screenshots = []
                for expected_file in expected_files:
                    file_path = os.path.join(report_dir, expected_file)
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        print(f"   ✅ {expected_file}: Found ({file_size} bytes)")
                        found_screenshots.append(expected_file)
                    else:
                        print(f"   ❌ {expected_file}: Not found")
                
                # Check HTML content for proper image references
                print(f"\n📄 Checking HTML content for screenshot references:")
                
                with open(html_report, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Check for screenshot image tags
                screenshot_checks = {
                    'URL1 screenshot image tag': f'{base_name}_url1_screenshot.png' in html_content,
                    'URL2 screenshot image tag': f'{base_name}_url2_screenshot.png' in html_content,
                    'Image click handlers': 'onclick="openImage(' in html_content,
                    'Visual Comparison tab': 'visual-comparison' in html_content
                }
                
                all_checks_passed = True
                for check_name, passed in screenshot_checks.items():
                    status = "✅ PASS" if passed else "❌ FAIL"
                    print(f"   {status}: {check_name}")
                    if not passed:
                        all_checks_passed = False
                
                # Summary of results
                print(f"\n📋 Test Results Summary:")
                if found_screenshots:
                    print(f"   ✅ Screenshot files copied: {len(found_screenshots)}/{len(expected_files)}")
                    for screenshot in found_screenshots:
                        print(f"      - {screenshot}")
                else:
                    print(f"   ❌ No screenshot files found in reports directory")
                
                if all_checks_passed and found_screenshots:
                    print(f"   ✅ HTML content properly references screenshot files")
                    print(f"   ✅ Image click functionality intact")
                    
                    # Open the report for manual verification
                    import webbrowser
                    try:
                        webbrowser.open(f'file://{os.path.abspath(html_report)}')
                        print(f"   🌐 Report opened for manual verification")
                        print(f"\n🔧 Manual Test Instructions:")
                        print(f"   1. Navigate to the 'Visual Comparison' tab")
                        print(f"   2. Verify that original screenshots (URL 1 and URL 2) are now visible")
                        print(f"   3. Click on the screenshot images to test modal functionality")
                        print(f"   4. Confirm images open in full-screen view")
                    except Exception as e:
                        print(f"   ⚠️ Could not open browser: {e}")
                    
                    return True, html_report
                else:
                    print(f"   ❌ Some checks failed - screenshot loading may still have issues")
                    return False, html_report
                
            else:
                print(f"❌ HTML report not found or not generated")
                return False, None
                
        else:
            print(f"❌ Analysis failed to complete")
            return False, None
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def main():
    """Main test function"""
    print("🔧 Screenshot Loading Fix Verification Test")
    print("=" * 60)
    
    success, html_path = test_screenshot_loading_fix()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ SUCCESS: Screenshot loading fix implemented and working!")
        print(f"📁 Report: {html_path}")
        print("🎯 Original screenshots should now be visible and clickable")
    else:
        print("❌ ISSUES: Screenshot loading fix needs additional work")
        if html_path:
            print(f"📁 Report (partial): {html_path}")
        print("🔧 Check the error messages above for details")

if __name__ == "__main__":
    main()
