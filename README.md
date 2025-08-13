# Visual AI Regression Testing Module

A comprehensive Python-based visual regression testing tool that uses AI and computer vision techniques to detect differences between web pages. This module combines traditional image comparison methods with advanced AI algorithms to provide detailed analysis of layout shifts, color changes, missing elements, and other visual differences.

## Features

### 🖼️ **Screenshot Capture**
- Multi-browser support (Chrome, Firefox, Edge)
- Full-page and viewport screenshots
- Customizable resolutions
- Automatic WebDriver management

### 🔍 **Advanced Image Analysis**
- **Structural Similarity (SSIM)** for overall comparison
- **Layout Shift Detection** using contour analysis
- **Color Difference Analysis** with threshold-based detection
- **Missing/Overlapping Element Detection** using computer vision
- **Font and Style Change Detection**

### 🤖 **AI-Powered Analysis**
- Feature extraction using HOG, LBP, and texture analysis
- Anomaly detection using clustering algorithms
- Semantic analysis of image regions
- Machine learning-based difference classification

### 📊 **Comprehensive Reporting**
- Interactive HTML reports with collapsible sections
- Professional PDF reports with tables and charts
- JSON reports for programmatic access
- Visual comparison images with annotations
- Difference heatmaps and highlighted regions

### 🖥️ **User-Friendly Interface**
- Modern Tkinter GUI with progress tracking
- Easy URL input and configuration
- Real-time analysis progress updates
- One-click report viewing

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows operating system
- Internet connection for WebDriver downloads

### Quick Start

1. **Clone or download the project** to your desired directory
2. **Run the batch file** for automatic setup:
   ```cmd
   run_visual_regression.bat
   ```

   Or use PowerShell:
   ```powershell
   .\run_visual_regression.ps1
   ```

3. **Manual installation** (if needed):
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

## Usage

### GUI Application

1. **Launch the application** using the batch file or by running `python main.py`
2. **Enter URLs**: Input the reference URL (original) and test URL (modified version)
3. **Configure options**:
   - Select browser (Chrome, Firefox, Edge)
   - Choose resolution (1920x1080, 1366x768, etc.)
   - Enable/disable analysis types:
     - Layout shift detection
     - Font/color analysis
     - Missing/overlapping elements
     - AI-powered analysis
4. **Start analysis** and monitor progress
5. **View results** in the application or generated reports

### Command Line Usage

```python
from visual_ai_regression import VisualAIRegression

# Configuration
config = {
    'url1': 'https://example.com/original',
    'url2': 'https://example.com/modified',
    'browser': 'chrome',
    'resolution': '1920x1080',
    'layout_shift': True,
    'font_color': True,
    'element_detection': True,
    'ai_analysis': True
}

# Run analysis
regression = VisualAIRegression()
results = regression.run_analysis(config)

print(f"Analysis complete: {results['summary']}")
```

## Project Structure

```
Visual-AI-Regression-Module/
├── main.py                     # Main GUI application
├── visual_ai_regression.py     # Core regression analysis logic
├── screenshot_capture.py       # Screenshot capture functionality
├── image_comparison.py         # OpenCV-based image comparison
├── ai_detector.py             # AI-powered difference detection
├── report_generator.py        # Report generation (HTML, PDF, JSON)
├── requirements.txt           # Python dependencies
├── run_visual_regression.bat  # Windows batch launcher
├── run_visual_regression.ps1  # PowerShell launcher
├── README.md                  # This file
├── .github/
│   └── copilot-instructions.md # Copilot configuration
├── screenshots/               # Generated screenshots
├── reports/                   # Generated reports
└── visualizations/           # Generated comparison images
```

## Key Components

### 1. Screenshot Capture (`screenshot_capture.py`)
- **Multi-browser support** with automatic WebDriver management
- **Full-page screenshots** with intelligent stitching
- **Element-specific screenshots** for targeted analysis
- **Page information extraction** (dimensions, metadata)

### 2. Image Comparison (`image_comparison.py`)
- **SSIM calculation** for structural similarity
- **Layout shift detection** using contour analysis
- **Color difference analysis** with clustering
- **Missing element detection** using morphological operations
- **Visual annotation** and heatmap generation

### 3. AI Detector (`ai_detector.py`)
- **Feature extraction**: HOG, LBP, texture, shape features
- **Anomaly detection** using DBSCAN clustering
- **Semantic analysis** with region matching
- **Machine learning** classification (extensible)

### 4. Report Generator (`report_generator.py`)
- **HTML reports** with interactive elements
- **PDF reports** with professional formatting
- **JSON exports** for API integration
- **Visual comparisons** with highlighted differences

## Configuration Options

### Analysis Types
- **Layout Shifts**: Detect element movement and repositioning
- **Font/Color Changes**: Identify text and color modifications
- **Missing Elements**: Find removed or added page elements
- **AI Analysis**: Advanced pattern recognition and anomaly detection

### Browser Options
- **Chrome** (default, fastest)
- **Firefox** (good compatibility)
- **Edge** (Windows-optimized)

### Resolution Options
- 1920x1080 (Full HD)
- 1366x768 (Laptop standard)
- 1440x900 (Mac-like)
- 1280x720 (HD)

## Output Files

### Generated Reports
- `visual_regression_report_TIMESTAMP.html` - Interactive HTML report
- `visual_regression_report_TIMESTAMP.pdf` - Professional PDF report
- `visual_regression_report_TIMESTAMP.json` - Machine-readable data
- `visual_regression_report_TIMESTAMP_visual_comparison.png` - Side-by-side comparison

### Analysis Images
- `difference_heatmap.png` - Color-coded difference visualization
- `annotated_comparison.png` - Annotated side-by-side comparison
- Original screenshots in `screenshots/` directory

## Troubleshooting

### Common Issues

1. **WebDriver Issues**
   - Ensure internet connection for automatic driver downloads
   - Update browser to latest version
   - Check antivirus/firewall settings

2. **Python/Package Issues**
   - Use Python 3.8+ (check with `python --version`)
   - Install Visual C++ Redistributable for OpenCV
   - Update pip: `python -m pip install --upgrade pip`

3. **Memory Issues**
   - Reduce image resolution for large pages
   - Close other applications during analysis
   - Use viewport screenshots instead of full-page

4. **Permission Issues**
   - Run as administrator if needed
   - Check folder write permissions
   - Ensure antivirus allows Python execution

### Performance Tips

- Use Chrome browser for fastest performance
- Enable only needed analysis types
- Use lower resolutions for faster processing
- Process images in batches for multiple URLs

## Development

### Extending the Module

1. **Custom AI Models**: Add your own ML models in `ai_detector.py`
2. **Additional Browsers**: Extend `screenshot_capture.py`
3. **New Report Formats**: Modify `report_generator.py`
4. **Custom Analysis**: Add methods to `image_comparison.py`

### API Integration

The module can be integrated into CI/CD pipelines:

```python
# Example CI integration
def run_regression_test(base_url, test_url):
    config = {
        'url1': base_url,
        'url2': test_url,
        'browser': 'chrome',
        'resolution': '1920x1080',
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': False  # Faster for CI
    }
    
    regression = VisualAIRegression()
    results = regression.run_analysis(config)
    
    # Return pass/fail based on similarity threshold
    return results['analysis_results']['similarity_score'] > 0.95
```

## Dependencies

- **selenium** >= 4.15.0 - Web automation and screenshot capture
- **opencv-python** >= 4.8.0 - Computer vision and image processing
- **Pillow** >= 10.0.0 - Image manipulation and processing
- **numpy** >= 1.24.0 - Numerical computations
- **scikit-image** >= 0.21.0 - Advanced image analysis
- **webdriver-manager** >= 4.0.0 - Automatic WebDriver management
- **matplotlib** >= 3.7.0 - Plotting and visualization
- **reportlab** >= 4.0.0 - PDF report generation
- **requests** >= 2.31.0 - HTTP requests
- **beautifulsoup4** >= 4.12.0 - HTML parsing

## License

This project is provided as-is for educational and development purposes. Please ensure compliance with website terms of service when testing external URLs.

## Support

For issues and feature requests, please check the troubleshooting section above or review the code documentation in each module.

---

**Visual AI Regression Module** - Bringing AI-powered visual testing to your development workflow.
