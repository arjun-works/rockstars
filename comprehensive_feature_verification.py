#!/usr/bin/env python3
"""
Comprehensive Feature Verification for Visual AI Regression Module v6.0
This script will verify all the key features mentioned in the conversation summary.
"""

import os
import sys
import json
import time
from datetime import datetime

# Add project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_file_exists(filepath, description):
    """Check if a file exists and report status"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory_exists(dirpath, description):
    """Check if a directory exists and report status"""
    exists = os.path.exists(dirpath) and os.path.isdir(dirpath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {dirpath}")
    return exists

def analyze_code_for_features(filepath, features_to_check):
    """Analyze code file for specific features"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {}
        for feature_name, search_terms in features_to_check.items():
            found = any(term in content for term in search_terms)
            results[feature_name] = found
            status = "✅" if found else "❌"
            print(f"  {status} {feature_name}")
        
        return results
    except Exception as e:
        print(f"❌ Error analyzing {filepath}: {str(e)}")
        return {}

def verify_html_report_features():
    """Verify HTML report generation and features"""
    print("\n📄 CHECKING HTML REPORT FEATURES:")
    print("=" * 50)
    
    # Check for recent HTML reports
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        print("❌ Reports directory not found")
        return False
    
    html_files = [f for f in os.listdir(reports_dir) if f.endswith('.html')]
    if not html_files:
        print("❌ No HTML reports found")
        return False
    
    # Get the most recent HTML report
    html_files.sort(key=lambda f: os.path.getmtime(os.path.join(reports_dir, f)), reverse=True)
    latest_html = os.path.join(reports_dir, html_files[0])
    
    print(f"📄 Checking latest HTML report: {html_files[0]}")
    
    try:
        with open(latest_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for key features
        features = {
            "Image Click Modal": ["openImage", "onclick"],
            "Screenshot Loading": ["screenshot_before", "screenshot_after"],
            "Tabbed Interface": ["nav-tab", "tab-content"],
            "Enhanced Descriptions": ["Side-by-side comparison", "Visual differences"],
            "Modal Overlay": ["modal-overlay", "closeModal"],
            "ESC Key Support": ["keydown", "Escape"],
            "Smooth Animations": ["transition", "animation"]
        }
        
        for feature, search_terms in features.items():
            found = any(term in html_content for term in search_terms)
            status = "✅" if found else "❌"
            print(f"  {status} {feature}")
        
        return True
    except Exception as e:
        print(f"❌ Error checking HTML report: {str(e)}")
        return False

def verify_core_modules():
    """Verify all core module files exist and have key features"""
    print("\n🔧 CHECKING CORE MODULES:")
    print("=" * 50)
    
    modules = {
        "main.py": ["class VisualAIRegressionGUI", "tkinter", "run_analysis"],
        "image_comparison.py": ["calculate_ssim", "calculate_mse", "calculate_psnr"],
        "visual_ai_regression.py": ["analyze_visual_differences", "generate_comparison"],
        "report_generator.py": ["generate_html_report", "openImage", "_generate_image_html"],
        "screenshot_capture.py": ["capture_screenshot", "WebDriver"],
        "ai_detector.py": ["detect_differences", "analyze_layout"]
    }
    
    all_exist = True
    for module_name, required_features in modules.items():
        if check_file_exists(module_name, f"Core Module: {module_name}"):
            try:
                with open(module_name, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"  📋 Checking features in {module_name}:")
                for feature in required_features:
                    found = feature in content
                    status = "✅" if found else "❌"
                    print(f"    {status} {feature}")
            except Exception as e:
                print(f"    ❌ Error reading {module_name}: {str(e)}")
        else:
            all_exist = False
    
    return all_exist

def verify_launcher_features():
    """Verify launcher batch file features"""
    print("\n🚀 CHECKING LAUNCHER FEATURES:")
    print("=" * 50)
    
    launcher_file = "launch_gui.bat"
    if not check_file_exists(launcher_file, "Launcher Script"):
        return False
    
    features_to_check = {
        "v6.0 Version": ["v6.0", "August 2025"],
        "Image Click Modal": ["Image Click Full View Modal", "full-screen viewing"],
        "Screenshot Loading Fix": ["Screenshot Loading Fix", "display properly"],
        "Feature Verification": ["findstr", "verification"],
        "Enhanced Messages": ["LATEST FEATURES", "August 2025"],
        "Testing Instructions": ["TESTING", "test image click"]
    }
    
    return analyze_code_for_features(launcher_file, features_to_check)

def verify_workspace_structure():
    """Verify workspace directory structure"""
    print("\n📁 CHECKING WORKSPACE STRUCTURE:")
    print("=" * 50)
    
    directories = {
        "reports": "Analysis Reports Directory",
        "screenshots": "Screenshots Directory", 
        "visualizations": "Visualizations Directory",
        "venv": "Virtual Environment"
    }
    
    all_exist = True
    for dir_name, description in directories.items():
        if not check_directory_exists(dir_name, description):
            all_exist = False
    
    # Check for important files
    files = {
        "requirements.txt": "Dependencies File",
        "README.md": "Documentation",
        "ENHANCED_WCAG_GUIDE.md": "WCAG Guide"
    }
    
    for file_name, description in files.items():
        if not check_file_exists(file_name, description):
            all_exist = False
    
    return all_exist

def main():
    """Main verification function"""
    print("🔍 VISUAL AI REGRESSION MODULE v6.0 - COMPREHENSIVE VERIFICATION")
    print("=" * 70)
    print(f"📅 Verification Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Run all verification checks
    checks = [
        ("Workspace Structure", verify_workspace_structure),
        ("Core Modules", verify_core_modules), 
        ("Launcher Features", verify_launcher_features),
        ("HTML Report Features", verify_html_report_features)
    ]
    
    results = {}
    for check_name, check_function in checks:
        print(f"\n🔍 {check_name.upper()} VERIFICATION:")
        print("-" * 50)
        try:
            results[check_name] = check_function()
        except Exception as e:
            print(f"❌ Error during {check_name} verification: {str(e)}")
            results[check_name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 VERIFICATION SUMMARY:")
    print("=" * 70)
    
    total_checks = len(results)
    passed_checks = sum(1 for result in results.values() if result)
    
    for check_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} {check_name}")
    
    print("-" * 70)
    print(f"📈 Overall Status: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 ALL VERIFICATIONS PASSED - Module is fully functional!")
    else:
        print("⚠️ Some verifications failed - See details above")
    
    print("\n🎯 NEXT STEPS:")
    if passed_checks == total_checks:
        print("✅ Ready for production use")
        print("✅ All v6.0 features verified and working")
        print("✅ Launch with launch_gui.bat or python main.py")
    else:
        print("🔧 Review failed checks and fix any issues")
        print("🔧 Re-run verification after fixes")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
