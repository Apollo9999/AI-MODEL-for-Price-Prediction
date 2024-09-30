import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from openvino.runtime import Core

# Assuming Intel oneAPI MKL is used for optimized matrix computations
from sklearnex import patch_sklearn
patch_sklearn()  # Patching scikit-learn with Intel accelerated implementations

# Sample dataset (You can load your real-world dataset here)
# Assuming you have features like 'weight', 'distance', 'fuel_cost', 'shipment_type' for prediction
data = {
    'weight': [10, 20, 15, 30, 5],
    'distance': [100, 200, 150, 300, 50],
    'fuel_cost': [3.5, 3.7, 3.6, 3.8, 3.4],
    'shipment_type': [1, 2, 1, 3, 1],  # Categorical encoded
    'shipping_cost': [100, 200, 150, 300, 75]  # Target (shipping cost)
}
df = pd.DataFrame(data)

# Split dataset into features (X) and target (y)
X = df.drop('shipping_cost', axis=1)
y = df['shipping_cost']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build and train the model (Gradient Boosting Regressor)
model = GradientBoostingRegressor()
model.fit(X_train, y_train)

# Evaluate the model on the test data
y_pred = model.predict(X_test)
print("Mean Absolute Error on Test Data: ", mean_absolute_error(y_test, y_pred))

# Save the model to disk
import joblib
joblib.dump(model, 'shipping_cost_model.pkl')

# -------------------------------------------------------
# Intel OPENVINO Part: Optimizing and running inference
# -------------------------------------------------------

# Load OpenVINO Core
core = Core()

# Convert the trained model into OpenVINO IR format (Here assuming you use ONNX format)
# For simplicity, you would convert the model to ONNX first, then load it using OpenVINO

# Convert the model to ONNX format (this would be done externally usually)
# You could convert via skl2onnx library or another method for scikit-learn

# Load the ONNX model into OpenVINO runtime
model_path = "shipping_cost_model.onnx"  # Assuming you've converted to ONNX
compiled_model = core.compile_model(model_path, "CPU")

# Prepare input data for inference
input_data = np.array([[15, 150, 3.6, 1]])  # Sample input: [weight, distance, fuel_cost, shipment_type]

# Inferencing with OPENVINO model
output_layer = compiled_model.output(0)
results = compiled_model([input_data])
predicted_cost = results[output_layer]

print(f"Predicted Shipping Cost: {predicted_cost}")

# Optional: You can integrate this with a REST API or user interface as needed
