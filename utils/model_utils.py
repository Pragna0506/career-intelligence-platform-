import joblib

def load_model(path):
    try:
        model = joblib.load(path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def load_encoder(path):
    try:
        encoder = joblib.load(path)
        return encoder
    except Exception as e:
        print(f"Error loading encoder: {e}")
        return None


def predict(model, input_data):
    try:
        return model.predict(input_data)
    except Exception as e:
        print(f"Prediction error: {e}")
        return None
