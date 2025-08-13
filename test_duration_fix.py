#!/usr/bin/env python3
"""
Test Analysis Duration Fix
This script tests that the analysis duration is properly calculated and displayed.
"""

import os
import sys
import time
from datetime import datetime

# Add project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from visual_ai_regression import VisualAIRegression
    from report_generator import ReportGenerator
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_duration_calculation():
    """Test that duration is properly calculated during analysis"""
    print("⏱️ TESTING ANALYSIS DURATION CALCULATION")
    print("=" * 50)
    
    # Create a simple config for testing
    config = {
        'url1': 'https://httpbin.org/html',
        'url2': 'https://httpbin.org/html',  # Same URL for quick test
        'browser': 'chrome',
        'resolution': '1280x720',
        'visual_comparison': True,
        'ai_analysis': False,  # Disable AI for faster test
        'wcag_analysis': False,  # Disable WCAG for faster test
        'capture_screenshots': True
    }
    
    print("🔍 Running quick analysis to test duration calculation...")
    print(f"📅 Test started at: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        # Create analyzer and run analysis
        analyzer = VisualAIRegression()
        
        def progress_callback(message):
            print(f"   📊 {message}")
        
        # Run the analysis
        start_test_time = time.time()
        results = analyzer.run_analysis(config, progress_callback)
        end_test_time = time.time()
        
        test_duration = end_test_time - start_test_time
        print(f"📅 Test completed at: {datetime.now().strftime('%H:%M:%S')}")
        print(f"⏱️ Total test duration: {test_duration:.1f} seconds")
        
        # Check if duration was calculated
        if results and 'analysis_results' in results:
            analysis_results = results['analysis_results']
            
            # Check for duration in analysis_results
            duration = analysis_results.get('duration', 'N/A')
            timestamp = analysis_results.get('timestamp', 'N/A')
            
            print("\n📊 DURATION CALCULATION RESULTS:")
            print("-" * 40)
            print(f"✅ Duration in analysis_results: {duration}")
            print(f"✅ Timestamp in analysis_results: {timestamp}")
            
            # Check if duration is not N/A
            if duration != 'N/A' and 'seconds' in duration:
                print("✅ Duration calculation working correctly!")
                
                # Extract duration value
                try:
                    duration_value = float(duration.split()[0])
                    if duration_value > 0:
                        print(f"✅ Duration value is valid: {duration_value} seconds")
                        return True, duration, timestamp
                    else:
                        print("❌ Duration value is zero or negative")
                        return False, duration, timestamp
                except:
                    print("❌ Could not parse duration value")
                    return False, duration, timestamp
            else:
                print("❌ Duration calculation failed - still showing N/A")
                return False, duration, timestamp
        else:
            print("❌ No analysis results returned")
            return False, "N/A", "N/A"
            
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return False, "Error", "Error"

def test_duration_in_html_report():
    """Test that duration appears correctly in HTML reports"""
    print("\n📄 TESTING DURATION IN HTML REPORTS")
    print("=" * 50)
    
    # Create test data with duration
    test_analysis_results = {
        'duration': '45.3 seconds',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'screenshots': {},
        'comparisons': {
            'ssim_score': 0.95,
            'mse_score': 123.4,
            'psnr_score': 28.5
        },
        'summary_dict': {
            'overall_similarity': 95.0
        }
    }
    
    test_config = {
        'analysis_type': 'Duration Test',
        'urls': {'url1': 'test1', 'url2': 'test2'}
    }
    
    try:
        # Generate HTML report
        report_generator = ReportGenerator()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"duration_test_report_{timestamp}.html"
        report_path = os.path.join("reports", report_filename)
        
        os.makedirs("reports", exist_ok=True)
        
        print("📄 Generating test HTML report...")
        report_generator.generate_enhanced_html_report(test_analysis_results, test_config, report_path)
        
        if os.path.exists(report_path):
            print(f"✅ Report generated: {report_filename}")
            
            # Check HTML content for duration
            with open(report_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Look for duration in HTML
            duration_found = '45.3 seconds' in html_content
            timestamp_found = test_analysis_results['timestamp'] in html_content
            
            print("\n📊 HTML REPORT DURATION CHECK:")
            print("-" * 40)
            status_duration = "✅" if duration_found else "❌"
            status_timestamp = "✅" if timestamp_found else "❌"
            print(f"{status_duration} Duration found in HTML: 45.3 seconds")
            print(f"{status_timestamp} Timestamp found in HTML")
            
            if duration_found and timestamp_found:
                print("✅ Duration properly displayed in HTML report!")
                return True, report_path
            else:
                print("❌ Duration not properly displayed in HTML report")
                return False, report_path
        else:
            print("❌ HTML report was not generated")
            return False, None
            
    except Exception as e:
        print(f"❌ Error generating HTML report: {str(e)}")
        return False, None

def main():
    """Main test function"""
    print("⏱️ ANALYSIS DURATION FIX VERIFICATION")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test 1: Duration calculation during analysis
    success1, duration, timestamp = test_duration_calculation()
    
    # Test 2: Duration display in HTML reports
    success2, report_path = test_duration_in_html_report()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DURATION FIX VERIFICATION SUMMARY:")
    print("=" * 60)
    
    if success1:
        print("✅ Duration calculation during analysis: WORKING")
        print(f"   Calculated duration: {duration}")
        print(f"   Analysis timestamp: {timestamp}")
    else:
        print("❌ Duration calculation during analysis: FAILED")
    
    if success2:
        print("✅ Duration display in HTML reports: WORKING")
        if report_path:
            print(f"   Test report: {os.path.basename(report_path)}")
    else:
        print("❌ Duration display in HTML reports: FAILED")
    
    if success1 and success2:
        print("\n🎉 DURATION FIX VERIFICATION SUCCESSFUL!")
        print("✅ Analysis duration is now properly calculated and displayed")
        print("✅ No more 'N/A' duration values in reports")
        print("✅ Timing information includes both duration and timestamp")
    else:
        print("\n⚠️ Some duration fix tests failed")
        print("🔧 Check error messages above for details")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
