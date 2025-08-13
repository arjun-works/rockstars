#!/usr/bin/env python3
"""
Test script to verify SSIM, MSE, and Pixel Difference calculations
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from image_comparison import ImageComparison
import cv2
import numpy as np
from PIL import Image

def create_test_images():
    """Create two test images for comparison"""
    # Create a simple test image 1
    img1 = np.ones((200, 200, 3), dtype=np.uint8) * 255  # White image
    img1[50:150, 50:150] = [255, 0, 0]  # Red square in the middle
    
    # Create a slightly different test image 2
    img2 = np.ones((200, 200, 3), dtype=np.uint8) * 255  # White image
    img2[55:155, 55:155] = [255, 0, 0]  # Red square slightly shifted
    img2[100:120, 100:120] = [0, 255, 0]  # Green square overlay
    
    return img1, img2

def test_metrics():
    """Test the new metrics calculation"""
    print("🧪 Testing SSIM, MSE, and Pixel Difference calculations...")
    
    try:
        # Create test images
        img1, img2 = create_test_images()
        
        # Initialize image comparator
        comparator = ImageComparison()
        
        # Test individual metrics
        print("\n📊 Testing individual metrics:")
        
        # Test SSIM
        ssim_score, diff_image = comparator.calculate_ssim(img1, img2)
        print(f"✅ SSIM: {ssim_score:.6f}")
        
        # Test MSE
        mse = comparator.calculate_mse(img1, img2)
        print(f"✅ MSE: {mse:.6f}")
        
        # Test Pixel Differences
        pixel_metrics = comparator.calculate_pixel_difference(img1, img2)
        print(f"✅ Pixel Differences:")
        print(f"   • Total pixels: {pixel_metrics['total_pixels']:,}")
        print(f"   • Different pixels: {pixel_metrics['different_pixels']:,}")
        print(f"   • Percentage different: {pixel_metrics['pixel_difference_percentage']:.2f}%")
        print(f"   • Average difference: {pixel_metrics['avg_pixel_difference']:.2f}")
        print(f"   • Maximum difference: {pixel_metrics['max_pixel_difference']:.2f}")
        
        # Test comprehensive metrics
        print("\n📈 Testing comprehensive metrics:")
        comprehensive = comparator.calculate_comprehensive_metrics(img1, img2)
        print(f"✅ Comprehensive metrics:")
        print(f"   • SSIM: {comprehensive['ssim']:.6f}")
        print(f"   • MSE: {comprehensive['mse']:.6f}")
        print(f"   • PSNR: {comprehensive['psnr']:.2f} dB")
        print(f"   • Overall similarity: {comprehensive['overall_similarity_percentage']:.2f}%")
        
        # Verify non-zero values
        if ssim_score > 0 and mse > 0 and pixel_metrics['different_pixels'] > 0:
            print("\n✅ SUCCESS: All metrics are calculating properly and showing non-zero values!")
            print("🎉 The SSIM, MSE, and Pixel Difference issue has been fixed!")
            return True
        else:
            print("\n❌ WARNING: Some metrics are still showing zero values")
            print(f"   SSIM: {ssim_score}")
            print(f"   MSE: {mse}")
            print(f"   Different pixels: {pixel_metrics['different_pixels']}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_metrics()
    if success:
        print("\n🚀 The Visual AI Regression Module should now display SSIM, MSE, and Pixel Difference correctly!")
    else:
        print("\n⚠️ There may still be issues with the metrics calculation.")
