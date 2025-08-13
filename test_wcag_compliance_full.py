#!/usr/bin/env python3
"""
Comprehensive WCAG compliance testing and verification
"""

import json
import os
import time

def run_wcag_compliance_test():
    """Run a complete WCAG compliance test and verify results"""
    print("🚀 Starting comprehensive WCAG compliance test...")
    
    # Step 1: Run a fresh analysis
    print("\n📋 Step 1: Analysis Configuration")
    print("- URL1: https://example.com (reference)")
    print("- URL2: https://httpbin.org/html (test)")
    print("- WCAG Analysis: ✅ Enabled")
    print("- Browser: Chrome")
    print("- Resolution: 1920x1080")
    
    print("\n⚠️  MANUAL STEPS REQUIRED:")
    print("1. Open the Visual AI Regression Module GUI")
    print("2. Enter URLs:")
    print("   - URL 1: https://example.com")
    print("   - URL 2: https://httpbin.org/html")
    print("3. Ensure 'WCAG Testing' checkbox is checked")
    print("4. Click 'Start Analysis' button")
    print("5. Wait for analysis to complete")
    print("6. Check the WCAG Compliance tab")
    print("7. Click the '🔄 Refresh WCAG Results' button if needed")
    
    print("\n📊 Expected Results:")
    print("✅ Compliance scores should be visible for both URLs")
    print("✅ Detailed WCAG analysis should appear in the text area")
    print("✅ Categories breakdown (Perceivable, Operable, Understandable, Robust)")
    print("✅ Issues count and compliance levels")
    
    # Step 2: Monitor for new reports
    print("\n⏳ Waiting for new analysis to complete...")
    print("(This script will monitor for new reports)")
    
    import glob
    initial_reports = set(glob.glob('reports/visual_regression_report_*.json'))
    
    # Wait for new report
    max_wait = 180  # 3 minutes
    wait_interval = 5
    waited = 0
    
    while waited < max_wait:
        current_reports = set(glob.glob('reports/visual_regression_report_*.json'))
        new_reports = current_reports - initial_reports
        
        if new_reports:
            print(f"\n✅ New report detected: {list(new_reports)[0]}")
            break
        
        print(f"⏳ Waiting... ({waited}/{max_wait}s)")
        time.sleep(wait_interval)
        waited += wait_interval
    
    if waited >= max_wait:
        print("\n⚠️  No new report detected within timeout")
        print("Please check if analysis is running correctly")
        return
    
    # Step 3: Verify WCAG data in the new report
    latest_report = max(glob.glob('reports/visual_regression_report_*.json'), key=os.path.getmtime)
    print(f"\n📄 Analyzing report: {os.path.basename(latest_report)}")
    
    with open(latest_report, 'r') as f:
        report_data = json.load(f)
    
    # Check WCAG data structure
    analysis_results = report_data.get('analysis_results', {})
    wcag_data = analysis_results.get('wcag_analysis', {})
    
    if not wcag_data:
        print("❌ WCAG analysis not found in report")
        return
    
    print("✅ WCAG analysis found in report")
    
    # Verify data structure
    for url_key in ['url1', 'url2']:
        if url_key in wcag_data:
            url_data = wcag_data[url_key]
            score = url_data.get('compliance_score', 0)
            level = url_data.get('compliance_level', 'Unknown')
            issues = url_data.get('total_issues', 0)
            
            print(f"\n📊 {url_key.upper()} Results:")
            print(f"   Score: {score}%")
            print(f"   Level: {level}")
            print(f"   Issues: {issues}")
            
            # Check categories
            categories = url_data.get('categories', {})
            for cat_name, cat_data in categories.items():
                cat_score = cat_data.get('score', 0)
                cat_issues = len(cat_data.get('issues', []))
                print(f"   {cat_name.capitalize()}: {cat_score}% ({cat_issues} issues)")
        else:
            print(f"❌ {url_key.upper()} data missing")
    
    # Check comparison
    if 'comparison' in wcag_data:
        comparison = wcag_data['comparison']
        assessment = comparison.get('assessment', 'No assessment')
        print(f"\n🔄 Comparison: {assessment}")
    
    print("\n🎯 VERIFICATION CHECKLIST:")
    print("□ Open the GUI and check the WCAG Compliance tab")
    print("□ Verify compliance scores are displayed for both URLs")
    print("□ Check that detailed analysis shows in the text area")
    print("□ Confirm category breakdowns are visible")
    print("□ Test the '🔄 Refresh WCAG Results' button")
    
    print("\n✅ WCAG compliance test completed!")
    print("If scores are not visible in the GUI, click the Refresh button.")

if __name__ == "__main__":
    run_wcag_compliance_test()
