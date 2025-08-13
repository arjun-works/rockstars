#!/usr/bin/env python3
"""
Regenerate the HTML report from the existing analysis to test the screenshot fix
"""

import sys
import os
import json
sys.path.append(os.path.dirname(__file__))

from report_generator import ReportGenerator

def regenerate_html_with_fix():
    """Regenerate the HTML report with the screenshot fix"""
    print("🔄 Regenerating HTML report with screenshot fix...")
    
    # Load the existing JSON report data
    json_file = "reports/visual_regression_report_20250813_085253.json"
    
    if not os.path.exists(json_file):
        print("❌ JSON report file not found. Run an analysis first.")
        return
    
    # Load the analysis data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract analysis results
    analysis_results = data.get('analysis_results', {})
    config = data.get('config', {})
    
    # Add the reports info so the function can reference them
    reports = {
        'pdf': 'reports/visual_regression_report_20250813_085253.pdf',
        'json': 'reports/visual_regression_report_20250813_085253.json',
        'visual': 'reports/visual_regression_report_20250813_085253_visual_comparison.png',
        'sidebyside': 'reports/visual_regression_report_20250813_085253_side_by_side.png',
        'heatmap': 'reports/visual_regression_report_20250813_085253_difference_heatmap.png'
    }
    
    analysis_results['reports'] = reports
    
    # Create report generator
    report_gen = ReportGenerator()
    
    # Generate the fixed HTML report
    html_output = "reports/visual_regression_report_20250813_085253_FIXED.html"
    report_gen.generate_enhanced_html_report(analysis_results, config, html_output)
    
    print(f"✅ Fixed HTML report generated: {html_output}")
    
    # Check the HTML for screenshot references
    with open(html_output, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Look for the proper screenshot filenames
    if 'visual_regression_report_20250813_085253_url1_screenshot.png' in html_content:
        print("✅ URL1 screenshot properly referenced in HTML")
    else:
        print("❌ URL1 screenshot not found in HTML")
    
    if 'visual_regression_report_20250813_085253_url2_screenshot.png' in html_content:
        print("✅ URL2 screenshot properly referenced in HTML")
    else:
        print("❌ URL2 screenshot not found in HTML")
    
    if 'not available' in html_content:
        print("⚠️  'Not available' messages still present")
    else:
        print("✅ No 'not available' messages found")
    
    print(f"\n🌐 Open {html_output} in browser to verify screenshots are loading!")
    
    return html_output

if __name__ == "__main__":
    regenerate_html_with_fix()
