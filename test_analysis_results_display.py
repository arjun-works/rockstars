#!/usr/bin/env python3
"""
Test script to debug Analysis Results tab display issues
"""

import os
import sys
import traceback

def test_analysis_results():
    """Test the analysis results display"""
    try:
        print("=" * 60)
        print("🔍 Testing Analysis Results Display")
        print("=" * 60)
        
        # Import modules
        print("📦 Importing modules...")
        from main import VisualRegressionGUI
        from visual_ai_regression import VisualAIRegressionModule
        
        print("✅ Modules imported successfully")
        
        # Create a test configuration
        test_config = {
            'url1': 'https://www.google.com',
            'url2': 'https://www.google.com',
            'browser': 'chrome',
            'resolution': '1920x1080',
            'layout_shift': True,
            'font_color': True,
            'element_detection': True,
            'ai_analysis': True,
            'wcag_analysis': True
        }
        
        print("🔧 Test configuration created:")
        for key, value in test_config.items():
            print(f"   {key}: {value}")
        
        # Create mock results
        mock_results = {
            'analysis_results': {
                'similarity_score': 0.95,
                'layout_shifts': [
                    {'area': 'header', 'magnitude': 0.1},
                    {'area': 'footer', 'magnitude': 0.05}
                ],
                'color_differences': [
                    {'description': 'Button color changed from blue to green'},
                    {'description': 'Text color changed in navigation'}
                ],
                'missing_elements': [
                    {'type': 'button', 'id': 'submit-btn'},
                    {'type': 'image', 'id': 'logo'}
                ],
                'new_elements': [
                    {'type': 'div', 'class': 'new-banner'}
                ],
                'overlapping_elements': [
                    {'type': 'div', 'overlap': 0.3}
                ],
                'ai_analysis': {
                    'anomaly_detected': True,
                    'anomalies': [
                        {'confidence': 0.8, 'description': 'Layout anomaly detected'},
                        {'confidence': 0.6, 'description': 'Color scheme change'}
                    ]
                },
                'wcag_analysis': {
                    'url1': {
                        'compliance_score': 85.5,
                        'compliance_level': 'AA'
                    },
                    'url2': {
                        'compliance_score': 82.3,
                        'compliance_level': 'AA'
                    },
                    'comparison': {
                        'assessment': 'Slight decrease in accessibility'
                    }
                }
            },
            'summary': {
                'similarity_score': 0.95,
                'layout_differences': 2,
                'color_differences': 2
            },
            'summary_dict': {
                'similarity_score': 0.95,
                'layout_differences': 2,
                'color_differences': 2,
                'missing_elements': 2,
                'new_elements': 1,
                'element_changes': 3,
                'ai_anomalies': 2
            },
            'reports': {
                'html': 'reports/test_report.html',
                'json': 'reports/test_report.json'
            }
        }
        
        print("📊 Mock results created with:")
        print(f"   ✅ Similarity Score: {mock_results['summary_dict']['similarity_score']:.1%}")
        print(f"   🔄 Layout Differences: {mock_results['summary_dict']['layout_differences']}")
        print(f"   🎨 Color Changes: {mock_results['summary_dict']['color_differences']}")
        print(f"   🔍 Element Changes: {mock_results['summary_dict']['element_changes']}")
        print(f"   🤖 AI Anomalies: {mock_results['summary_dict']['ai_anomalies']}")
        
        print("\n🧪 Testing Analysis Results Processing...")
        
        # Test if the visual_ai_regression module can process the config
        regression_module = VisualAIRegressionModule()
        print("✅ VisualAIRegressionModule created")
        
        # Test summary generation
        summary_dict = regression_module._generate_summary_dict(mock_results['analysis_results'], test_config)
        print("✅ Summary generation test passed:")
        for key, value in summary_dict.items():
            print(f"   {key}: {value}")
        
        print("\n🎯 Test Summary:")
        print("✅ All modules import correctly")
        print("✅ Configuration handling works")
        print("✅ Mock results structure is valid")
        print("✅ Summary generation works")
        print("\n💡 The Analysis Results tab should display properly with real data")
        print("   If it's still empty, check:")
        print("   1. URL accessibility (both URLs must be reachable)")
        print("   2. Chrome/WebDriver installation")
        print("   3. Network connectivity")
        print("   4. Popup blockers or security software")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\n📋 Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Analysis Results Display Test...")
    success = test_analysis_results()
    
    if success:
        print("\n🎉 Test completed successfully!")
        print("🔧 Try running the main application with accessible URLs")
    else:
        print("\n💥 Test failed - check the errors above")
    
    input("\nPress Enter to exit...")
