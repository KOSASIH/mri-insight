# MRI Insight

MRI Insight is a user-friendly platform that allows healthcare professionals to upload MRI images and receive instant analysis and tumor classification, enhancing decision-making in patient care.

![MRI Insight Platform](https://via.placeholder.com/800x400?text=MRI+Insight+Platform)

## Features

- **Upload MRI Scans**: Simple drag-and-drop interface for uploading brain MRI scans
- **Instant Analysis**: Get immediate results with advanced AI algorithms
- **Tumor Detection**: Identifies the presence of tumors with confidence scoring
- **Tumor Classification**: Accurate classification of tumor types with confidence scores
- **Location Identification**: Pinpoints the location of detected tumors
- **Report Generation**: Creates downloadable/printable reports for patient records
- **API Access**: Programmatic access for integration with existing systems
- **Secure & Private**: All uploads are processed securely with no permanent storage

## Installation

1. Clone the repository:
```bash
git clone https://github.com/KOSASIH/mri-insight.git
cd mri-insight
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at http://localhost:8080

## Usage

### Web Interface

1. Open your browser and navigate to http://localhost:8080
2. Click on the "Choose File" button to select an MRI scan image
3. Click "Analyze MRI Scan" to upload and process the image
4. View the analysis results, including tumor detection, classification, and confidence scores

### API Access

You can also use the API endpoint for programmatic access:

```bash
curl -X POST -F "file=@/path/to/your/mri_image.jpg" http://localhost:8080/api/analyze
```

Response format:
```json
{
  "tumor_detected": true,
  "tumor_type": "Benign",
  "confidence": 0.92,
  "location": "Region A",
  "filename": "unique_filename.jpg"
}
```

## Technical Details

- **Backend**: Built with Flask, a lightweight Python web framework
- **Image Processing**: Uses OpenCV and PIL for image preprocessing
- **Machine Learning**: Designed for TensorFlow/Keras models (mock model included for demonstration)
- **Frontend**: Responsive design with Bootstrap 5, custom CSS, and JavaScript
- **Supported Formats**: PNG, JPG, JPEG, TIF, TIFF
- **Deployment**: Ready for containerization with Docker and deployment with Gunicorn
- **Security**: Implements secure file handling and validation

## Development

### Project Structure

```
mri_insight/
├── app.py              # Main application file
├── __init__.py         # Package initialization
├── requirements.txt    # Python dependencies
├── static/             # Static files
│   ├── css/            # CSS stylesheets
│   │   └── style.css   # Custom styles
│   └── js/             # JavaScript files
│       └── main.js     # Custom scripts
├── templates/          # HTML templates
│   ├── index.html      # Upload page
│   └── result.html     # Results page
├── uploads/            # Directory for uploaded images
└── README.md           # Project documentation
```

### Adding a Custom Model

To replace the mock model with your own trained model:

1. Create a new model class that implements the `predict` method
2. Update the model initialization in `app.py`
3. Ensure your model's preprocessing requirements match the `preprocess_image` function

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is intended to be used as a decision support system and not as a replacement for professional medical judgment. Always consult with a qualified healthcare provider for diagnosis and treatment decisions.
