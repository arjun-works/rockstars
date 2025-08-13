#!/usr/bin/env python3
"""
Quick test to run a minimal analysis and check WCAG data flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression
import json

def test_simple_analysis():
    """Run a simple analysis to test WCAG data flow"""
    print("🧪 Testing WCAG data flow with simple analysis...")
    
    analyzer = VisualAIRegression()
    
    config = {
        'url1': 'https://example.com',
        'url2': 'https://example.com',
        'browser': 'chrome',
        'resolution': '1920x1080',
        'layout_shift': False,
        'font_color': False,
        'element_detection': False,
        'ai_analysis': False,
        'wcag_analysis': True  # Only test WCAG
    }
    
    def progress_callback(message):
        print(f"Progress: {message}")
    
    try:
        results = analyzer.run_analysis(config, progress_callback)
        
        print(f"✅ Analysis completed. Results keys: {list(results.keys())}")
        
        if 'wcag_analysis' in results:
            wcag = results['wcag_analysis']
            print(f"✅ WCAG analysis found! Keys: {list(wcag.keys())}")
            
            for url_key in ['url1', 'url2']:
                if url_key in wcag:
                    score = wcag[url_key].get('compliance_score', 'missing')
                    level = wcag[url_key].get('compliance_level', 'missing')
                    print(f"   {url_key}: Score={score}, Level={level}")
        else:
            print("❌ No WCAG analysis in results")
            
        return results
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_simple_analysis()
