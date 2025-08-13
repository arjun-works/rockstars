import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from PIL import Image
import logging

class ScreenshotCapture:
    def __init__(self, browser="chrome", headless=True):
        self.browser = browser.lower()
        self.headless = headless
        self.driver = None
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging for screenshot capture"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def initialize_driver(self, resolution="1920x1080"):
        """Initialize the WebDriver based on browser choice"""
        try:
            width, height = map(int, resolution.split('x'))
            
            if self.browser == "chrome":
                options = ChromeOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-plugins")
                options.add_argument("--disable-images")
                options.add_argument(f"--window-size={width},{height}")
                options.add_argument("--force-device-scale-factor=1")
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                
            elif self.browser == "firefox":
                options = FirefoxOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument(f"--width={width}")
                options.add_argument(f"--height={height}")
                
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
                
            elif self.browser == "edge":
                options = EdgeOptions()
                if self.headless:
                    options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument(f"--window-size={width},{height}")
                
                service = EdgeService(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service, options=options)
            
            # Set window size
            self.driver.set_window_size(width, height)
            self.logger.info(f"Initialized {self.browser} driver with resolution {resolution}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize {self.browser} driver: {str(e)}")
            raise
    
    def capture_screenshot(self, url, output_path, wait_time=3, full_page=True):
        """Capture screenshot of a given URL"""
        try:
            if not self.driver:
                raise Exception("Driver not initialized. Call initialize_driver() first.")
            
            self.logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Additional wait time for dynamic content
            time.sleep(wait_time)
            
            # Hide scrollbars for consistent screenshots
            self.driver.execute_script("""
                document.documentElement.style.overflow = 'hidden';
                document.body.style.overflow = 'hidden';
            """)
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if full_page:
                # Get full page screenshot
                self._capture_full_page_screenshot(output_path)
            else:
                # Get viewport screenshot
                self.driver.save_screenshot(output_path)
            
            self.logger.info(f"Screenshot saved to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot for {url}: {str(e)}")
            raise
    
    def _capture_full_page_screenshot(self, output_path):
        """Capture full page screenshot by scrolling"""
        try:
            # Get page dimensions
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            viewport_height = self.driver.execute_script("return window.innerHeight")
            viewport_width = self.driver.execute_script("return window.innerWidth")
            
            # If page fits in viewport, take single screenshot
            if total_height <= viewport_height:
                self.driver.save_screenshot(output_path)
                return
            
            # Calculate number of screenshots needed
            screenshots_needed = (total_height + viewport_height - 1) // viewport_height
            screenshots = []
            
            for i in range(screenshots_needed):
                # Scroll to position
                scroll_position = i * viewport_height
                self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(0.5)  # Wait for scroll to complete
                
                # Take screenshot
                screenshot_path = f"{output_path}_part_{i}.png"
                self.driver.save_screenshot(screenshot_path)
                screenshots.append(screenshot_path)
            
            # Stitch screenshots together
            self._stitch_screenshots(screenshots, output_path, viewport_width, viewport_height, total_height)
            
            # Clean up individual screenshots
            for screenshot in screenshots:
                if os.path.exists(screenshot):
                    os.remove(screenshot)
                    
        except Exception as e:
            self.logger.error(f"Failed to capture full page screenshot: {str(e)}")
            raise
    
    def _stitch_screenshots(self, screenshot_paths, output_path, width, viewport_height, total_height):
        """Stitch multiple screenshots into one image"""
        try:
            # Create new image with full page dimensions
            full_screenshot = Image.new('RGB', (width, total_height))
            
            y_offset = 0
            for i, screenshot_path in enumerate(screenshot_paths):
                if os.path.exists(screenshot_path):
                    img = Image.open(screenshot_path)
                    
                    # For the last screenshot, we might need to crop it
                    if i == len(screenshot_paths) - 1:
                        remaining_height = total_height - y_offset
                        if img.height > remaining_height:
                            img = img.crop((0, 0, width, remaining_height))
                    
                    full_screenshot.paste(img, (0, y_offset))
                    y_offset += img.height
                    img.close()
            
            # Save the stitched image
            full_screenshot.save(output_path, 'PNG', optimize=True, quality=95)
            full_screenshot.close()
            
        except Exception as e:
            self.logger.error(f"Failed to stitch screenshots: {str(e)}")
            raise
    
    def capture_element_screenshot(self, url, element_selector, output_path, wait_time=3):
        """Capture screenshot of a specific element"""
        try:
            if not self.driver:
                raise Exception("Driver not initialized. Call initialize_driver() first.")
            
            self.logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            time.sleep(wait_time)
            
            # Find the element
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
            )
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Take screenshot of the element
            element.screenshot(output_path)
            
            self.logger.info(f"Element screenshot saved to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to capture element screenshot: {str(e)}")
            raise
    
    def get_page_info(self, url):
        """Get page information like title, dimensions, etc."""
        try:
            if not self.driver:
                raise Exception("Driver not initialized. Call initialize_driver() first.")
            
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            info = {
                'title': self.driver.title,
                'url': self.driver.current_url,
                'viewport_width': self.driver.execute_script("return window.innerWidth"),
                'viewport_height': self.driver.execute_script("return window.innerHeight"),
                'page_width': self.driver.execute_script("return document.body.scrollWidth"),
                'page_height': self.driver.execute_script("return document.body.scrollHeight"),
                'user_agent': self.driver.execute_script("return navigator.userAgent")
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Failed to get page info for {url}: {str(e)}")
            raise
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing WebDriver: {str(e)}")
            finally:
                self.driver = None

# Example usage
if __name__ == "__main__":
    # Example usage
    capturer = ScreenshotCapture(browser="chrome", headless=True)
    
    try:
        capturer.initialize_driver(resolution="1920x1080")
        
        # Capture screenshots
        capturer.capture_screenshot(
            "https://example.com", 
            "screenshots/example1.png",
            wait_time=3,
            full_page=True
        )
        
        # Get page information
        info = capturer.get_page_info("https://example.com")
        print(f"Page info: {info}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        capturer.close()
