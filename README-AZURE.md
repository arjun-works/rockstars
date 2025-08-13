# Visual AI Regression Testing - Azure Deployment

This repository contains a Visual AI Regression Testing application converted for web deployment on Azure App Service.

## Overview

The Visual AI Regression Testing Module is a powerful tool for comparing images and detecting visual differences in web applications. It uses advanced computer vision techniques and AI algorithms to identify layout shifts, color changes, and other visual regression issues.

## Features

- **Image Comparison**: Upload two images for detailed comparison
- **AI-Powered Analysis**: Advanced algorithms detect subtle differences
- **Visual Reporting**: Generate comprehensive reports with difference highlights
- **Web Interface**: Modern, responsive web interface built with Bootstrap
- **Real-time Progress**: Live updates during analysis
- **Downloadable Results**: Export complete analysis results

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Computer Vision**: OpenCV, scikit-image
- **AI/ML**: NumPy, scikit-learn
- **Image Processing**: Pillow (PIL)
- **Report Generation**: ReportLab, Matplotlib
- **Cloud Platform**: Azure App Service

## Deployment to Azure

### Prerequisites

1. **Azure Account**: You need an active Azure subscription
2. **Azure CLI**: Install from [Azure CLI Installation Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
3. **Git**: Ensure Git is installed on your system

### Quick Deployment

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd TestProject_1
   ```

2. **Login to Azure**:
   ```bash
   az login
   ```

3. **Run the deployment script**:
   
   **For Linux/macOS**:
   ```bash
   chmod +x deploy-to-azure.sh
   ./deploy-to-azure.sh
   ```
   
   **For Windows PowerShell**:
   ```powershell
   .\deploy-to-azure.ps1
   ```

4. **Follow the prompts** and wait for deployment to complete

### Manual Deployment

If you prefer manual deployment:

1. **Create Resource Group**:
   ```bash
   az group create --name visual-ai-regression-rg --location "East US"
   ```

2. **Deploy ARM Template**:
   ```bash
   az deployment group create \
     --resource-group visual-ai-regression-rg \
     --template-file azure-template.json \
     --parameters appName=your-app-name
   ```

3. **Configure Git Deployment**:
   ```bash
   az webapp deployment source config-local-git \
     --name your-app-name \
     --resource-group visual-ai-regression-rg
   ```

4. **Deploy Code**:
   ```bash
   git remote add azure <azure-git-url>
   git push azure main
   ```

## Configuration

### Environment Variables

The application uses the following environment variables:

- `SECRET_KEY`: Flask secret key (automatically generated during deployment)
- `PORT`: Port number (automatically set by Azure)

### App Service Settings

The deployment configures:
- **Python Runtime**: 3.9
- **Startup Command**: `gunicorn --bind=0.0.0.0 --timeout 600 app:app`
- **Build Process**: Oryx build enabled
- **Instance Size**: B2 (recommended for image processing)

## Usage

1. **Access the Web Application**: Navigate to your Azure App Service URL
2. **Upload Images**: 
   - Upload a baseline image (reference)
   - Upload a current image (to compare)
3. **Configure Analysis**:
   - Set sensitivity level (0.1 - 1.0)
   - Choose analysis type (Quick, Comprehensive, Detailed)
   - Enable/disable specific detection features
4. **Start Analysis**: Click "Start Analysis" and wait for results
5. **View Results**: Review metrics, difference visualization, and download reports

## File Structure

```
├── app.py                     # Flask web application
├── templates/
│   └── index.html            # Web interface
├── visual_ai_regression.py   # Core analysis engine
├── image_comparison.py       # Image comparison algorithms
├── ai_detector.py           # AI-powered difference detection
├── report_generator.py      # Report generation
├── screenshot_capture.py    # Screenshot functionality
├── requirements-web.txt     # Python dependencies for web
├── azure-template.json      # Azure ARM template
├── deploy-to-azure.sh       # Linux/macOS deployment script
├── deploy-to-azure.ps1      # Windows deployment script
├── web.config              # IIS configuration (if needed)
├── Procfile                # Process file for deployment
└── runtime.txt             # Python runtime version
```

## Monitoring and Troubleshooting

### View Logs
```bash
az webapp log tail --name your-app-name --resource-group visual-ai-regression-rg
```

### Access Kudu Console
Navigate to: `https://your-app-name.scm.azurewebsites.net`

### Monitor Performance
Use Azure Application Insights for detailed monitoring and analytics.

## Cost Optimization

- **Basic Tier (B1/B2)**: Recommended for development and testing
- **Standard Tier (S1/S2)**: Recommended for production workloads
- **Auto-scaling**: Configure based on usage patterns

## Security Considerations

1. **HTTPS**: Always enabled by default
2. **File Upload Limits**: Configured for image files only
3. **Session Management**: Temporary files are cleaned up automatically
4. **Environment Variables**: Sensitive data stored securely

## Support

For issues and questions:
1. Check the application logs in Azure portal
2. Review the troubleshooting section in this README
3. Submit issues through the repository issue tracker

## License

This project is licensed under the MIT License - see the LICENSE file for details.
