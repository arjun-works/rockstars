import numpy as np
import cv2
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
import logging
from scipy.spatial.distance import cdist
from skimage.feature import hog, local_binary_pattern
from skimage.segmentation import slic
from skimage.measure import regionprops
import pickle
import os

class AIDetector:
    def __init__(self):
        self.setup_logging()
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=50)
        
    def setup_logging(self):
        """Setup logging for AI detector"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def extract_features(self, image):
        """Extract comprehensive features from image for AI analysis"""
        try:
            features = []
            
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image.copy()
            
            # 1. HOG Features (Histogram of Oriented Gradients)
            hog_features = hog(gray, orientations=9, pixels_per_cell=(8, 8),
                              cells_per_block=(2, 2), block_norm='L2-Hys')
            features.extend(hog_features[:100])  # Limit to first 100 features
            
            # 2. LBP Features (Local Binary Pattern)
            radius = 3
            n_points = 8 * radius
            lbp = local_binary_pattern(gray, n_points, radius, method='uniform')
            lbp_hist, _ = np.histogram(lbp.ravel(), bins=n_points + 2, 
                                     range=(0, n_points + 2), density=True)
            features.extend(lbp_hist)
            
            # 3. Color histogram features
            if len(image.shape) == 3:
                for i in range(3):  # RGB channels
                    hist = cv2.calcHist([image], [i], None, [32], [0, 256])
                    features.extend(hist.flatten() / hist.sum())
            
            # 4. Edge density features
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            features.append(edge_density)
            
            # 5. Texture features using GLCM approximation
            texture_features = self._extract_texture_features(gray)
            features.extend(texture_features)
            
            # 6. Shape features using contours
            shape_features = self._extract_shape_features(gray)
            features.extend(shape_features)
            
            return np.array(features)
            
        except Exception as e:
            self.logger.error(f"Failed to extract features: {str(e)}")
            return np.array([])
    
    def _extract_texture_features(self, gray_image):
        """Extract texture features using statistical measures"""
        try:
            features = []
            
            # Calculate statistical measures
            features.append(np.mean(gray_image))
            features.append(np.std(gray_image))
            features.append(np.var(gray_image))
            
            # Calculate entropy
            hist, _ = np.histogram(gray_image, bins=256, range=(0, 256))
            hist = hist / hist.sum()
            entropy = -np.sum(hist * np.log2(hist + 1e-10))
            features.append(entropy)
            
            # Gradient magnitude
            grad_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            features.append(np.mean(gradient_magnitude))
            features.append(np.std(gradient_magnitude))
            
            return features
            
        except Exception as e:
            self.logger.error(f"Failed to extract texture features: {str(e)}")
            return [0] * 6
    
    def _extract_shape_features(self, gray_image):
        """Extract shape-based features"""
        try:
            features = []
            
            # Find contours
            contours, _ = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Number of contours
                features.append(len(contours))
                
                # Average contour area
                areas = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) > 10]
                features.append(np.mean(areas) if areas else 0)
                features.append(np.std(areas) if areas else 0)
                
                # Average perimeter
                perimeters = [cv2.arcLength(c, True) for c in contours if cv2.contourArea(c) > 10]
                features.append(np.mean(perimeters) if perimeters else 0)
                
                # Aspect ratios
                aspect_ratios = []
                for contour in contours:
                    if cv2.contourArea(contour) > 10:
                        rect = cv2.boundingRect(contour)
                        aspect_ratio = rect[2] / rect[3] if rect[3] > 0 else 0
                        aspect_ratios.append(aspect_ratio)
                
                features.append(np.mean(aspect_ratios) if aspect_ratios else 0)
                features.append(np.std(aspect_ratios) if aspect_ratios else 0)
            else:
                features.extend([0] * 6)
            
            return features
            
        except Exception as e:
            self.logger.error(f"Failed to extract shape features: {str(e)}")
            return [0] * 6
    
    def segment_image(self, image, n_segments=100):
        """Segment image using SLIC superpixels for region analysis"""
        try:
            # Apply SLIC segmentation
            segments = slic(image, n_segments=n_segments, compactness=10, sigma=1)
            
            # Extract properties of each segment
            segment_properties = []
            
            for region in regionprops(segments):
                # Skip small regions
                if region.area < 10:
                    continue
                
                # Extract region from original image
                min_row, min_col, max_row, max_col = region.bbox
                region_image = image[min_row:max_row, min_col:max_col]
                
                # Calculate region properties
                properties = {
                    'area': region.area,
                    'centroid': region.centroid,
                    'bbox': region.bbox,
                    'perimeter': region.perimeter,
                    'eccentricity': region.eccentricity,
                    'solidity': region.solidity,
                    'mean_color': np.mean(region_image.reshape(-1, region_image.shape[-1]), axis=0) if len(region_image.shape) == 3 else np.mean(region_image),
                    'std_color': np.std(region_image.reshape(-1, region_image.shape[-1]), axis=0) if len(region_image.shape) == 3 else np.std(region_image)
                }
                
                segment_properties.append(properties)
            
            self.logger.info(f"Segmented image into {len(segment_properties)} regions")
            return segments, segment_properties
            
        except Exception as e:
            self.logger.error(f"Failed to segment image: {str(e)}")
            return None, []
    
    def detect_anomalies_clustering(self, features1, features2, eps=0.5, min_samples=5):
        """Detect anomalies using clustering techniques"""
        try:
            # Combine features
            all_features = np.vstack([features1.reshape(1, -1), features2.reshape(1, -1)])
            
            # Normalize features
            normalized_features = self.scaler.fit_transform(all_features)
            
            # Apply DBSCAN clustering
            clustering = DBSCAN(eps=eps, min_samples=min_samples)
            cluster_labels = clustering.fit_predict(normalized_features)
            
            # Check if images are in different clusters (anomaly)
            anomaly_detected = cluster_labels[0] != cluster_labels[1]
            
            # Calculate feature distance
            feature_distance = cdist([normalized_features[0]], [normalized_features[1]], metric='euclidean')[0][0]
            
            result = {
                'anomaly_detected': anomaly_detected,
                'feature_distance': feature_distance,
                'cluster_labels': cluster_labels.tolist(),
                'confidence': min(feature_distance / 10.0, 1.0)  # Normalize to 0-1
            }
            
            self.logger.info(f"Anomaly detection: {anomaly_detected}, distance: {feature_distance:.4f}")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to detect anomalies: {str(e)}")
            return {'anomaly_detected': False, 'feature_distance': 0, 'confidence': 0}
    
    def analyze_semantic_differences(self, img1, img2):
        """Analyze semantic differences between images using AI techniques"""
        try:
            results = {
                'layout_changes': [],
                'content_changes': [],
                'style_changes': [],
                'structural_changes': []
            }
            
            # 1. Segment both images
            segments1, props1 = self.segment_image(img1)
            segments2, props2 = self.segment_image(img2)
            
            if not props1 or not props2:
                return results
            
            # 2. Match regions between images
            region_matches = self._match_regions(props1, props2)
            
            # 3. Analyze matched regions for changes
            for match in region_matches:
                if match['confidence'] > 0.7:  # High confidence matches
                    changes = self._analyze_region_changes(match['region1'], match['region2'])
                    
                    if changes['layout_change']:
                        results['layout_changes'].append(changes)
                    if changes['content_change']:
                        results['content_changes'].append(changes)
                    if changes['style_change']:
                        results['style_changes'].append(changes)
            
            # 4. Detect new/missing regions
            unmatched1 = [p for i, p in enumerate(props1) if i not in [m['idx1'] for m in region_matches]]
            unmatched2 = [p for i, p in enumerate(props2) if i not in [m['idx2'] for m in region_matches]]
            
            for region in unmatched1:
                results['structural_changes'].append({
                    'type': 'removed_element',
                    'region': region,
                    'confidence': 0.8
                })
            
            for region in unmatched2:
                results['structural_changes'].append({
                    'type': 'added_element',
                    'region': region,
                    'confidence': 0.8
                })
            
            self.logger.info(f"Semantic analysis complete: {len(results['layout_changes'])} layout, "
                           f"{len(results['content_changes'])} content, {len(results['style_changes'])} style, "
                           f"{len(results['structural_changes'])} structural changes")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to analyze semantic differences: {str(e)}")
            return {'layout_changes': [], 'content_changes': [], 'style_changes': [], 'structural_changes': []}
    
    def _match_regions(self, props1, props2, threshold=0.5):
        """Match regions between two images based on similarity"""
        matches = []
        
        for i, region1 in enumerate(props1):
            best_match = None
            best_score = 0
            
            for j, region2 in enumerate(props2):
                # Calculate similarity score
                score = self._calculate_region_similarity(region1, region2)
                
                if score > best_score and score > threshold:
                    best_score = score
                    best_match = j
            
            if best_match is not None:
                matches.append({
                    'idx1': i,
                    'idx2': best_match,
                    'region1': region1,
                    'region2': props2[best_match],
                    'confidence': best_score
                })
        
        return matches
    
    def _calculate_region_similarity(self, region1, region2):
        """Calculate similarity between two regions"""
        try:
            # Size similarity
            area_ratio = min(region1['area'], region2['area']) / max(region1['area'], region2['area'])
            
            # Position similarity
            centroid_distance = np.sqrt((region1['centroid'][0] - region2['centroid'][0])**2 + 
                                       (region1['centroid'][1] - region2['centroid'][1])**2)
            max_distance = np.sqrt(region1['centroid'][0]**2 + region1['centroid'][1]**2) + \
                          np.sqrt(region2['centroid'][0]**2 + region2['centroid'][1]**2)
            position_similarity = 1 - (centroid_distance / max_distance) if max_distance > 0 else 0
            
            # Shape similarity
            shape_similarity = min(region1['eccentricity'], region2['eccentricity']) / \
                              max(region1['eccentricity'], region2['eccentricity']) if \
                              max(region1['eccentricity'], region2['eccentricity']) > 0 else 0
            
            # Color similarity (if available)
            color_similarity = 1.0
            if isinstance(region1['mean_color'], np.ndarray) and isinstance(region2['mean_color'], np.ndarray):
                color_distance = np.linalg.norm(region1['mean_color'] - region2['mean_color'])
                color_similarity = 1 / (1 + color_distance / 100)  # Normalize
            
            # Combined similarity score
            similarity = (area_ratio * 0.3 + position_similarity * 0.4 + 
                         shape_similarity * 0.2 + color_similarity * 0.1)
            
            return similarity
            
        except Exception as e:
            self.logger.error(f"Failed to calculate region similarity: {str(e)}")
            return 0.0
    
    def _analyze_region_changes(self, region1, region2):
        """Analyze changes between two matched regions"""
        changes = {
            'layout_change': False,
            'content_change': False,
            'style_change': False,
            'position_change': 0,
            'size_change': 0,
            'color_change': 0
        }
        
        try:
            # Position change
            position_change = np.sqrt((region1['centroid'][0] - region2['centroid'][0])**2 + 
                                    (region1['centroid'][1] - region2['centroid'][1])**2)
            changes['position_change'] = position_change
            if position_change > 10:  # Threshold for significant movement
                changes['layout_change'] = True
            
            # Size change
            size_change = abs(region1['area'] - region2['area']) / max(region1['area'], region2['area'])
            changes['size_change'] = size_change
            if size_change > 0.2:  # 20% size change threshold
                changes['content_change'] = True
            
            # Color change (if available)
            if isinstance(region1['mean_color'], np.ndarray) and isinstance(region2['mean_color'], np.ndarray):
                color_change = np.linalg.norm(region1['mean_color'] - region2['mean_color'])
                changes['color_change'] = color_change
                if color_change > 20:  # Threshold for significant color change
                    changes['style_change'] = True
            
            return changes
            
        except Exception as e:
            self.logger.error(f"Failed to analyze region changes: {str(e)}")
            return changes
    
    def save_model(self, filepath):
        """Save the trained model and scaler"""
        try:
            model_data = {
                'scaler': self.scaler,
                'model': self.model
            }
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            self.logger.info(f"Model saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save model: {str(e)}")
    
    def load_model(self, filepath):
        """Load a trained model and scaler"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    model_data = pickle.load(f)
                self.scaler = model_data['scaler']
                self.model = model_data['model']
                self.logger.info(f"Model loaded from {filepath}")
                return True
            else:
                self.logger.warning(f"Model file not found: {filepath}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to load model: {str(e)}")
            return False

# Example usage
if __name__ == "__main__":
    detector = AIDetector()
    
    # Example with dummy images
    img1 = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    img2 = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    
    # Extract features
    features1 = detector.extract_features(img1)
    features2 = detector.extract_features(img2)
    
    print(f"Features extracted: {len(features1)} dimensions")
    
    # Detect anomalies
    anomaly_result = detector.detect_anomalies_clustering(features1, features2)
    print(f"Anomaly detection: {anomaly_result}")
    
    # Semantic analysis
    semantic_results = detector.analyze_semantic_differences(img1, img2)
    print(f"Semantic analysis: {semantic_results}")
