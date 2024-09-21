from flask import Flask, render_template, request, jsonify
from model import ElectionPredictor
from data_handler import DataHandler
import os

app = Flask(__name__)

# Initialize DataHandler and ElectionPredictor
data_handler = DataHandler()
predictor = ElectionPredictor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Validate input data
        if not all(key in data for key in ['region', 'population', 'gdp', 'unemployment']):
            return jsonify({'error': 'Missing required fields'}), 400

        # Preprocess input data
        processed_data = data_handler.preprocess_input(data)
        
        # Make prediction
        prediction = predictor.predict(processed_data)
        
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/train', methods=['POST'])
def train_model():
    try:
        # Load and preprocess training data
        training_data = data_handler.load_training_data()
        
        # Train the model
        accuracy = predictor.train(training_data)
        
        return jsonify({'message': 'Model trained successfully', 'accuracy': accuracy})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure the model is trained before starting the server
    if not predictor.is_trained():
        print("Training the model...")
        training_data = data_handler.load_training_data()
        predictor.train(training_data)
    
    app.run(host='0.0.0.0', port=5000)
