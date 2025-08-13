#!/usr/bin/env python3
"""
Quick Demo Test - Generate a fresh analysis with all v6.0 features
This will create a new analysis and immediately test the image click functionality
"""

import os
import sys
import webbrowser
import time
from datetime import datetime

# Add project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from visual_ai_regression import VisualAIRegression
    from report_generator import ReportGenerator
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all modules are available")
    sys.exit(1)

def create_demo_analysis():
    """Create a quick demo analysis"""
    print("🚀 GENERATING FRESH v6.0 DEMO ANALYSIS")
    print("=" * 50)
    
    # Create analyzer instance
    analyzer = VisualAIRegression()
    
    # Use existing screenshots if available
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        print("❌ Screenshots directory not found")
        return None
    
    screenshot_files = [f for f in os.listdir(screenshots_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if len(screenshot_files) < 2:
        print("❌ Need at least 2 screenshots for comparison")
        return None
    
    # Use first two screenshots for demo
    before_img = os.path.join(screenshots_dir, screenshot_files[0])
    after_img = os.path.join(screenshots_dir, screenshot_files[1])
    
    print(f"📷 Using screenshots:")
    print(f"   Before: {screenshot_files[0]}")
    print(f"   After: {screenshot_files[1]}")
    
    # Generate analysis
    try:
        print("🔍 Running analysis...")
        analysis_results = analyzer.analyze_images(before_img, after_img)
        
        if analysis_results:
            print("✅ Analysis completed successfully")
            
            # Generate HTML report with all v6.0 features
            print("📄 Generating HTML report with v6.0 features...")
            report_generator = ReportGenerator()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"demo_v6_report_{timestamp}.html"
            report_path = os.path.join("reports", report_filename)
            
            # Ensure reports directory exists
            os.makedirs("reports", exist_ok=True)
            
            # Generate the report
            config = {"analysis_type": "demo", "timestamp": timestamp}
            report_generator.generate_enhanced_html_report(analysis_results, config, report_path)
            
            print(f"✅ HTML report generated: {report_filename}")
            return report_path
        else:
            print("❌ Analysis failed to generate results")
            return None
            
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return None

def test_html_report_features(report_path):
    """Test the generated HTML report features"""
    print("\n🔍 TESTING HTML REPORT v6.0 FEATURES")
    print("=" * 50)
    
    if not os.path.exists(report_path):
        print(f"❌ Report not found: {report_path}")
        return False
    
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Test for v6.0 features
        features_test = {
            "🖼️ Image Click Modal": "openImage" in html_content and "onclick" in html_content,
            "📷 Screenshot Display": "screenshot_before" in html_content and "screenshot_after" in html_content,
            "🎯 Tabbed Interface": "nav-tab" in html_content and "tab-content" in html_content,
            "✨ Enhanced Descriptions": "Side-by-side comparison" in html_content,
            "🚀 JavaScript Functions": "function openImage" in html_content,
            "📊 Metrics Display": any(metric in html_content for metric in ["SSIM", "MSE", "PSNR"]),
            "🎨 Professional Styling": "style>" in html_content and "background" in html_content
        }
        
        all_passed = True
        for feature, passed in features_test.items():
            status = "✅" if passed else "❌"
            print(f"{status} {feature}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n🎉 All v6.0 features detected in HTML report!")
        else:
            print("\n⚠️ Some v6.0 features missing in HTML report")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error testing HTML report: {str(e)}")
        return False

def open_demo_report(report_path):
    """Open the demo report in browser"""
    print("\n🌐 OPENING DEMO REPORT IN BROWSER")
    print("=" * 50)
    
    if os.path.exists(report_path):
        try:
            # Convert to absolute path for browser
            abs_path = os.path.abspath(report_path)
            webbrowser.open(f'file://{abs_path}')
            print(f"✅ Opened report in browser: {os.path.basename(report_path)}")
            print("\n🎯 TEST THE FOLLOWING v6.0 FEATURES:")
            print("   • Click any image to open full-screen modal")
            print("   • Press ESC to close modal")
            print("   • Click outside modal to close")
            print("   • Navigate between tabs")
            print("   • Check screenshot loading")
            return True
        except Exception as e:
            print(f"❌ Error opening browser: {str(e)}")
            return False
    else:
        print(f"❌ Report file not found: {report_path}")
        return False

def main():
    """Main demo function"""
    print("🚀 VISUAL AI REGRESSION MODULE v6.0 - QUICK DEMO")
    print("=" * 60)
    print(f"📅 Demo Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Step 1: Generate fresh analysis
    report_path = create_demo_analysis()
    if not report_path:
        print("❌ Failed to generate demo analysis")
        return
    
    # Step 2: Test HTML report features
    features_working = test_html_report_features(report_path)
    
    # Step 3: Open in browser for manual testing
    browser_opened = open_demo_report(report_path)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEMO SUMMARY:")
    print("=" * 60)
    
    if features_working and browser_opened:
        print("🎉 DEMO SUCCESSFUL!")
        print("✅ Fresh analysis generated")
        print("✅ All v6.0 features detected")
        print("✅ Report opened in browser")
        print("\n🎯 Now test the image click functionality manually!")
    else:
        print("⚠️ Demo partially successful")
        if not features_working:
            print("❌ Some v6.0 features missing")
        if not browser_opened:
            print("❌ Could not open browser")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
