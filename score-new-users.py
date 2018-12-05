from skafossdk import *
import logging
import random
import datetime
import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

from common.data import *
from common.modeling import *
from common.schema import *


ska = Skafos()

#Grab relevant features from those selected in the modeling.py file. 
features = MODEL_INPUT_FEATURES
ska.log(f"List of model input: {features}", labels=["features"], level=logging.INFO)

csvCols = features.copy()
csvCols.append(TARGET_VARIABLE) # Break into features, label, ID
csvCols.insert(0, UNIQUE_ID)

# Get model that was previously saved in Cassandra using latest tag. 
pickledModel = ska.engine.load_model(MODEL_TYPE, tag="latest").result()
model_id = int(pickledModel['meta']['version'])
fittedModel = pickle.loads(pickledModel['data'])

scoringData = get_data(csvCols, "scoring")
xToScore = dummify_columns(scoringData[features], features)
y_actual = scoringData[TARGET_VARIABLE].apply(lambda x: 1 if x == "Yes" else 0)

# Predict and score users
preds = fittedModel.predict(xToScore)
pctOnes = np.sum(preds)/len(preds)
pctZeros = 1 - pctOnes
scores = [p[1] for p in fittedModel.predict_proba(xToScore)]
model_accuracy = accuracy_score(y_actual.values, preds)
model_auc = roc_auc_score(y_actual.values, scores)
ska.log(f"Scoring accuracy: {model_accuracy} \n ROC_AUC: {model_auc}", 
        labels=["Metrics"], level=logging.INFO)

#Construct scoring output
scoring = pd.DataFrame(data=scoringData[UNIQUE_ID], columns=[UNIQUE_ID])
scoring['model_id'] = model_id
scoring['score'] = [p[1] for p in fittedModel.predict_proba(xToScore)]

# Construct metric output to keep across runs
metrics=[{'model_id': model_id, 
          'run_time': datetime.datetime.now(),
          'accuracy': model_accuracy,
          'pct_zeros': pctZeros,
          'pct_ones': pctOnes}]

# Save scores and metrics to Cassandra
# location options: Cassandra, S3, or both
save_data(ska, scoring, SCORING_SCHEMA, "Cassandra")
save_data(ska, metrics, METRIC_SCHEMA, "Cassandra")

# Here is where we will re-import metrics for scoring
