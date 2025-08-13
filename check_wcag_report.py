import json
import glob
import os

# Find the most recent report
reports = glob.glob('reports/visual_regression_report_*.json')
if reports:
    latest = max(reports, key=os.path.getmtime)
    print(f'Checking latest report: {os.path.basename(latest)}')
    
    with open(latest, 'r') as f:
        data = json.load(f)
    
    # Check for WCAG data
    analysis_results = data.get('analysis_results', {})
    print(f'Analysis results keys: {list(analysis_results.keys())}')
    
    if 'wcag_analysis' in analysis_results:
        wcag = analysis_results['wcag_analysis']
        print(f'WCAG analysis found with keys: {list(wcag.keys())}')
        
        if 'url1' in wcag:
            url1_data = wcag['url1']
            print(f'URL1 WCAG score: {url1_data.get("compliance_score", "missing")}')
            print(f'URL1 categories: {list(url1_data.get("categories", {}).keys())}')
        
        if 'url2' in wcag:
            url2_data = wcag['url2']
            print(f'URL2 WCAG score: {url2_data.get("compliance_score", "missing")}')
            print(f'URL2 categories: {list(url2_data.get("categories", {}).keys())}')
    else:
        print('No WCAG analysis found in analysis_results')
else:
    print('No reports found')
