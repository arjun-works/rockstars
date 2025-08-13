import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
from skimage.metrics import structural_similarity as ssim
from skimage.feature import local_binary_pattern
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy import ndimage
import logging

class ImageComparison:
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for image comparison"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def load_images(self, image1_path, image2_path):
        """Load and preprocess images for comparison"""
        try:
            # Load images using OpenCV
            img1 = cv2.imread(image1_path)
            img2 = cv2.imread(image2_path)
            
            if img1 is None:
                raise ValueError(f"Could not load image: {image1_path}")
            if img2 is None:
                raise ValueError(f"Could not load image: {image2_path}")
            
            # Convert BGR to RGB
            img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            
            self.logger.info(f"Loaded images: {img1_rgb.shape} vs {img2_rgb.shape}")
            
            return img1_rgb, img2_rgb
            
        except Exception as e:
            self.logger.error(f"Failed to load images: {str(e)}")
            raise
    
    def resize_images_to_match(self, img1, img2):
        """Resize images to have the same dimensions"""
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        
        # Use the smaller dimensions to avoid upscaling
        target_height = min(h1, h2)
        target_width = min(w1, w2)
        
        if h1 != target_height or w1 != target_width:
            img1 = cv2.resize(img1, (target_width, target_height), interpolation=cv2.INTER_AREA)
        
        if h2 != target_height or w2 != target_width:
            img2 = cv2.resize(img2, (target_width, target_height), interpolation=cv2.INTER_AREA)
        
        self.logger.info(f"Resized images to: {target_width}x{target_height}")
        return img1, img2
    
    def calculate_ssim(self, img1, img2):
        """Calculate Structural Similarity Index"""
        try:
            # Convert to grayscale
            gray1 = rgb2gray(img1)
            gray2 = rgb2gray(img2)
            
            # Calculate SSIM with proper data_range
            similarity_index, diff_image = ssim(gray1, gray2, full=True, data_range=1.0)
            
            # Convert difference image to proper format
            diff_image = (diff_image * 255).astype(np.uint8)
            
            self.logger.info(f"SSIM calculated: {similarity_index:.4f}")
            
            return similarity_index, diff_image
            
        except Exception as e:
            self.logger.error(f"Failed to calculate SSIM: {str(e)}")
            raise
    
    def calculate_mse(self, img1, img2):
        """Calculate Mean Squared Error between two images"""
        try:
            # Convert to grayscale for MSE calculation
            gray1 = rgb2gray(img1)
            gray2 = rgb2gray(img2)
            
            # Calculate MSE
            mse = np.mean((gray1 - gray2) ** 2)
            
            self.logger.info(f"MSE calculated: {mse:.6f}")
            return mse
            
        except Exception as e:
            self.logger.error(f"Failed to calculate MSE: {str(e)}")
            raise
    
    def calculate_pixel_difference(self, img1, img2):
        """Calculate pixel-wise differences between two images"""
        try:
            # Calculate absolute difference
            diff = cv2.absdiff(img1, img2)
            
            # Calculate different metrics
            total_pixels = img1.shape[0] * img1.shape[1]
            
            # Count pixels with any difference
            diff_gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            different_pixels = np.count_nonzero(diff_gray > 5)  # threshold of 5 for noise tolerance
            pixel_difference_percentage = (different_pixels / total_pixels) * 100
            
            # Calculate average difference per pixel
            avg_pixel_difference = np.mean(diff_gray)
            
            # Calculate maximum difference
            max_pixel_difference = np.max(diff_gray)
            
            pixel_metrics = {
                'total_pixels': total_pixels,
                'different_pixels': different_pixels,
                'pixel_difference_percentage': pixel_difference_percentage,
                'avg_pixel_difference': avg_pixel_difference,
                'max_pixel_difference': max_pixel_difference
            }
            
            self.logger.info(f"Pixel differences: {different_pixels}/{total_pixels} ({pixel_difference_percentage:.2f}%)")
            return pixel_metrics
            
        except Exception as e:
            self.logger.error(f"Failed to calculate pixel differences: {str(e)}")
            raise
    
    def detect_layout_shifts(self, img1, img2, threshold=30):
        """Detect layout shifts between two images"""
        try:
            # Convert to grayscale
            gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
            
            # Apply edge detection
            edges1 = cv2.Canny(gray1, 50, 150)
            edges2 = cv2.Canny(gray2, 50, 150)
            
            # Find contours
            contours1, _ = cv2.findContours(edges1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours2, _ = cv2.findContours(edges2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter significant contours
            significant_contours1 = [c for c in contours1 if cv2.contourArea(c) > 100]
            significant_contours2 = [c for c in contours2 if cv2.contourArea(c) > 100]
            
            # Compare contour positions
            layout_shifts = []
            
            for i, contour1 in enumerate(significant_contours1):
                rect1 = cv2.boundingRect(contour1)
                best_match_distance = float('inf')
                best_match_rect = None
                
                for contour2 in significant_contours2:
                    rect2 = cv2.boundingRect(contour2)
                    
                    # Calculate center distance
                    center1 = (rect1[0] + rect1[2]//2, rect1[1] + rect1[3]//2)
                    center2 = (rect2[0] + rect2[2]//2, rect2[1] + rect2[3]//2)
                    distance = np.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
                    
                    if distance < best_match_distance and abs(rect1[2] - rect2[2]) < 50 and abs(rect1[3] - rect2[3]) < 50:
                        best_match_distance = distance
                        best_match_rect = rect2
                
                # If significant movement detected
                if best_match_distance > threshold:
                    shift_info = {
                        'original_position': rect1,
                        'new_position': best_match_rect,
                        'distance': best_match_distance,
                        'shift_x': (best_match_rect[0] - rect1[0]) if best_match_rect else 0,
                        'shift_y': (best_match_rect[1] - rect1[1]) if best_match_rect else 0
                    }
                    layout_shifts.append(shift_info)
            
            self.logger.info(f"Detected {len(layout_shifts)} layout shifts")
            return layout_shifts
            
        except Exception as e:
            self.logger.error(f"Failed to detect layout shifts: {str(e)}")
            raise
    
    def detect_color_differences(self, img1, img2, threshold=20):
        """Detect color and font differences"""
        try:
            # Calculate absolute difference
            diff = cv2.absdiff(img1, img2)
            
            # Create mask for significant differences
            diff_gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            _, mask = cv2.threshold(diff_gray, threshold, 255, cv2.THRESH_BINARY)
            
            # Find contours of different regions
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            color_differences = []
            for contour in contours:
                if cv2.contourArea(contour) > 50:  # Filter small differences
                    rect = cv2.boundingRect(contour)
                    
                    # Extract regions from both images
                    region1 = img1[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
                    region2 = img2[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
                    
                    # Calculate average colors
                    avg_color1 = np.mean(region1.reshape(-1, 3), axis=0)
                    avg_color2 = np.mean(region2.reshape(-1, 3), axis=0)
                    
                    color_diff = {
                        'position': rect,
                        'color1': avg_color1.tolist(),
                        'color2': avg_color2.tolist(),
                        'color_distance': np.linalg.norm(avg_color1 - avg_color2),
                        'area': cv2.contourArea(contour)
                    }
                    color_differences.append(color_diff)
            
            # Sort by significance (color distance * area)
            color_differences.sort(key=lambda x: x['color_distance'] * x['area'], reverse=True)
            
            self.logger.info(f"Detected {len(color_differences)} color differences")
            return color_differences, diff
            
        except Exception as e:
            self.logger.error(f"Failed to detect color differences: {str(e)}")
            raise
    
    def detect_missing_elements(self, img1, img2):
        """Detect missing or new elements between images"""
        try:
            # Convert to grayscale
            gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blur1 = cv2.GaussianBlur(gray1, (5, 5), 0)
            blur2 = cv2.GaussianBlur(gray2, (5, 5), 0)
            
            # Calculate absolute difference
            diff = cv2.absdiff(blur1, blur2)
            
            # Apply threshold to get binary image
            _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            
            # Morphological operations to clean up
            kernel = np.ones((3, 3), np.uint8)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            missing_elements = []
            new_elements = []
            
            for contour in contours:
                if cv2.contourArea(contour) > 100:  # Filter small changes
                    rect = cv2.boundingRect(contour)
                    
                    # Check if element exists in original image
                    region1 = gray1[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
                    region2 = gray2[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
                    
                    avg_intensity1 = np.mean(region1)
                    avg_intensity2 = np.mean(region2)
                    
                    element_info = {
                        'position': rect,
                        'area': cv2.contourArea(contour),
                        'avg_intensity1': avg_intensity1,
                        'avg_intensity2': avg_intensity2
                    }
                    
                    # Classify as missing or new based on intensity difference
                    if avg_intensity1 > avg_intensity2 + 30:
                        missing_elements.append(element_info)
                    elif avg_intensity2 > avg_intensity1 + 30:
                        new_elements.append(element_info)
            
            self.logger.info(f"Detected {len(missing_elements)} missing and {len(new_elements)} new elements")
            return missing_elements, new_elements, thresh
            
        except Exception as e:
            self.logger.error(f"Failed to detect missing elements: {str(e)}")
            raise
    
    def detect_overlapping_elements(self, img1, img2):
        """Detect overlapping or misaligned elements"""
        try:
            # Use template matching for detecting overlaps
            gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
            
            # Detect features using ORB
            orb = cv2.ORB_create(nfeatures=1000)
            
            kp1, des1 = orb.detectAndCompute(gray1, None)
            kp2, des2 = orb.detectAndCompute(gray2, None)
            
            overlapping_elements = []
            
            if des1 is not None and des2 is not None:
                # Match features
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(des1, des2)
                matches = sorted(matches, key=lambda x: x.distance)
                
                # Analyze matches for overlaps
                for match in matches[:50]:  # Top 50 matches
                    pt1 = kp1[match.queryIdx].pt
                    pt2 = kp2[match.trainIdx].pt
                    
                    distance = np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
                    
                    if distance > 10:  # Significant movement
                        overlap_info = {
                            'point1': pt1,
                            'point2': pt2,
                            'distance': distance,
                            'match_quality': match.distance
                        }
                        overlapping_elements.append(overlap_info)
            
            self.logger.info(f"Detected {len(overlapping_elements)} potential overlapping elements")
            return overlapping_elements
            
        except Exception as e:
            self.logger.error(f"Failed to detect overlapping elements: {str(e)}")
            raise
    
    def create_difference_heatmap(self, img1, img2, output_path):
        """Create a heatmap showing differences between images"""
        try:
            # Calculate difference
            diff = cv2.absdiff(img1, img2)
            diff_gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            
            # Apply colormap
            heatmap = cv2.applyColorMap(diff_gray, cv2.COLORMAP_JET)
            
            # Blend with original image
            blended = cv2.addWeighted(img1, 0.7, heatmap, 0.3, 0)
            
            # Save heatmap
            cv2.imwrite(output_path, cv2.cvtColor(blended, cv2.COLOR_RGB2BGR))
            
            self.logger.info(f"Difference heatmap saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create difference heatmap: {str(e)}")
            raise
    
    def create_annotated_comparison(self, img1, img2, differences, output_path):
        """Create annotated comparison image highlighting differences"""
        try:
            # Create side-by-side comparison
            height = max(img1.shape[0], img2.shape[0])
            width = img1.shape[1] + img2.shape[1] + 20  # 20px gap
            
            comparison = np.ones((height, width, 3), dtype=np.uint8) * 255
            
            # Place images
            comparison[:img1.shape[0], :img1.shape[1]] = img1
            comparison[:img2.shape[0], img1.shape[1]+20:] = img2
            
            # Convert to PIL for annotation
            pil_image = Image.fromarray(comparison)
            draw = ImageDraw.Draw(pil_image)
            
            # Try to load a font
            try:
                font = ImageFont.truetype("arial.ttf", 16)
            except:
                font = ImageFont.load_default()
            
            # Annotate differences
            colors = ['red', 'blue', 'green', 'orange', 'purple']
            
            for i, diff in enumerate(differences[:10]):  # Limit to top 10 differences
                color = colors[i % len(colors)]
                
                if 'position' in diff:
                    x, y, w, h = diff['position']
                    
                    # Draw rectangle on first image
                    draw.rectangle([x, y, x+w, y+h], outline=color, width=3)
                    
                    # Draw rectangle on second image
                    draw.rectangle([x+img1.shape[1]+20, y, x+w+img1.shape[1]+20, y+h], outline=color, width=3)
                    
                    # Add label
                    draw.text((x, y-20), f"Diff {i+1}", fill=color, font=font)
            
            # Save annotated image
            pil_image.save(output_path)
            
            self.logger.info(f"Annotated comparison saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to create annotated comparison: {str(e)}")
            raise
    
    def calculate_comprehensive_metrics(self, img1, img2):
        """Calculate comprehensive comparison metrics including SSIM, MSE, and Pixel Differences"""
        try:
            results = {}
            
            # Calculate SSIM
            ssim_score, diff_image = self.calculate_ssim(img1, img2)
            results['ssim'] = ssim_score
            results['ssim_diff_image'] = diff_image
            
            # Calculate MSE
            mse = self.calculate_mse(img1, img2)
            results['mse'] = mse
            
            # Calculate Pixel Differences
            pixel_metrics = self.calculate_pixel_difference(img1, img2)
            results['pixel_metrics'] = pixel_metrics
            
            # Calculate additional metrics
            # Peak Signal-to-Noise Ratio (PSNR)
            if mse > 0:
                psnr = 20 * np.log10(1.0 / np.sqrt(mse))  # Assuming normalized images (0-1 range)
            else:
                psnr = float('inf')  # Perfect match
            results['psnr'] = psnr
            
            # Overall similarity percentage (inverse of differences)
            overall_similarity = (1 - pixel_metrics['pixel_difference_percentage'] / 100) * 100
            results['overall_similarity_percentage'] = max(0, overall_similarity)
            
            self.logger.info(f"Comprehensive metrics calculated - SSIM: {ssim_score:.4f}, MSE: {mse:.6f}, PSNR: {psnr:.2f}, Pixel Diff: {pixel_metrics['pixel_difference_percentage']:.2f}%")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to calculate comprehensive metrics: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    comparator = ImageComparison()
    
    # Example comparison
    try:
        img1, img2 = comparator.load_images("screenshot1.png", "screenshot2.png")
        img1, img2 = comparator.resize_images_to_match(img1, img2)
        
        # Calculate SSIM
        ssim_score, diff_image = comparator.calculate_ssim(img1, img2)
        print(f"SSIM Score: {ssim_score}")
        
        # Detect differences
        layout_shifts = comparator.detect_layout_shifts(img1, img2)
        color_diffs, color_diff_img = comparator.detect_color_differences(img1, img2)
        missing_elements, new_elements, elements_diff = comparator.detect_missing_elements(img1, img2)
        
        print(f"Layout shifts: {len(layout_shifts)}")
        print(f"Color differences: {len(color_diffs)}")
        print(f"Missing elements: {len(missing_elements)}")
        print(f"New elements: {len(new_elements)}")
        
    except Exception as e:
        print(f"Error: {e}")
