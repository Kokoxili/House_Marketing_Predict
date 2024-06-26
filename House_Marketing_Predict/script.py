# -*- coding: utf-8 -*-

# Problem 1

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import fetch_california_housing
california_housing = fetch_california_housing(as_frame=True).frame
data = california_housing


features = ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'MedHouseVal']
plt.figure(figsize=(15, 12))
for i, feature in enumerate(features, 1):
    plt.subplot(3, 3, i)
    sns.histplot(data[feature], bins=30, kde=True)
    plt.title(f'Distribution of {feature}')
plt.tight_layout()
plt.show()

# Problem 2

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

from sklearn.datasets import fetch_california_housing
california_housing = fetch_california_housing(as_frame=True).frame
data = california_housing

np.random.seed(0)  # For reproducibility
shuffle_indices = np.random.permutation(len(data))
split_index = int(len(data) * 0.8)  # Splitting at 80% for training

train_indices = shuffle_indices[:split_index]
test_indices = shuffle_indices[split_index:]

X_train = data['MedInc'].values[train_indices]
y_train = data['MedHouseVal'].values[train_indices]
X_test = data['MedInc'].values[test_indices]
y_test = data['MedHouseVal'].values[test_indices]

# 2. Implement the model (simple linear regression)
def linear_regression(X, y):
    # Calculate the means of X and y
    mean_X, mean_y = np.mean(X), np.mean(y)
    # Total number of values
    n = len(X)

    # Using the formula to calculate 'b1' and 'b0'
    numer = np.sum((X - mean_X) * (y - mean_y))
    denom = np.sum((X - mean_X) ** 2)

    b1 = numer / denom  # Slope
    b0 = mean_y - (b1 * mean_X)  # Intercept

    return (b1, b0)

# Fit the model to the training data
slope, intercept = linear_regression(X_train, y_train)

def predict(X, slope, intercept):
    return slope * X + intercept

def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# Predictions
y_pred_train = predict(X_train, slope, intercept)
y_pred_test = predict(X_test, slope, intercept)

# Calculate MSE
mse_train = mean_squared_error(y_train, y_pred_train)
mse_test = mean_squared_error(y_test, y_pred_test)

# Print out the MSE for both sets
print(f'Training MSE: {mse_train}')
print(f'Testing MSE: {mse_test}')

r_squared = r2_score(y_test, y_pred_test)
print("R-squared using scikit-learn:", r_squared)

# 4. Plot the errors
plt.figure(figsize=(14, 6))

# Training data
plt.subplot(1, 2, 1)
plt.scatter(X_train, y_train, color='blue', label='Actual')
plt.plot(X_train, y_pred_train, color='red', label='Predicted')
plt.title('Training Data')
plt.xlabel('Median Income')
plt.ylabel('Median House Value')
plt.legend()

# Testing data
plt.subplot(1, 2, 2)
plt.scatter(X_test, y_test, color='blue', label='Actual')
plt.plot(X_test, y_pred_test, color='red', label='Predicted')
plt.title('Testing Data')
plt.xlabel('Median Income')
plt.ylabel('Median House Value')
plt.legend()

plt.show()

# Problem 3

from sklearn.datasets import fetch_california_housing
import numpy as np

class MultipleLinearRegression:
    def __init__(self):
        self.coefficients = None

    def fit(self, X, y):
        X = np.column_stack((np.ones(len(X)), X))

        self.coefficients = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)

    def predict(self, X):
        X = np.column_stack((np.ones(len(X)), X))

        y_pred = X.dot(self.coefficients)
        return y_pred

housing_data = fetch_california_housing()
X = housing_data.data
y = housing_data.target


def train_test_split(X, y, test_size=0.2):
    data = list(zip(X, y))
    np.random.shuffle(data)
    split_index = int(len(data) * (1 - test_size))
    train_data = data[:split_index]
    test_data = data[split_index:]
    X_train, y_train = zip(*train_data)
    X_test, y_test = zip(*test_data)
    return np.array(X_train), np.array(y_train), np.array(X_test), np.array(y_test)

X_train, y_train, X_test, y_test = train_test_split(X, y)


model = MultipleLinearRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


def mean_absolute_error(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

mae = mean_absolute_error(y_test, y_pred)
print("MAE:", mae)

r_squared = r2_score(y_test, y_pred)
print("R-squared using scikit-learn:", r_squared)

# Problem 4

from sklearn.datasets import fetch_california_housing
import numpy as np
import pandas as pd

# Fetch the California housing dataset
california_housing = fetch_california_housing(as_frame=True).frame

# Define the Gaussian kernel function
def gaussian_kernel(distance, bandwidth):
    return np.exp(-0.5 * (distance / bandwidth) ** 2)

# Implement Locally Weighted Linear Regression
def lwlr(prediction_point, dataset, bandwidth):
    n = dataset.shape[0]  # Number of data points in the dataset
    X = np.c_[np.ones(n), dataset.iloc[:, :-1].values]  # Add a column of ones to the features for the intercept
    y = dataset.iloc[:, -1].values.reshape(-1, 1)  # Target variable

    # Initialize weights matrix as an identity matrix
    weights = np.eye(n)

    # Calculate weights for each data point in the dataset
    for i in range(n):
        distance = np.linalg.norm(X[i, 1:] - prediction_point)
        weights[i, i] = gaussian_kernel(distance, bandwidth)

    # Calculate theta using the Normal Equation with weights
    XTX = X.T.dot(weights).dot(X)
    if np.linalg.det(XTX) == 0.0:
        print("Matrix is singular, cannot do inverse")
        return
    theta = np.linalg.inv(XTX).dot(X.T).dot(weights).dot(y)

    # Predict the value for the prediction point
    prediction = np.array([1] + list(prediction_point)).dot(theta)
    return prediction

# Example usage
bandwidth = 10  # Example bandwidth value, needs to be chosen carefully
prediction_point = california_housing.iloc[0, :-1].values  # Using the first row's features as an example
prediction = lwlr(prediction_point, california_housing, bandwidth)
print("Predicted value:", prediction)

# Example of tuning bandwidth values
bandwidth_values = [1, 5, 10, 20, 30]  # Example range of bandwidth values to test
for bandwidth in bandwidth_values:
    prediction = lwlr(prediction_point, california_housing, bandwidth)
    print(f"Bandwidth: {bandwidth}, Predicted value: {prediction}")

def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

# Select a subset of points for evaluation (for demonstration, use the first 10 points)
subset_points = california_housing.iloc[:10, :-1].values
actual_values = california_housing.iloc[:10, -1].values

predictions = []
for point in subset_points:
    pred = lwlr(point, california_housing, bandwidth)  # Choose an appropriate bandwidth
    predictions.append(pred)

# Calculate MSE
mse = mean_squared_error(actual_values, np.array(predictions).flatten())
print(f"Mean Squared Error: {mse}")

# Problem 5
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Summary of previous models' performance
performance_summary = {
    'Simple Linear Regression': {
        'Training MSE': 0.709588244777414,
        'Testing MSE': 0.667452053993711,
        'R-squared': 0.48601145971104476
    },
    'Multiple Linear Regression': {
        'MAE': 0.5334789629837159,
        'R-squared': 0.5992040333170137
    },
    'Locally Weighted Linear Regression': {
        'Mean Squared Error': 0.1854663691567629,
        'Bandwidth Effectiveness': {
            '1': -13.70056655,
            '5': 4.37338645,
            '10': 4.03573491,
            '20': 3.93911231,
            '30': 3.94211779
        }
    }
}

# Model comparison and selection
def model_selection(performance_summary):
    # consider MSE and R-squared
    best_model = None
    best_r_squared = -float('inf')  # Initialize with the lowest possible value

    for model, metrics in performance_summary.items():
        r_squared = metrics.get('R-squared')
        if r_squared and r_squared > best_r_squared:
            best_model = model
            best_r_squared = r_squared

    return best_model, best_r_squared

# Execute model selection
best_model, best_r_squared = model_selection(performance_summary)
print(f"The best model based on R-squared is: {best_model} with an R-squared of: {best_r_squared}")
