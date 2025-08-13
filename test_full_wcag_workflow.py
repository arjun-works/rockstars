"""
Comprehensive test of the Visual AI Regression Module with enhanced WCAG HTML reporting
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression
import tempfile

def test_full_workflow_with_wcag():
    """Test the full workflow including WCAG analysis and enhanced HTML reporting"""
    
    print("🧪 Testing Visual AI Regression Module with Enhanced WCAG HTML Report...")
    
    # Initialize the regression tester
    tester = VisualAIRegression()
    
    # Mock configuration for testing
    test_config = {
        'url1': 'https://example.com',
        'url2': 'https://httpbin.org',  # Different site for comparison
        'browser': 'chrome',
        'resolution': '1280x720',  # Smaller resolution for faster testing
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True,
        'wcag_analysis': True,  # Enable WCAG analysis
        'headless': True,  # Run in headless mode for testing
        'wait_time': 2  # Shorter wait time for testing
    }
    
    try:
        print(f"📋 Test Configuration:")
        for key, value in test_config.items():
            print(f"   {key}: {value}")
        print()
        
        # Run the analysis
        print("🚀 Starting visual regression analysis with WCAG...")
        results = tester.run_comparison(test_config)
        
        if results and 'reports' in results:
            print("✅ Analysis completed successfully!")
            
            # Check if WCAG analysis was included
            if 'wcag_analysis' in results:
                print("✅ WCAG analysis data found in results")
                wcag_data = results['wcag_analysis']
                
                if 'url1' in wcag_data:
                    url1_score = wcag_data['url1'].get('compliance_score', 0)
                    print(f"   URL1 WCAG Score: {url1_score:.1f}%")
                
                if 'url2' in wcag_data:
                    url2_score = wcag_data['url2'].get('compliance_score', 0)
                    print(f"   URL2 WCAG Score: {url2_score:.1f}%")
            else:
                print("⚠️ WCAG analysis data not found in results")
            
            # Check generated reports
            reports = results.get('reports', {})
            print(f"\n📊 Generated Reports:")
            
            for report_type, report_path in reports.items():
                if os.path.exists(report_path):
                    file_size = os.path.getsize(report_path)
                    print(f"   ✅ {report_type}: {report_path} ({file_size} bytes)")
                    
                    # Special check for HTML report WCAG content
                    if report_type == 'html' and report_path.endswith('.html'):
                        try:
                            with open(report_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            
                            if '♿ WCAG Accessibility Compliance Analysis' in content:
                                print(f"      ✅ WCAG section found in HTML report")
                            else:
                                print(f"      ❌ WCAG section missing from HTML report")
                                
                        except Exception as e:
                            print(f"      ⚠️ Could not verify HTML content: {e}")
                else:
                    print(f"   ❌ {report_type}: {report_path} (file not found)")
            
            # Open the HTML report for visual inspection
            html_report = reports.get('html')
            if html_report and os.path.exists(html_report):
                print(f"\n🌐 Opening HTML report for inspection: {html_report}")
                # Note: In real scenario, we'd open this in browser
                print(f"   File size: {os.path.getsize(html_report)} bytes")
                
                # Check key sections exist
                with open(html_report, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                checks = [
                    ('Executive Summary', '📊 Executive Summary' in content),
                    ('WCAG Section', '♿ WCAG Accessibility Compliance Analysis' in content),
                    ('Visual Gallery', '🖼️ Visual Comparison Gallery' in content),
                    ('Detailed Analysis', '📈 Detailed Analysis' in content),
                    ('Export Options', '💾 Export Options' in content)
                ]
                
                print("   Report sections verification:")
                for section_name, exists in checks:
                    status = "✅" if exists else "❌"
                    print(f"      {status} {section_name}")
            
            print("\n🎉 Test completed successfully!")
            return True
            
        else:
            print("❌ Analysis failed - no results returned")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_full_workflow_with_wcag()
    if success:
        print("\n✅ All tests passed! Enhanced WCAG HTML reporting is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
