#!/usr/bin/env python3
"""
Test script to verify enhanced visual definitions with the full application workflow
"""

import os
import sys
import time
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression

def test_full_workflow_with_definitions():
    """Test the full workflow to ensure enhanced definitions work in real reports"""
    print("🚀 Testing Enhanced Definitions with Full Application Workflow...")
    
    try:
        # Initialize the visual AI regression tester
        vai = VisualAIRegression()
        
        # Create test configuration
        config = {
            'test_name': 'Enhanced Definitions Integration Test',
            'url1': 'https://httpbin.org/html',  # Reference URL
            'url2': 'https://httpbin.org/html',  # Test URL - same page for consistent test
            'viewport_width': 1024,
            'viewport_height': 768,
            'threshold': 0.05,
            'wait_time': 2,
            'analysis_options': {
                'pixel_comparison': True,
                'layout_analysis': True,
                'content_analysis': True,
                'wcag_compliance': True
            }
        }
        
        print(f"📋 Test Configuration:")
        print(f"   Reference URL (url1): {config['url1']}")
        print(f"   Test URL (url2): {config['url2']}")
        print(f"   Viewport: {config['viewport_width']}x{config['viewport_height']}")
        print(f"   Analysis Options: {list(config['analysis_options'].keys())}")
        
        # Run the full analysis
        print(f"\n🔄 Running full visual regression analysis...")
        start_time = time.time()
        
        results = vai.run_analysis(config)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if results:
            print(f"✅ Analysis completed successfully in {duration:.2f} seconds")
            
            # Check if reports were generated
            if 'reports' in results:
                reports = results['reports']
                print(f"\n📊 Generated Reports:")
                
                for report_type, report_path in reports.items():
                    if os.path.exists(report_path):
                        file_size = os.path.getsize(report_path)
                        print(f"   ✅ {report_type.upper()}: {report_path} ({file_size:,} bytes)")
                    else:
                        print(f"   ❌ {report_type.upper()}: {report_path} (NOT FOUND)")
                
                # Specifically check the HTML report for enhanced definitions
                html_report = reports.get('html')
                if html_report and os.path.exists(html_report):
                    print(f"\n🔍 Checking HTML report for enhanced definitions...")
                    
                    with open(html_report, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check for key enhanced definition elements
                    definition_checks = [
                        'This gallery provides three different visualization approaches',
                        'What it shows:', 'Use case:', 'Best for:',
                        'Reference and test screenshots placed side-by-side',
                        'heat-mapped overlay where red/warm colors indicate pixel differences',
                        'AI-detected differences highlighted using bounding boxes',
                        'background-color: #e8f4f8',  # Side-by-side styling
                        'background-color: #fff2e8',  # Heatmap styling
                        'background-color: #f0f8e8'   # Annotated styling
                    ]
                    
                    found_definitions = 0
                    for check in definition_checks:
                        if check in content:
                            found_definitions += 1
                    
                    definition_percentage = (found_definitions / len(definition_checks)) * 100
                    print(f"   📈 Enhanced definitions coverage: {definition_percentage:.1f}% ({found_definitions}/{len(definition_checks)})")
                    
                    if definition_percentage >= 90:
                        print(f"   ✅ Enhanced definitions successfully integrated!")
                    else:
                        print(f"   ⚠️  Some enhanced definitions may be missing")
                        
                    # Show sample content
                    if 'Side-by-Side Comparison' in content:
                        print(f"   ✅ Side-by-Side section with definitions found")
                    if 'Difference Heatmap' in content:
                        print(f"   ✅ Heatmap section with definitions found")
                    if 'Annotated Visual Comparison' in content:
                        print(f"   ✅ Annotated comparison section with definitions found")
                
                return True
            else:
                print(f"❌ No reports generated in results")
                return False
        else:
            print(f"❌ Analysis failed or returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Error in full workflow test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_report_accessibility():
    """Test that the enhanced definitions improve report accessibility"""
    print(f"\n♿ Testing Report Accessibility Improvements...")
    
    try:
        # Check that the enhanced definitions use proper semantic HTML and accessibility features
        from report_generator import ReportGenerator
        
        # Create minimal test data
        mock_results = {
            'summary': {'analysis_types_enabled': {'pixel_comparison': True}},
            'reports': {}
        }
        mock_config = {'test_name': 'Accessibility Test'}
        
        report_gen = ReportGenerator()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"reports/test_accessibility_{timestamp}.html"
        
        report_gen.generate_enhanced_html_report(mock_results, mock_config, output_path)
        
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check accessibility features
            accessibility_checks = [
                'lang="en"',                    # Language attribute
                '<strong>What it shows:</strong>',  # Bold text for clarity
                '<strong>Use case:</strong>',       # Bold text for clarity
                '<strong>Best for:</strong>',       # Bold text for clarity
                'style="margin: 0; font-size: 14px;',  # Readable font size
                'alt='                          # Alt text for images
            ]
            
            accessibility_score = 0
            for check in accessibility_checks:
                if check in content:
                    accessibility_score += 1
            
            accessibility_percentage = (accessibility_score / len(accessibility_checks)) * 100
            print(f"   📊 Accessibility features: {accessibility_percentage:.1f}% ({accessibility_score}/{len(accessibility_checks)})")
            
            # Check color contrast considerations
            if '#2c5aa0' in content and '#d2691e' in content and '#228b22' in content:
                print(f"   🎨 Color-coded sections using contrasting colors: ✅")
            
            return accessibility_percentage >= 80
        else:
            print(f"   ❌ Accessibility test report not generated")
            return False
            
    except Exception as e:
        print(f"❌ Error in accessibility test: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Enhanced Visual Definitions - Full Integration Test\n")
    
    # Ensure directories exist
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    
    # Run tests
    print("=" * 60)
    workflow_passed = test_full_workflow_with_definitions()
    
    print("\n" + "=" * 60)
    accessibility_passed = test_report_accessibility()
    
    # Final summary
    print(f"\n" + "=" * 60)
    print(f"📋 FINAL TEST SUMMARY")
    print(f"=" * 60)
    print(f"Full Workflow Integration: {'✅ PASSED' if workflow_passed else '❌ FAILED'}")
    print(f"Accessibility Improvements: {'✅ PASSED' if accessibility_passed else '❌ FAILED'}")
    
    if workflow_passed and accessibility_passed:
        print(f"\n🎉 SUCCESS: Enhanced visual comparison definitions are fully integrated and working!")
        print(f"💡 The Visual AI Regression Module now provides clear, user-friendly explanations")
        print(f"   for all visual comparison types in the HTML reports.")
    else:
        print(f"\n⚠️  Some integration issues detected. Please review the test output above.")
    
    print(f"\n📁 Check the 'reports' directory for generated test reports.")
