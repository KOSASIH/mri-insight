import os
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import tensorflow as tf
import cv2
import io
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_for_testing')

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif', 'tiff'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mock model for demonstration (would be replaced with a real model in production)
class MockMRIModel:
    def predict(self, image):
        # This is a placeholder for actual model prediction
        # In a real application, this would use a trained neural network
        return {
            'tumor_detected': np.random.choice([True, False], p=[0.3, 0.7]),
            'tumor_type': np.random.choice(['Benign', 'Malignant', 'N/A'], p=[0.2, 0.1, 0.7]),
            'confidence': np.random.uniform(0.7, 0.99) if np.random.random() > 0.3 else np.random.uniform(0.5, 0.7),
            'location': f"Region {np.random.choice(['A', 'B', 'C', 'D'])}" if np.random.random() > 0.3 else "N/A"
        }

# Initialize model
model = MockMRIModel()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """Preprocess the image for model input"""
    # In a real application, this would resize, normalize, etc.
    img = cv2.imread(image_path)
    if img is None:
        # Try with PIL if OpenCV fails
        pil_img = Image.open(image_path)
        img = np.array(pil_img)
        if pil_img.mode == 'RGBA':
            img = img[:, :, :3]  # Remove alpha channel
    
    # Resize to expected input size (example: 224x224)
    img = cv2.resize(img, (224, 224))
    
    # Normalize pixel values
    img = img / 255.0
    
    return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the file
        file.save(filepath)
        
        try:
            # Preprocess image
            processed_img = preprocess_image(filepath)
            
            # Get prediction
            prediction = model.predict(processed_img)
            
            # Return results
            return render_template('result.html', 
                                  filename=unique_filename,
                                  prediction=prediction)
        except Exception as e:
            flash(f'Error processing image: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('File type not allowed. Please upload an image (png, jpg, jpeg, tif, tiff).')
        return redirect(url_for('index'))

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for programmatic access"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the file
        file.save(filepath)
        
        try:
            # Preprocess image
            processed_img = preprocess_image(filepath)
            
            # Get prediction
            prediction = model.predict(processed_img)
            
            # Add file info to response
            prediction['filename'] = unique_filename
            
            return jsonify(prediction)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)