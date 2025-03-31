import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

try:
    # Load dataset
    file_path = "solar_power_classification.csv"
    data = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found. Please check the file path.")
    exit()

# Display basic info
print("Dataset Info:")
print(data.info())
print("\nFirst few rows:")
print(data.head())

# Handle missing values (numeric columns)
numeric_cols = data.select_dtypes(include=[np.number]).columns
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

# Exploratory Data Analysis
plt.figure(figsize=(10,6))
sns.heatmap(data[numeric_cols].corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title("Feature Correlation Matrix")
plt.show()

# Selecting features and target
target_column = "Power_Output"
try:
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset. Available columns: {list(data.columns)}")

    X = data.drop(columns=[target_column])
    y = data[target_column]

    # Convert categorical features to numerical if any exist
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        print(f"Converting categorical columns to numerical: {list(categorical_cols)}")
        X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

    # Check if we have enough data
    if len(X) < 10:
        raise ValueError("Dataset is too small for meaningful training.")

    # Splitting data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predictions on test set
    y_pred = model.predict(X_test)

    # Evaluation
    accuracy = accuracy_score(y_test, y_pred)
    print("\nModel Performance on Test Set:")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Feature Importance
    feat_importances = pd.Series(model.feature_importances_, index=X.columns)
    plt.figure(figsize=(10,6))
    feat_importances.nlargest(10).plot(kind='barh')
    plt.title("Top 10 Feature Importances")
    plt.xlabel("Importance Score")
    plt.show()

    # Save model
    joblib.dump(model, "solar_failure_model.pkl")
    print("Model successfully saved as 'solar_failure_model.pkl'.")

    # Prediction function for new data
    def predict_solar_output(temperature, sunlight_hours, humidity, panel_angle):
        """
        Predict solar power output given input features
        Parameters: temperature (°C), sunlight_hours (hours), humidity (%), panel_angle (degrees)
        Returns: 'Low' or 'High' prediction with correct probabilities
        """
        # Create a DataFrame with the same structure as training data
        new_data = pd.DataFrame({
            'Temperature': [temperature],
            'Sunlight_Hours': [sunlight_hours],
            'Humidity': [humidity],
            'Panel_Angle': [panel_angle]
        })
        
        # Make prediction
        prediction = model.predict(new_data)[0]
        probability = model.predict_proba(new_data)[0]
        
        # Align probabilities with class labels
        class_order = model.classes_
        if class_order[0] == 'Low':
            prob_low = probability[0]
            prob_high = probability[1]
        else:
            prob_low = probability[1]
            prob_high = probability[0]
        
        return {
            'Prediction': prediction,
            'Probability_Low': prob_low,
            'Probability_High': prob_high
        }

    # Example predictions
    print("\nExample Predictions:")
    examples = [
        (25.0, 8.0, 50.0, 30.0),  # Typical conditions
        (40.0, 10.0, 25.0, 35.0), # Hot, sunny conditions
        (15.0, 4.0, 75.0, 20.0)   # Cool, cloudy conditions
    ]
    
    for temp, sun, hum, angle in examples:
        result = predict_solar_output(temp, sun, hum, angle)
        print(f"\nTemperature: {temp}°C, Sunlight: {sun}h, Humidity: {hum}%, Angle: {angle}°")
        print(f"Prediction: {result['Prediction']}")
        print(f"Probability - Low: {result['Probability_Low']:.2%}, High: {result['Probability_High']:.2%}")

    # Interactive prediction
    print("\nEnter your own values for prediction (or press Enter to skip):")
    try:
        temp = input("Temperature (°C): ")
        if temp:  # Only proceed if user entered a value
            temp = float(temp)
            sun = float(input("Sunlight Hours: "))
            hum = float(input("Humidity (%): "))
            angle = float(input("Panel Angle (degrees): "))
            
            result = predict_solar_output(temp, sun, hum, angle)
            print(f"\nYour Input Prediction:")
            print(f"Prediction: {result['Prediction']}")
            print(f"Probability - Low: {result['Probability_Low']:.2%}, High: {result['Probability_High']:.2%}")
        else:
            print("Prediction skipped.")
    except ValueError:
        print("Error: Please enter valid numerical values.")

except ValueError as e:
    print(f"Error: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
