from skafossdk import *
import logging
import random
import pickle
import datetime
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

from common.data import *
from common.modeling import *

# Initialize Skafos object
ska = Skafos()

#Grab relevant features from those selected in the modeling.py file.   
features = MODEL_INPUT_FEATURES
ska.log(f"List of model input: {features}", labels=["features"], level=logging.INFO)

csvCols = features.copy()
csvCols.append(TARGET_VARIABLE) # Break into features, label, ID
csvCols.insert(0, UNIQUE_ID)

#Get data 
df = get_data(csvCols, "training")

# Split X and Y variables and convert categorial to dummy variables
xVars = dummify_columns(df[features], features)
yVar = df[TARGET_VARIABLE].apply(lambda x: 1 if x == "Yes" else 0)

# Create train/test split. 
X_train, X_test, y_train, y_test = train_test_split(xVars, yVar, random_state=10)

#Build logistic regression model
lr = LogisticRegression(C=1.0, solver='liblinear')
fittedModel = lr.fit(X_train, y_train)

# Compare predictions to actual values and calculate accuracy and ROC
y_preds = fittedModel.predict(X_test)
y_scores = [p[1] for p in fittedModel.predict_proba(X_test)]
model_accuracy = accuracy_score(y_test, y_preds)
model_auc = roc_auc_score(y_test, y_scores)
ska.log(f"Training accuracy: {model_accuracy}", labels=["Metrics"], level=logging.INFO)
ska.log(f"Training ROC_AUC: {model_auc}", labels=["Metrics"], level=logging.INFO)

# save model to Cassandra using the Skafos Data Engine
pickledModel = pickle.dumps(fittedModel)
saved_model = ska.engine.save_model(MODEL_TYPE, pickledModel, tags=[MODEL_TYPE, "latest"])
ska.log(f"Model saved to Cassandra: {saved_model} \n", labels=["model saving"], level=logging.INFO)



