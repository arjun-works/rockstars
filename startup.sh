#!/bin/bash

# Install system dependencies for OpenCV and other packages
apt-get update
apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 libgtk-3-0 libgl1-mesa-glx

# Install Chrome for Selenium
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Start the application
python -m gunicorn --bind=0.0.0.0 --timeout 600 app:app
