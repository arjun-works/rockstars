"""
Test script to verify WCAG HTML report generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator

def test_wcag_html_generation():
    """Test the enhanced HTML report with WCAG results"""
    
    # Create mock WCAG analysis results
    mock_wcag_analysis = {
        'url1': {
            'url': 'https://example.com/original',
            'timestamp': '2025-01-06T10:30:00',
            'wcag_version': '2.2',
            'compliance_level': 'AA',
            'total_issues': 5,
            'critical_issues': 2,
            'compliance_score': 78.5,
            'categories': {
                'perceivable': {
                    'score': 85,
                    'issues': [
                        {
                            'guideline': '1.4.3',
                            'level': 'AA',
                            'description': 'Text contrast ratio is below 4.5:1',
                            'element': 'button.primary',
                            'impact': 'critical'
                        }
                    ]
                },
                'operable': {
                    'score': 92,
                    'issues': [
                        {
                            'guideline': '2.4.3',
                            'level': 'A',
                            'description': 'Focus order is not logical',
                            'element': 'navigation',
                            'impact': 'moderate'
                        }
                    ]
                },
                'understandable': {
                    'score': 88,
                    'issues': []
                },
                'robust': {
                    'score': 95,
                    'issues': []
                }
            },
            'wcag_22_features': {
                'target_size_compliant': False,
                'focus_appearance_score': 75.0,
                'dragging_alternative_score': 90.0
            }
        },
        'url2': {
            'url': 'https://example.com/modified',
            'timestamp': '2025-01-06T10:35:00',
            'wcag_version': '2.2',
            'compliance_level': 'AA',
            'total_issues': 3,
            'critical_issues': 1,
            'compliance_score': 85.2,
            'categories': {
                'perceivable': {
                    'score': 90,
                    'issues': [
                        {
                            'guideline': '1.4.3',
                            'level': 'AA',
                            'description': 'Some text still has low contrast',
                            'element': 'footer text',
                            'impact': 'critical'
                        }
                    ]
                },
                'operable': {
                    'score': 95,
                    'issues': []
                },
                'understandable': {
                    'score': 88,
                    'issues': []
                },
                'robust': {
                    'score': 95,
                    'issues': []
                }
            },
            'wcag_22_features': {
                'target_size_compliant': True,
                'focus_appearance_score': 85.0,
                'dragging_alternative_score': 92.0
            }
        }
    }
    
    # Mock analysis results
    mock_results = {
        'screenshots': {
            'url1': 'screenshot1.png',
            'url2': 'screenshot2.png'
        },
        'comparisons': {
            'ssim': 0.875,
            'mse': 125.3,
            'pixel_diff_percentage': 12.5,
            'layout_shifts': [],
            'color_differences': [],
            'element_changes': [],
            'missing_elements': []
        },
        'ai_analysis': {
            'anomalies': [],
            'confidence': 0.85
        },
        'summary': {
            'similarity_score': 0.875,
            'layout_differences': 0,
            'color_differences': 0
        },
        'wcag_analysis': mock_wcag_analysis,
        'reports': {
            'html': 'test_report.html',
            'pdf': 'test_report.pdf',
            'json': 'test_report.json',
            'visual': 'test_comparison.png',
            'sidebyside': 'test_sidebyside.png',
            'heatmap': 'test_heatmap.png',
            'package': 'test_package.zip'
        }
    }
    
    mock_config = {
        'url1': 'https://example.com/original',
        'url2': 'https://example.com/modified',
        'browser': 'chrome',
        'resolution': '1920x1080',
        'layout_shift': True,
        'font_color': True,
        'ai_analysis': True,
        'wcag_analysis': True
    }
    
    # Create report generator and test
    generator = ReportGenerator()
    
    try:
        print("Testing WCAG HTML generation...")
        
        # Test WCAG HTML generation specifically
        wcag_html = generator._generate_wcag_html(mock_results)
        print(f"WCAG HTML generated successfully. Length: {len(wcag_html)} characters")
        
        # Test full HTML report generation
        html_output = "test_wcag_enhanced_report.html"
        generator.generate_enhanced_html_report(mock_results, mock_config, html_output)
        
        if os.path.exists(html_output):
            print(f"✅ Enhanced HTML report with WCAG section generated: {html_output}")
            
            # Read and check if WCAG section is included
            with open(html_output, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if '♿ WCAG Accessibility Compliance Analysis' in content:
                print("✅ WCAG section header found in report")
            else:
                print("❌ WCAG section header NOT found in report")
                
            if 'Reference Page Accessibility Analysis' in content:
                print("✅ Reference page WCAG analysis found in report")
            else:
                print("❌ Reference page WCAG analysis NOT found")
                
            if 'Test Page Accessibility Analysis' in content:
                print("✅ Test page WCAG analysis found in report") 
            else:
                print("❌ Test page WCAG analysis NOT found")
                
            if 'WCAG 2.2 Specific Features' in content:
                print("✅ WCAG 2.2 features section found in report")
            else:
                print("❌ WCAG 2.2 features section NOT found")
                
            if 'Accessibility Comparison' in content:
                print("✅ WCAG comparison section found in report")
            else:
                print("❌ WCAG comparison section NOT found")
        else:
            print(f"❌ HTML report was not created: {html_output}")
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_wcag_html_generation()
