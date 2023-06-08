import os.path
import librosa
import numpy as np
from keras.models import Sequential, model_from_json
from flask import Flask, request, jsonify, render_template
import base64
import tempfile

app = Flask(__name__)

# Check if the model file exists
model_file = 'stutter_detection_modela.h5'
if not os.path.isfile(model_file):
    raise Exception("Model file does not exist")

# Load the model architecture from a file
json_file = open('stutter_detection_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

# Create the model from the loaded architecture
loaded_model = model_from_json(loaded_model_json)

# Load the saved model weights into the model
loaded_model.load_weights(model_file)

# Compile the model
loaded_model.compile(optimizer='adam', loss='binary_crossentropy')

@app.route('/')
def Home():
    return render_template('index.html')
@app.route('/process', methods=['POST'])
def process_audio():
    # Get the Base64-encoded audio data from the request body
    data = request.json
    base64_audio = data['audioData']

    # Decode the Base64-encoded audio data
    audio_bytes = base64.b64decode(base64_audio)

    # Save the audio data as a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as audio_file:
        audio_file.write(audio_bytes)
        audio_path = audio_file.name

    # Process the audio data and extract features
    def extract_features(audio_path):
        signal, sr = librosa.load(audio_path, sr=44100)
        mfcc_features = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=20)
        # Calculate the mean of each MFCC coefficient
        features = np.mean(mfcc_features, axis=1)
        return features

    # Extract features from the audio file to be predicted
    features = extract_features(audio_path)

    # Predict the class probability of the audio file
    probabilities = loaded_model.predict(np.array([features]))
    predicted_class = round(probabilities[0][0])

    def predict():
        if predicted_class == 0:
            return "The audio file is normal"
        else:
            return "The audio file contains stuttering"

    # Prepare the response
    response = {
        'message': 'Audio data received and processed',
        'probability': float(probabilities[0][0]),
        'prediction': predict()
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
