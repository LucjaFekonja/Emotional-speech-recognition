# Emotional-speech-recognition
This project implements a system for recognizing emotions from speech and modifying the emotional tone of the speech in real-time. The system leverages machine learning models and signal processing techniques to analyze speech characteristics. The application provides a user-friendly interface with sliders and buttons to modify the emotional tone of speech based on the detected emotion.

## Features
- __Emotion detection:__ Recognizes the emotional tone from a speech recording, identifying emotions such as happiness, sadness, anger, fear, surprise, disgust, and neutrality.
- __Emotion Modulation:__ Allows real-time adjustment of the emotional tone of the speech by modifying its pitch, tempo, and volume to match the selected emotion.
- __User Interface:__ Interactive sliders and buttons enable users to control and modify speech characteristics.

## Installation
1. Clone the repository:
```
git https://github.com/LucjaFekonja/Emotional-speech-recognition.git
cd Emotional-speech-recognition
```

2. Install required dependencies:
```
pip install -r requirements.txt
```

3. Run the application
- using SAVEE database:
```
python app.py savee
```
- using TESS database:
```
python app.py tess
```