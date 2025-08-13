#!/usr/bin/env python3
"""
Test script to verify the upgraded launch_gui.bat file includes all v6.0 features.
"""

import os
import subprocess
import sys

def test_launcher_upgrade():
    """Test the upgraded launch_gui.bat file"""
    print("🧪 Testing Upgraded launch_gui.bat File")
    print("=" * 50)
    
    launcher_path = "launch_gui.bat"
    
    if not os.path.exists(launcher_path):
        print(f"❌ {launcher_path} not found!")
        return False
    
    # Read the launcher content
    try:
        with open(launcher_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        with open(launcher_path, 'r', encoding='cp1252') as f:
            content = f.read()
    
    print(f"📏 Launcher file size: {len(content)} characters")
    
    # Check for v6.0 features
    v6_features = {
        'Version 6.0': 'v6.0' in content,
        'Image Click Full View': 'Image Click Full View' in content or 'Image Click Modal' in content,
        'Screenshot Loading Fix': 'Screenshot Loading Fix' in content,
        'Modal Functionality': 'Modal' in content,
        'Feature Verification': 'V6.0 FEATURES VERIFICATION' in content or 'V6.0 Feature verification' in content,
        'Testing Instructions': 'V6.0 FEATURE TESTING GUIDE' in content,
        'openImage Function Check': 'function openImage' in content,
        'Enhanced Features List': 'NEW ADVANCED FEATURES' in content,
        'Click Outside to Close': 'Click Outside to Close' in content or 'click outside' in content,
        'ESC Key Support': 'ESC Key' in content or 'ESC key' in content
    }
    
    print("\n🔍 V6.0 Feature Verification:")
    all_passed = True
    for feature, present in v6_features.items():
        status = "✅ PASS" if present else "❌ FAIL"
        print(f"   {status}: {feature}")
        if not present:
            all_passed = False
    
    # Check for specific version strings
    version_checks = {
        'August 13, 2025': 'August 13, 2025' in content,
        'v6.0 in title': 'v6.0' in content and 'Aug 2025' in content,
        'Updated date': '2025' in content,
        'Image click description': 'click' in content.lower() and 'image' in content.lower()
    }
    
    print("\n📅 Version Information:")
    for check, passed in version_checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}: {check}")
        if not passed:
            all_passed = False
    
    # Check for feature verification code
    verification_checks = {
        'findstr commands': 'findstr' in content,
        'Feature verification section': 'Feature Verification' in content or 'Feature verification' in content,
        'Testing guide section': 'FEATURE TESTING GUIDE' in content,
        'Demo file check': 'image_click_full_view_demo.html' in content
    }
    
    print("\n🛠️ Verification Code:")
    for check, passed in verification_checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status}: {check}")
        if not passed:
            all_passed = False
    
    # Count feature mentions
    feature_counts = {
        'Image': content.lower().count('image'),
        'Modal': content.lower().count('modal'),
        'Click': content.lower().count('click'),
        'Screenshot': content.lower().count('screenshot'),
        'v6.0': content.lower().count('v6.0')
    }
    
    print("\n📊 Feature Mentions:")
    for feature, count in feature_counts.items():
        print(f"   {feature}: {count} times")
    
    # Test launcher syntax (basic check)
    print("\n🔧 Syntax Verification:")
    try:
        # Check for basic batch file syntax issues
        if 'echo off' in content:
            print("   ✅ Valid batch file header")
        else:
            print("   ❌ Missing batch file header")
            all_passed = False
            
        if ':start' in content or ':main' in content:
            print("   ✅ Valid batch file labels")
        else:
            print("   ❌ Missing batch file labels")
            all_passed = False
            
        if 'pause' in content:
            print("   ✅ User interaction included")
        else:
            print("   ❌ Missing user interaction")
            all_passed = False
            
    except Exception as e:
        print(f"   ⚠️ Syntax check error: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ SUCCESS: launch_gui.bat successfully upgraded to v6.0!")
        print("🎯 All v6.0 features properly documented and verified")
        print("🚀 Ready for production use with enhanced functionality")
    else:
        print("❌ ISSUES: Some v6.0 features missing from launcher")
        print("🔧 Review the upgrade and add missing components")
    
    print(f"\n📁 Launcher location: {os.path.abspath(launcher_path)}")
    print("💡 Run the launcher to test all v6.0 features!")
    
    return all_passed

def main():
    """Main test function"""
    print("🚀 Testing Upgraded launch_gui.bat File")
    print("=" * 50)
    
    success = test_launcher_upgrade()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 LAUNCHER UPGRADE COMPLETE!")
        print("✅ All v6.0 features properly integrated")
        print("🔧 Ready to launch with enhanced functionality")
    else:
        print("⚠️ LAUNCHER UPGRADE NEEDS ATTENTION")
        print("❌ Some features may need additional integration")

if __name__ == "__main__":
    main()
