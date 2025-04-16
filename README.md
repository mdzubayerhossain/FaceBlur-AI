# FaceBlur AI

FaceBlur AI is a web application that uses computer vision to automatically detect and blur faces in images, providing a simple and effective way to protect privacy in photos.

![image](https://github.com/user-attachments/assets/77dc1a9c-ffcd-4f42-b4a0-4d912981ac83)
![image](https://github.com/user-attachments/assets/d9dad8da-13ce-4c4f-9f68-1ed3f2e496c6)



## 🌟 Features

- **Automatic Face Detection**: Detects both frontal and profile faces for maximum accuracy
- **Natural Blur Effect**: Applies a circular blur mask that looks natural while preserving privacy
- **User-Friendly Interface**: Clean, responsive design with drag-and-drop functionality
- **Fast Processing**: Efficiently processes images with minimal wait time
- **Secure**: All processing happens on the server, with no data stored long-term
- **Downloadable Results**: Easily download processed images with blurred faces

## 🚀 Live Demo

Check out the live demo at [Link](https://face-blur-ai-flask-ll15rzi9h-mdzubayerhossains-projects.vercel.app)

## 📋 Requirements

- Python 3.8+
- Flask
- OpenCV
- NumPy
- Werkzeug

## 💻 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/mdzubayerhossain/faceblur-ai.git
   cd faceblur-ai
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## 📁 Project Structure

```
face-blur-app/
│
├── app.py                  # Main Flask application
│
├── static/                 # Static files
│   ├── css/
│   │   └── style.css       # CSS styles
│   │
│   ├── js/
│   │   └── script.js       # JavaScript code
│   │
│   ├── img/                # Images for the README and website
│   │
│   ├── uploads/            # Directory for original uploaded images
│   │
│   └── processed/          # Directory for processed images with blurred faces
│
├── templates/
│   └── index.html          # HTML template
│
└── requirements.txt        # Python dependencies
```

## 🔧 How It Works

1. **Image Upload**: User uploads an image through the web interface
2. **Face Detection**: The application uses OpenCV's Haar Cascade classifiers to detect faces
3. **Blur Processing**: A Gaussian blur is applied to each detected face using a circular mask
4. **Result Display**: The original and processed images are displayed side by side
5. **Download**: User can download the processed image with blurred faces

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Computer Vision**: OpenCV
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with responsive design
- **Icons**: Font Awesome

## 🔒 Privacy

- All image processing happens on the server
- Uploaded images are temporarily stored and then deleted after processing
- No facial recognition or identification data is stored or used

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 📬 Contact

Project Link: [https://github.com/mdzubayerhossain/FaceBlur-AI](https://github.com/mdzubayerhossain/FaceBlur-AI)

---

Made with ❤️ for privacy protection
