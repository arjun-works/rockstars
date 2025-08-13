#!/usr/bin/env python3
"""
Quick test to generate a real tabbed report using actual analysis
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from visual_ai_regression import VisualAIRegression

def test_real_tabbed_report():
    """Test the tabbed interface with a real analysis"""
    print("🚀 Testing tabbed interface with real analysis...")
    
    analyzer = VisualAIRegression()
    
    # Simple config for quick test
    config = {
        'url1': 'https://www.example.com',
        'url2': 'https://www.google.com',
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True
    }
    
    def progress_callback(message):
        print(f"📊 {message}")
    
    try:
        # Run analysis
        results = analyzer.run_analysis(config, progress_callback)
        
        # Check if HTML report was generated
        html_report = results.get('reports', {}).get('html', '')
        if html_report and os.path.exists(html_report):
            print(f"✅ Real tabbed HTML report generated: {html_report}")
            print("🎯 The tabbed interface is now active in real analysis reports!")
            
            # Open in browser
            from report_generator import ReportGenerator
            import webbrowser
            webbrowser.open(f'file:///{os.path.abspath(html_report)}')
            
        else:
            print("❌ HTML report not found")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_real_tabbed_report()
