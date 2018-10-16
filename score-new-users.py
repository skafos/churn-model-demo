from skafossdk import *
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

from common.data import *
from common.modeling import *

# Grab latest data and model from S3

ska = Skafos()

#Grab relevant columns from those selected from Tableau and written to Cassandra tables  
dataset_id, features = get_features(ska)
ska.log(f"List of features selected by user: {features}", labels=["features"], level=logging.INFO)

csvCols = features.copy()
csvCols.append(TARGET_VARIABLE) # Break into features, label, ID
csvCols.insert(0, UNIQUE_ID)

# Grab model
fittedModel = get_model(ska, dataset_id, MODEL_TYPE)

scoringData = get_data(csvCols, "scoring")
xToScore = dummify_columns(scoringData[features], features)
y_actual = scoringData[TARGET_VARIABLE].apply(lambda x: 1 if x == "Yes" else 0)


preds = fittedModel.predict(xToScore)
scores = [p[1] for p in fittedModel.predict_proba(xToScore)]
model_accuracy = accuracy_score(y_actual.values, preds)
model_auc = roc_auc_score(y_actual.values, scores)
ska.log(f"Scoring accuracy: {model_accuracy} \n ROC_AUC: {model_auc}", 
        labels=["Metrics"], level=logging.INFO)

#Construct scoring output
scoring = pd.DataFrame(data=scoringData[UNIQUE_ID], columns=[UNIQUE_ID])
scoring['dataset_id'] = dataset_id
scoring['score'] = [p[1] for p in fittedModel.predict_proba(xToScore)]

# output_model
# location options: Cassandra, S3, or both
save_scores(ska, scoring, "both")