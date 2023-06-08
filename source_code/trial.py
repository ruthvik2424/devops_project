import os.path
import librosa
import numpy as np
from keras.models import Sequential, model_from_json
from flask import Flask, request
from flask_restful import Api, Resource
import base64

app = Flask(__name__)
api = Api(app)

# check if the model file exists
model_file = 'stutter_detection_modela.h5'
if not os.path.isfile(model_file):
    raise Exception("Model file does not exist")

# load the model architecture from a file
json_file = open('stutter_detection_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

# create the model from the loaded architecture
loaded_model = model_from_json(loaded_model_json)

# load the saved model weights into the model
loaded_model.load_weights(model_file)


@app.route('/process', methods=['POST'])
def post():
    # Get the Base64-encoded audio data from the request body
    data = request.data
    base64Audio = data['audioData']

    # Decode the Base64-encoded audio data
    audioBytes = base64.b64decode(base64Audio)

    # Process the audio data as needed
    def extract_features(audio_path):
        signal, sr = librosa.load(audio_path, sr=44100)
        mfcc_features = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=20)
        # calculate the mean of each MFCC coefficient
        features = np.mean(mfcc_features, axis=1)
        return features

    # extract features from the audio file to be predicted
    audio_file = audioBytes
    features = extract_features(audio_file)

    # predict the class probability of the audio file
    probabilities = loaded_model.predict(np.array([features]))
    predicted_class = round(probabilities[0][0])

    # print the predicted class and probability

    def predict():
        if predicted_class == 0:
            return "The audio file is normal"
        else:
            return "The audio file contains stuttering"

    # calculate the accuracy of the prediction
    test_X = np.array([features])
    test_y = np.array([1])  # provide the true label of the audio file
    loss, accuracy = loaded_model.evaluate(test_X, test_y)

    def final_result():
        final_result = {
            'message': 'Audio data received and processed',
            'probability': probabilities[0][0],
            'prediction': predict()
        }
        return final_result

    return final_result()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)