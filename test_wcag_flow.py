#!/usr/bin/env python3
"""Test script to check WCAG data flow"""

import json
import os
from pprint import pprint

def test_wcag_flow():
    """Test the WCAG data flow from reports"""
    print("Testing WCAG data flow...")
    
    # Find the most recent report
    reports_dir = "reports"
    json_files = [f for f in os.listdir(reports_dir) if f.endswith('.json')]
    
    if not json_files:
        print("No JSON reports found")
        return
    
    # Get the latest report
    latest_report = max(json_files, key=lambda x: os.path.getmtime(os.path.join(reports_dir, x)))
    report_path = os.path.join(reports_dir, latest_report)
    
    print(f"Reading report: {latest_report}")
    
    with open(report_path, 'r') as f:
        data = json.load(f)
    
    print(f"Report structure keys: {list(data.keys())}")
    
    # Check if wcag_analysis exists
    if 'wcag_analysis' in data:
        wcag = data['wcag_analysis']
        print(f"WCAG analysis keys: {list(wcag.keys())}")
        
        for url_key in ['url1', 'url2']:
            if url_key in wcag:
                url_data = wcag[url_key]
                print(f"\n{url_key.upper()} WCAG Data:")
                print(f"  URL: {url_data.get('url', 'Missing')}")
                print(f"  Compliance Score: {url_data.get('compliance_score', 'Missing')}")
                print(f"  Compliance Level: {url_data.get('compliance_level', 'Missing')}")
                print(f"  Total Issues: {url_data.get('total_issues', 'Missing')}")
                print(f"  Critical Issues: {url_data.get('critical_issues', 'Missing')}")
                
                # Check categories
                categories = url_data.get('categories', {})
                print(f"  Categories: {list(categories.keys())}")
                for cat_name, cat_data in categories.items():
                    print(f"    {cat_name}: {cat_data.get('score', 'Missing')}% ({len(cat_data.get('issues', []))} issues)")
    else:
        print("No wcag_analysis found in report")

if __name__ == "__main__":
    test_wcag_flow()
