from flask import Flask, render_template, request, jsonify, send_file, session
from werkzeug.utils import secure_filename
import os
import threading
from datetime import datetime
import uuid
from visual_ai_regression import VisualAIRegression
import zipfile
from io import BytesIO
import base64

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Configuration
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Global storage for analysis results (in production, use Redis or database)
analysis_results = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        if 'image1' not in request.files or 'image2' not in request.files:
            return jsonify({'error': 'Both images are required'}), 400
        
        file1 = request.files['image1']
        file2 = request.files['image2']
        
        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
            return jsonify({'error': 'Invalid file type. Please upload image files.'}), 400
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        
        # Create session directory
        session_dir = os.path.join(UPLOAD_FOLDER, session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        # Save uploaded files
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        
        filepath1 = os.path.join(session_dir, 'baseline_' + filename1)
        filepath2 = os.path.join(session_dir, 'current_' + filename2)
        
        file1.save(filepath1)
        file2.save(filepath2)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Files uploaded successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        session_id = session.get('session_id')
        
        if not session_id:
            return jsonify({'error': 'No session found. Please upload images first.'}), 400
        
        session_dir = os.path.join(UPLOAD_FOLDER, session_id)
        if not os.path.exists(session_dir):
            return jsonify({'error': 'Session not found'}), 400
        
        # Get uploaded files
        files = os.listdir(session_dir)
        baseline_file = None
        current_file = None
        
        for file in files:
            if file.startswith('baseline_'):
                baseline_file = os.path.join(session_dir, file)
            elif file.startswith('current_'):
                current_file = os.path.join(session_dir, file)
        
        if not baseline_file or not current_file:
            return jsonify({'error': 'Uploaded files not found'}), 400
        
        # Configure analysis
        config = {
            'baseline_image': baseline_file,
            'current_image': current_file,
            'sensitivity': data.get('sensitivity', 0.8),
            'analysis_type': data.get('analysis_type', 'comprehensive'),
            'detect_layout_shifts': data.get('detect_layout_shifts', True),
            'detect_color_changes': data.get('detect_color_changes', True),
            'detect_text_changes': data.get('detect_text_changes', True),
            'generate_report': True,
            'output_dir': os.path.join(RESULTS_FOLDER, session_id)
        }
        
        # Create results directory
        os.makedirs(config['output_dir'], exist_ok=True)
        
        # Start analysis in background thread
        def run_analysis():
            try:
                regression_module = VisualAIRegression()
                results = regression_module.run_image_analysis(config)
                analysis_results[session_id] = {
                    'status': 'completed',
                    'results': results,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                analysis_results[session_id] = {
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        # Initialize analysis status
        analysis_results[session_id] = {
            'status': 'running',
            'timestamp': datetime.now().isoformat()
        }
        
        # Start analysis thread
        thread = threading.Thread(target=run_analysis)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Analysis started successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status/<session_id>')
def get_status(session_id):
    try:
        if session_id not in analysis_results:
            return jsonify({'error': 'Session not found'}), 404
        
        status_data = analysis_results[session_id]
        
        if status_data['status'] == 'completed':
            # Prepare results for frontend
            results = status_data['results']
            
            # Convert images to base64 for display
            if 'difference_image_path' in results:
                try:
                    with open(results['difference_image_path'], 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode()
                        results['difference_image_base64'] = f"data:image/png;base64,{img_data}"
                except Exception:
                    results['difference_image_base64'] = None
            
            return jsonify({
                'status': 'completed',
                'results': results
            })
        
        return jsonify(status_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<session_id>')
def download_results(session_id):
    try:
        if session_id not in analysis_results:
            return jsonify({'error': 'Session not found'}), 404
        
        results_dir = os.path.join(RESULTS_FOLDER, session_id)
        if not os.path.exists(results_dir):
            return jsonify({'error': 'Results not found'}), 404
        
        # Create zip file of all results
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(results_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, results_dir)
                    zf.write(file_path, arc_path)
        
        memory_file.seek(0)
        
        return send_file(
            BytesIO(memory_file.getvalue()),
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'visual_regression_results_{session_id}.zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
