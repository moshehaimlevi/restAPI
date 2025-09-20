from fastapi import FastAPI, Query
from sklearn.linear_model import LogisticRegression
import numpy as np
import math
from starlette.responses import HTMLResponse

app = FastAPI(title="Logistic Regression")

# Data
X_data = np.array([18, 22, 25, 30, 35, 40, 45, 50, 55, 60]).reshape(-1, 1)
y_data = np.array([0, 0, 0, 1, 1, 1, 1, 1, 1, 1])  # Changed values

# model training
model = LogisticRegression(solver='liblinear')
model.fit(X_data, y_data)

#coefficients
b0 = model.intercept_[0]
b1 = model.coef_[0][0]

# Sigmoid function
def predict_probability(x: float) -> float:
    z = b0 + b1 * x
    return 1 / (1 + math.exp(-z))


######### API Endpoints ###########

@app.get("/logistic/predict")
def get_logistic_prediction(x: float = Query(..., description="Input value")):
    prob = predict_probability(x)
    return {
        "x": x,
        "probability": round(prob, 4)
    }

@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <html>
        <head><title>Logistic Regression</title></head>
        <body>
            <h1>Logistic Regression Demo </h1>
            <p>Trained with custom data:</p>
            <p><b>X:</b> {X_data.flatten().tolist()}</p>
            <p><b>y:</b> {y_data.tolist()}</p>
            <a href="/logistic/predict?x=30">Try /logistic/predict?x=30</a>
        </body>
    </html>
    """