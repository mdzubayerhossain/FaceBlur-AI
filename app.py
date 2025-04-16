import os
import cv2
import numpy as np
from flask import Flask, request, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

# Configuration
# Use environment variables for flexibility across deployment environments
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp/uploads')
PROCESSED_FOLDER = os.environ.get('PROCESSED_FOLDER', '/tmp/processed')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def blur_faces(image_path, output_path):
    """
    Detect faces in the image and apply a natural blur effect to them
    """
    try:
        # Load the image
        img = cv2.imread(image_path)
        if img is None:
            return False, "Failed to read image"
        
        # Load face detection classifiers
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        profile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
        
        # Convert to grayscale for detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        # Detect faces
        frontal_faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(30, 30))
        profile_faces = profile_cascade.detectMultiScale(gray, 1.2, 5, minSize=(30, 30))
        
        # Combine face detections
        faces = list(frontal_faces) + list(profile_faces)
        
        face_count = 0
        
        # Process each detected face
        for (x, y, w, h) in faces:
            # Calculate center and radius for circular mask
            center_x = x + w // 2
            center_y = y + h // 2
            radius = int(max(w, h) // 2 * 1.2)
            
            # Create circular mask
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            cv2.circle(mask, (center_x, center_y), radius, 255, -1)
            
            # Extract face region
            face_roi = cv2.bitwise_and(img, img, mask=mask)
            
            # Apply blur
            blurred_face = cv2.GaussianBlur(face_roi, (31, 31), 10)
            
            # Create inverted mask
            mask_inv = cv2.bitwise_not(mask)
            
            # Extract background
            background = cv2.bitwise_and(img, img, mask=mask_inv)
            
            # Combine background and blurred face
            img = cv2.add(background, blurred_face)
            face_count += 1
        
        # Save the result
        cv2.imwrite(output_path, img)
        return True, face_count
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return False, f"Error processing image: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        try:
            # Generate unique filenames
            unique_id = str(uuid.uuid4())
            original_filename = secure_filename(file.filename)
            filename_parts = original_filename.rsplit('.', 1)
            
            # Create secure filenames with unique ID
            original_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                        f"{filename_parts[0]}_{unique_id}.{filename_parts[1]}")
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], 
                                        f"{filename_parts[0]}_{unique_id}.{filename_parts[1]}")
            
            # Save the uploaded file
            file.save(original_path)
            
            # Process the image
            success, result = blur_faces(original_path, processed_path)
            
            if not success:
                return jsonify({'error': result})
            
            # Get filenames for URLs
            original_filename = os.path.basename(original_path)
            processed_filename = os.path.basename(processed_path)
            
            return jsonify({
                'success': True,
                'message': f"Processed successfully. Detected and blurred {result} faces." if result > 0 else "No faces detected in the image.",
                'original_image': f"/uploads/{original_filename}",
                'processed_image': f"/processed/{processed_filename}"
            })
        except Exception as e:
            print(f"Error in upload: {str(e)}")
            return jsonify({'error': f"Server error: {str(e)}"})
    
    return jsonify({'error': 'File type not allowed'})

# Routes to serve files from the storage directories
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

# For Vercel: add a health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'})

# For API usage
@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    # Same functionality as upload_file, just a different endpoint
    return upload_file()

# Initialize application
if __name__ == '__main__':
    # Get port from environment variable or use 8080 as default
    port = int(os.environ.get('PORT', 8080))
    # In production, set debug to False
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)