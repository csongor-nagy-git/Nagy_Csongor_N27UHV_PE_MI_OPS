# **Fundus Image Analysis with Keras Model**

🚀 **A web-based tool to analyze fundus images and predict diabetic retinopathy severity using a pre-trained Keras model.**

---

## **Table of Contents**
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Model Format](#model-format)
- [Prediction Categories](#prediction-categories)
- [Screenshots](#screenshots)
- [License](#license)

---

## **Overview**
This application provides an intuitive **Streamlit UI** for analyzing fundus images to detect diabetic retinopathy. Users can upload fundus images, load a Keras-based model, and view the predicted severity levels.

---

## **Features**
- 📥 **Upload fundus images** in PNG, JPG, or JPEG formats. (you can find sample images in data folder)
- 🔍 **Load Keras models** stored locally in the `saved_models` folder. (e.g.:  DR_EfficientNet_APTOS_Regression_Final.keras)
- 📊 **Predict severity** of diabetic retinopathy with a single click. 
- 🎯 **User-friendly interface** with image previews and result display.

---

## **Technologies Used**
- **Streamlit**: For the web interface.
- **Keras/TensorFlow**: For model loading and prediction.
- **Pillow**: For image processing.
- **NumPy**: For numerical computations.
- **Python 3.x**: Backend programming.

---

## **Setup and Installation**

### Prerequisites
- **Python 3.x** installed
- Virtual environment (recommended)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/csongor-nagy-git/Nagy_Csongor_N27UHV_PE_MI_OPS.git
   cd Nagy_Csongor_N27UHV_PE_MI_OPS

2. **Install required dependencies**:  
    ```bash
    pip install -r requirements.txt
    ```

3. **Place your Keras models** in the `saved_models` directory.  

4. **Run the application**:  
    ```bash
    python back_end.py
    streamlit run front_end.py
    ```

## **Usage**
- 🚀 **Load a Model**:  
   - Enter the name of a `.h5` or `.keras` model file located in the `saved_models` folder.  
   - Click the **"Load Model"** button to load the model.

- 📥 **Upload an Image**:  
   - Upload a fundus image in **PNG**, **JPG**, or **JPEG** format using the file uploader.  
   - The uploaded image will be displayed on the interface.

- 🔍 **Run Prediction**:  
   - Once the model is loaded and the image is uploaded, the app analyzes the image and predicts the severity level.  
   - The result will be displayed as one of the following severity categories.

## **Model Format**
- 📁 **Supported Formats**:  
   - The model must be saved in **`.h5`** or **`.keras`** format.  

- 📐 **Input Requirements**:  
   - The model should accept input images of shape **`(224, 224, 3)`**.  
   - Images are resized automatically to meet this requirement before being passed to the model.

- ✅ **Directory**:  
   - Place your model files in the **`saved_models`** folder.

## **Prediction Categories**
The application predicts one of the following severity levels for diabetic retinopathy:

| **Category** | **Description**                   |
|--------------|-----------------------------------|
| 0            | No Diabetic Retinopathy           |
| 1            | Mild Diabetic Retinopathy         |
| 2            | Moderate Diabetic Retinopathy     |
| 3            | Severe Diabetic Retinopathy       |
| 4            | Proliferative Diabetic Retinopathy|
