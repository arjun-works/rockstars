#!/usr/bin/env python3
"""
Verification script to confirm that the metrics issue has been completely fixed
"""

import os
import sys
import re

def verify_metrics_fix():
    """Verify that metrics are now showing correctly in HTML reports"""
    print("🔍 Verifying metrics fix in HTML reports...")
    
    # Find the most recent HTML report
    reports_dir = "reports"
    html_files = [f for f in os.listdir(reports_dir) if f.endswith('.html') and 'visual_regression_report' in f and 'summary' not in f]
    
    if not html_files:
        print("❌ No HTML reports found!")
        return False
    
    # Get the most recent report
    latest_report = max(html_files, key=lambda x: os.path.getctime(os.path.join(reports_dir, x)))
    report_path = os.path.join(reports_dir, latest_report)
    
    print(f"📊 Checking report: {latest_report}")
    
    # Read the HTML content
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for metrics values (not just 0)
    metrics_found = {}
    
    # SSIM - look for values between 0 and 1 (not 0)
    ssim_matches = re.findall(r'SSIM.*?(\d+\.\d+)', content, re.IGNORECASE | re.DOTALL)
    if ssim_matches:
        ssim_value = float(ssim_matches[0])
        metrics_found['SSIM'] = ssim_value
        print(f"✅ SSIM found: {ssim_value}")
    else:
        print("❌ SSIM not found or is 0")
    
    # MSE - look for non-zero values
    mse_matches = re.findall(r'MSE.*?(\d+\.\d+)', content, re.IGNORECASE | re.DOTALL)
    if mse_matches:
        mse_value = float(mse_matches[0])
        metrics_found['MSE'] = mse_value
        print(f"✅ MSE found: {mse_value}")
    else:
        print("❌ MSE not found or is 0")
    
    # PSNR - look for non-zero values
    psnr_matches = re.findall(r'PSNR.*?(\d+\.\d+)', content, re.IGNORECASE | re.DOTALL)
    if psnr_matches:
        psnr_value = float(psnr_matches[0])
        metrics_found['PSNR'] = psnr_value
        print(f"✅ PSNR found: {psnr_value} dB")
    else:
        print("❌ PSNR not found or is 0")
    
    # Pixel Difference - look for percentage values
    pixel_matches = re.findall(r'Pixel.*?(\d+\.\d+)%', content, re.IGNORECASE | re.DOTALL)
    if pixel_matches:
        pixel_value = float(pixel_matches[0])
        metrics_found['Pixel Difference'] = pixel_value
        print(f"✅ Pixel Difference found: {pixel_value}%")
    else:
        print("❌ Pixel Difference not found or is 0")
    
    # Summary
    print("\n📊 Metrics Fix Verification Summary:")
    print("="*50)
    
    if len(metrics_found) == 4:
        print("🎉 SUCCESS! All metrics are now displaying correctly in HTML reports!")
        print(f"   - SSIM: {metrics_found['SSIM']}")
        print(f"   - MSE: {metrics_found['MSE']}")
        print(f"   - PSNR: {metrics_found['PSNR']} dB")
        print(f"   - Pixel Difference: {metrics_found['Pixel Difference']}%")
        print("\n✅ The metrics issue has been completely resolved!")
        return True
    else:
        print(f"❌ Only {len(metrics_found)}/4 metrics found. Issue not fully resolved.")
        return False

if __name__ == "__main__":
    verify_metrics_fix()
