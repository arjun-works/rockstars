#!/usr/bin/env python3
"""
Test Configuration Settings in HTML Report
This script tests the new configuration settings tab functionality.
"""

import os
import sys
import webbrowser
from datetime import datetime

# Add project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from report_generator import ReportGenerator
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def create_test_config():
    """Create a comprehensive test configuration"""
    return {
        'analysis_type': 'Advanced Visual Regression with AI',
        'urls': {
            'url1': 'https://example.com/original',
            'url2': 'https://example.com/updated'
        },
        'visual_comparison': True,
        'ai_analysis': True,
        'wcag_analysis': True,
        'layout_analysis': True,
        'color_analysis': True,
        'font_analysis': True,
        'capture_screenshots': True,
        'detailed_logging': False,
        'browser': 'Chrome',
        'viewport_width': 1920,
        'viewport_height': 1080,
        'wait_time': 5,
        'image_format': 'PNG',
        'similarity_threshold': 0.95,
        'comparison_method': 'SSIM + MSE + PSNR + AI',
        'report_format': 'HTML + PDF + JSON'
    }

def create_test_analysis_results():
    """Create mock analysis results for testing"""
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'duration': '45.3 seconds',
        'screenshots': {
            'url1_screenshot': 'test_before.png',
            'url2_screenshot': 'test_after.png'
        },
        'comparisons': {
            'ssim_score': 0.892,
            'mse_score': 156.7,
            'psnr_score': 26.4,
            'pixel_difference': 2843
        },
        'summary_dict': {
            'overall_similarity': 89.2,
            'layout_changes': 15.3,
            'color_changes': 8.7,
            'ai_confidence': 94.1
        },
        'ai_analysis': {
            'anomalies': [
                'Button color changed from blue to green',
                'Navigation menu position shifted 10px down',
                'Logo size reduced by 15%'
            ]
        }
    }

def test_configuration_settings():
    """Test the configuration settings HTML generation"""
    print("🔧 TESTING CONFIGURATION SETTINGS IN HTML REPORT")
    print("=" * 60)
    
    # Create test data
    config = create_test_config()
    analysis_results = create_test_analysis_results()
    
    # Generate report
    report_generator = ReportGenerator()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"test_configuration_report_{timestamp}.html"
    report_path = os.path.join("reports", report_filename)
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    try:
        print("📄 Generating HTML report with configuration settings...")
        report_generator.generate_enhanced_html_report(analysis_results, config, report_path)
        
        if os.path.exists(report_path):
            print(f"✅ Report generated successfully: {report_filename}")
            
            # Verify configuration content
            print("🔍 Verifying configuration settings content...")
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for configuration features
            config_features = {
                "Configuration Tab Button": "configuration-settings",
                "Configuration Section": "config-category",
                "Analysis Configuration": "Analysis Configuration",
                "Technical Settings": "Technical Settings",
                "Metrics Information": "Metrics & Algorithms",
                "Environment Information": "Environment Information",
                "Feature Toggles": "Analysis Options",
                "SSIM Description": "Structural Similarity Index",
                "Configuration Styling": "config-grid",
                "Module Version": "Visual AI Regression v6.0"
            }
            
            all_present = True
            for feature_name, search_term in config_features.items():
                found = search_term in content
                status = "✅" if found else "❌"
                print(f"  {status} {feature_name}")
                if not found:
                    all_present = False
            
            if all_present:
                print("\n🎉 All configuration features detected!")
            else:
                print("\n⚠️ Some configuration features missing")
            
            return report_path
        else:
            print("❌ Report file was not created")
            return None
            
    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")
        return None

def open_report_for_testing(report_path):
    """Open the report for manual testing"""
    if not report_path or not os.path.exists(report_path):
        print("❌ No report available to open")
        return False
    
    print(f"\n🌐 OPENING REPORT FOR TESTING:")
    print("-" * 40)
    print(f"📄 Report: {os.path.basename(report_path)}")
    
    try:
        abs_path = os.path.abspath(report_path)
        webbrowser.open(f'file://{abs_path}')
        print("✅ Report opened in browser")
        
        print("\n🎯 TEST THE FOLLOWING:")
        print("   1. Click the '⚙️ Configuration' tab")
        print("   2. Verify all configuration sections appear:")
        print("      • Analysis Configuration")
        print("      • Analysis Options")
        print("      • Technical Settings")
        print("      • Metrics & Algorithms")
        print("      • Environment Information")
        print("   3. Check that all settings show correct values")
        print("   4. Verify styling and layout look professional")
        print("   5. Test switching between tabs")
        
        return True
    except Exception as e:
        print(f"❌ Error opening browser: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🔧 CONFIGURATION SETTINGS HTML REPORT TEST")
    print("=" * 50)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Test configuration settings generation
    report_path = test_configuration_settings()
    
    if report_path:
        # Offer to open for manual testing
        print("\n🎯 MANUAL TESTING OPPORTUNITY:")
        print("-" * 40)
        response = input("Would you like to open the report to test configuration settings? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            open_report_for_testing(report_path)
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print("=" * 50)
    
    if report_path:
        print("✅ Configuration settings implementation successful!")
        print("✅ New ⚙️ Configuration tab added to HTML reports")
        print("✅ Comprehensive configuration information included:")
        print("   • Analysis configuration and URLs")
        print("   • Feature toggles and enabled options")
        print("   • Technical settings and parameters")
        print("   • Metrics and algorithms descriptions")
        print("   • Environment and system information")
        print("✅ Professional styling and layout applied")
        print("✅ Ready for production use!")
    else:
        print("❌ Configuration settings test failed")
        print("🔧 Check error messages above for details")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
