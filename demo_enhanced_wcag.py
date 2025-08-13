"""
Enhanced WCAG Compliance Testing Demo
=====================================

This script demonstrates the enhanced WCAG 2.1/2.2 compliance testing features
including advanced color analysis and WCAG 2.2 specific checks.
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wcag_checker import WCAGCompliantChecker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def setup_driver():
    """Setup Chrome WebDriver with accessibility-focused options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Enable accessibility features
    chrome_options.add_argument("--force-renderer-accessibility")
    chrome_options.add_argument("--enable-features=VaapiVideoDecoder")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def demo_wcag_analysis():
    """Demonstrate enhanced WCAG analysis features"""
    print("🚀 Enhanced WCAG Compliance Testing Demo")
    print("=" * 50)
    
    # Initialize WCAG checker
    checker = WCAGCompliantChecker()
    driver = None
    
    try:
        # Setup WebDriver
        print("🔧 Setting up WebDriver...")
        driver = setup_driver()
        
        # Test URLs (you can modify these)
        test_urls = [
            "https://www.w3.org/WAI/WCAG21/Understanding/",  # Good accessibility
            "https://example.com"  # Basic example
        ]
        
        for i, url in enumerate(test_urls, 1):
            print(f"\n📊 Testing URL {i}: {url}")
            print("-" * 40)
            
            def progress_callback(message):
                print(f"   {message}")
            
            try:
                # Run enhanced WCAG analysis
                results = checker.check_wcag_compliance(driver, url, progress_callback)
                
                # Display results
                print(f"\n✅ Analysis Complete!")
                print(f"   WCAG Version: {results.get('wcag_version', '2.1')}")
                print(f"   Compliance Score: {checker.compliance_score}%")
                print(f"   Compliance Level: {results.get('compliance_level', 'Unknown')}")
                print(f"   Total Issues: {results.get('total_issues', 0)}")
                print(f"   Critical Issues: {results.get('critical_issues', 0)}")
                
                # WCAG 2.2 Features
                wcag_22 = results.get('wcag_22_features', {})
                print(f"\n🆕 WCAG 2.2 Features:")
                print(f"   Target Size Compliant: {'✅' if wcag_22.get('target_size_compliant', False) else '❌'}")
                print(f"   Focus Appearance Score: {wcag_22.get('focus_appearance_score', 0)}%")
                print(f"   Dragging Alternative Score: {wcag_22.get('dragging_alternative_score', 0)}%")
                
                # Category Breakdown
                print(f"\n📋 Category Scores:")
                categories = results.get('categories', {})
                for category, data in categories.items():
                    score = data.get('score', 0)
                    issue_count = len(data.get('issues', []))
                    print(f"   {category.title()}: {score}% ({issue_count} issues)")
                
                # Top Issues
                all_issues = []
                for category_data in categories.values():
                    all_issues.extend(category_data.get('issues', []))
                
                if all_issues:
                    print(f"\n⚠️  Top Issues:")
                    critical_issues = [issue for issue in all_issues if issue.get('impact') == 'critical']
                    for issue in critical_issues[:3]:  # Show top 3 critical issues
                        print(f"   • {issue.get('description', 'Unknown issue')} (WCAG {issue.get('guideline', 'Unknown')})")
                
                # Generate report
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_path = f"reports/enhanced_wcag_report_{timestamp}.json"
                
                # Ensure reports directory exists
                os.makedirs("reports", exist_ok=True)
                
                # Save detailed report
                checker.generate_wcag_report(report_path)
                print(f"\n📄 Detailed report saved: {report_path}")
                
            except Exception as e:
                print(f"❌ Error analyzing {url}: {str(e)}")
                continue
    
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
    
    finally:
        if driver:
            driver.quit()
            print("\n🔧 WebDriver closed")
    
    print("\n🎉 Enhanced WCAG Demo Complete!")
    print("\nKey Features Demonstrated:")
    print("• WCAG 2.2 compliance checking")
    print("• Enhanced color contrast analysis")
    print("• Target size validation")
    print("• Accessible authentication checks")
    print("• Color blindness simulation")
    print("• Comprehensive scoring system")


if __name__ == "__main__":
    demo_wcag_analysis()
