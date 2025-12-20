# Chicken Disease Detection System

A Streamlit-based web application that uses Convolutional Neural Networks (CNN) to detect chicken diseases from fecal images. The application loads two pre-trained models (HDF5 and pickled formats) to provide dual predictions and confidence scores.

## Features

- **Disease Classification**: Detects four classes of chicken fecal samples:
  - 🐔 Coccidiosis
  - ✅ Healthy
  - 🦠 New Castle Disease
  - 🦠 Salmonella

- **Dual Model Prediction**: Uses both HDF5 and pickled CNN models for cross-validation
- **Confidence Scoring**: Displays prediction confidence with color-coded indicators
- **Visual Analysis**: Shows detailed probability distributions using matplotlib charts
- **Recommendations**: Provides actionable advice based on detection results
- **User-Friendly Interface**: Clean, responsive UI built with Streamlit and custom CSS
- **Data Source**: Dataset from Kaggle (https://www.kaggle.com/datasets/efoeetienneblavo/chicken-disease-dataset)

## Prerequisites

- Python 3.7+
- Required model files:
  - `cnn_model.h5` (HDF5 format)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure the model files (`cnn_model.h5` and `model_cnn.pkl`) are in the same directory as `app.py`
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open your browser to the provided local URL (typically http://localhost:8501)
4. Upload a chicken fecal image (JPG, JPEG, or PNG format)
5. View the analysis results, including predictions from both models, confidence levels, and recommendations

## Model Details

- **Input**: RGB images resized to 150x150 pixels
- **Architecture**: Convolutional Neural Network (CNN)
- **Output**: Probability distribution across 4 disease classes
- **Preprocessing**: Image normalization (divide by 255.0)

## File Structure

```
├── app.py                 # Main application (FastAPI)
├── requirements.txt       # Python dependencies
├── model/cnn_model.h5      # HDF5 model file
└── README.md             # This file
```

## Dependencies

- FastAPI: Backend application framework
- tensorflow: Machine learning framework
- numpy: Numerical computing
- pillow: Image processing
- matplotlib: Data visualization

## Disclaimer

This is an AI-powered diagnostic tool for educational and research purposes. Always consult with a qualified veterinarian for definitive diagnosis and treatment. The predictions are based on trained models and may not be 100% accurate.

## License

This project is for educational purposes. Please ensure compliance with relevant data usage and privacy regulations when deploying or using this application.