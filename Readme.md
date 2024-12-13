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
- 📥 **Upload fundus images** in PNG, JPG, or JPEG formats.
- 🔍 **Load Keras models** stored locally in the `saved_models` folder.
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
   git clone https://github.com/your-username/fundus-analysis-app.git
   cd fundus-analysis-app
