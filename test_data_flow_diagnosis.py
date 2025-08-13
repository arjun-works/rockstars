#!/usr/bin/env python3
"""
Test script to diagnose data flow from analysis to HTML report.
This test checks if the issue is in data collection vs report generation.
"""

import os
import sys
import tempfile
from datetime import datetime
from PIL import Image, ImageDraw

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator

def simulate_gui_analysis_workflow():
    """Simulate the workflow that happens when GUI runs analysis and generates reports"""
    print("🔧 Testing GUI to HTML Data Flow")
    print("=" * 60)
    
    temp_dir = tempfile.mkdtemp(prefix="data_flow_test_")
    
    try:
        # Simulate analysis results that might come from the GUI workflow
        print("📊 Simulating analysis results from GUI workflow...")
        
        # This represents what might come from visual_ai_regression.py
        simulated_analysis_results = {
            'screenshots': {
                'url1': 'reference_screenshot.png',
                'url2': 'test_screenshot.png'
            },
            'comparisons': {
                'overall_similarity': 0.8432,  # This should show as 84.3%
                'differences_found': 23,
                'layout_shifts': [
                    {'element': 'header', 'distance': 12.5},
                    {'element': 'sidebar', 'distance': 8.3},
                    {'element': 'footer', 'distance': 5.1}
                ],
                'color_differences': [
                    {'element': 'button', 'old': '#blue', 'new': '#navy'},
                    {'element': 'background', 'old': '#fff', 'new': '#fafafa'}
                ],
                'missing_elements': [
                    {'element': 'nav-item', 'xpath': '//nav/li[3]'}
                ],
                'new_elements': [
                    {'element': 'banner', 'xpath': '//header/div[2]'},
                    {'element': 'icon', 'xpath': '//footer/span'}
                ]
            },
            'ai_analysis': {
                'anomalies': [
                    {'type': 'layout', 'confidence': 0.9},
                    {'type': 'color', 'confidence': 0.8},
                    {'type': 'content', 'confidence': 0.75},
                    {'type': 'structural', 'confidence': 0.85}
                ],
                'anomaly_detected': True
            },
            'wcag_analysis': {
                'url1': {
                    'compliance_score': 89.2,
                    'compliance_level': 'AA',
                    'total_issues': 6,
                    'critical_issues': 2
                },
                'url2': {
                    'compliance_score': 85.8,
                    'compliance_level': 'AA', 
                    'total_issues': 8,
                    'critical_issues': 3
                }
            },
            'summary': "Analysis found 84.3% similarity with 3 layout shifts, 2 color changes, and 4 AI anomalies.",
            'summary_dict': {
                'similarity_score': 0.8432,      # Should show as 84.3%
                'layout_differences': 3,         # Count of layout_shifts
                'color_differences': 2,          # Count of color_differences  
                'missing_elements': 1,           # Count of missing_elements
                'new_elements': 2,               # Count of new_elements
                'element_changes': 3,            # missing + new = 1 + 2
                'ai_anomalies': 4                # Count of AI anomalies
            }
        }
        
        print("✅ Simulated analysis results created")
        print(f"   📊 Expected Similarity: {simulated_analysis_results['summary_dict']['similarity_score']:.1%}")
        print(f"   📐 Expected Layout: {simulated_analysis_results['summary_dict']['layout_differences']}")
        print(f"   🎨 Expected Color: {simulated_analysis_results['summary_dict']['color_differences']}")
        print(f"   🔄 Expected Element: {simulated_analysis_results['summary_dict']['element_changes']}")
        print(f"   🤖 Expected AI: {simulated_analysis_results['summary_dict']['ai_anomalies']}")
        print(f"   ♿ Expected WCAG: {(simulated_analysis_results['wcag_analysis']['url1']['compliance_score'] + simulated_analysis_results['wcag_analysis']['url2']['compliance_score']) / 2:.1f}%")
        
        # Generate HTML report using the same process as GUI
        config = {
            'url1': 'https://example.com/reference',
            'url2': 'https://example.com/test',
            'layout_shift': True,
            'font_color': True,
            'element_analysis': True,
            'ai_analysis': True,
            'wcag_compliance': True
        }
        
        print("\n🔄 Generating HTML report through normal workflow...")
        
        report_generator = ReportGenerator(output_dir=temp_dir)
        
        # This simulates the comprehensive report generation that GUI calls
        reports = report_generator.generate_comprehensive_report(simulated_analysis_results, config)
        
        html_path = reports.get('html', '')
        
        if html_path and os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            print(f"✅ HTML report generated: {os.path.basename(html_path)}")
            
            # Check what actually appears in the HTML
            print("\n🔍 Analyzing HTML Executive Summary content...")
            
            import re
            
            # Extract all percentages
            percentage_pattern = r'<div class="number">([^<]+)</div>'
            number_matches = re.findall(percentage_pattern, html_content)
            
            print(f"   📈 Found number values in Executive Summary:")
            for i, match in enumerate(number_matches[:6]):  # First 6 should be the summary cards
                print(f"      {i+1}. {match}")
            
            # Check if the expected values are present
            expected_similarity = f"{simulated_analysis_results['summary_dict']['similarity_score']:.1%}"
            expected_values = [
                expected_similarity,
                str(simulated_analysis_results['summary_dict']['layout_differences']),
                str(simulated_analysis_results['summary_dict']['color_differences']),
                str(simulated_analysis_results['summary_dict']['element_changes']),
                str(simulated_analysis_results['summary_dict']['ai_anomalies'])
            ]
            
            print(f"\n   🎯 Checking for expected values:")
            accuracy_issues = []
            
            for expected_val in expected_values:
                if expected_val in html_content:
                    print(f"      ✅ Found: {expected_val}")
                else:
                    print(f"      ❌ Missing: {expected_val}")
                    accuracy_issues.append(expected_val)
            
            # Check Executive Summary structure
            if "📊 Executive Summary" in html_content:
                print(f"   ✅ Executive Summary section found")
            else:
                print(f"   ❌ Executive Summary section missing")
                accuracy_issues.append("Executive Summary section")
            
            # Final diagnosis
            print(f"\n📈 Data Flow Analysis Results:")
            if len(accuracy_issues) == 0:
                print(f"   🎉 SUCCESS: All expected values appear correctly in HTML")
                print(f"   ✅ Data flows correctly from analysis to HTML report")
                print(f"   ✅ Executive Summary percentages are accurate")
                
                # Show the actual similarity percentage found
                if number_matches:
                    print(f"   📊 Similarity percentage in HTML: {number_matches[0]}")
                
                return True
            else:
                print(f"   ⚠️ ISSUES FOUND: {len(accuracy_issues)} values missing or incorrect")
                print(f"   🔍 Missing values: {accuracy_issues}")
                print(f"   💡 This suggests a data flow issue from analysis to HTML")
                return False
        else:
            print(f"❌ HTML report not generated")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        print(f"\n📁 Test files preserved for inspection:")
        print(f"   Directory: {temp_dir}")

if __name__ == "__main__":
    print("🧪 GUI to HTML Data Flow Diagnosis")
    print("Testing if data flows correctly from analysis to HTML report")
    print("=" * 60)
    
    success = simulate_gui_analysis_workflow()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST PASSED: Data flow is correct, percentages are accurate!")
    else:
        print("❌ TEST FAILED: Data flow issues detected")
        print("💡 RECOMMENDATION: Check how summary_dict is populated in visual_ai_regression.py")
    
    print("🔍 Compare with actual GUI results to identify discrepancies.")
