## File of helper functions for handling data. Copied from various common modules. 

import os
import pandas as pd
import pickle
import logging
from skafossdk import DataSourceType, Skafos
from s3fs.core import S3FileSystem  
from .schema import SCORING_SCHEMA


# Data access functions

# Input data
S3_BUCKET = "skafos.example.data"
TRAINING_FILE_NAME = "TelcoChurnData/WA_Fn-UseC_-Telco-Customer-Churn_train.csv"
SCORING_FILE_NAME = "TelcoChurnData/WA_Fn-UseC_-Telco-Customer-Churn_score.csv"

# Output models and scores
S3_PRIVATE_BUCKET = "skafos.example.output.data"
CHURN_MODEL_SCORES = "TelcoChurnData/churn_model_scores/scores.csv"
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Project Token
KEYSPACE = "91633e3d419e23dc7a2da419"


#-------------------Data Access Functions -----------------------

# Get input data from S3 -- specify training or scoring. 
def get_data(csvCols, whichData):  
    s3 = S3FileSystem(anon=True)
    if whichData == "training":
        path = f's3://{S3_BUCKET}/{TRAINING_FILE_NAME}'
    elif whichData == "scoring":
        path = f's3://{S3_BUCKET}/{SCORING_FILE_NAME}'
    # PUT ERROR CATCHING HERE FOR ERRORS IN INPUT FILES
    # Read in .csv file, but only for specified columns. 
    df = pd.read_csv(s3.open(f'{path}', mode='rb'), usecols=csvCols)
    for c in csvCols:
        if (df[c].dtype == 'object'):
            df = df[df[c].str.match(" ") == False]
    return df

def save_scores(ska, scoring, location):
    # Save to Cassandra
    if location=="both" or location=="cassandra":
        #Convert scoring data to list of objects
        scores = scoring.to_dict(orient='records')
        #Save to Cassandra
        ska.log("Saving to Cassandra", level=logging.INFO)
        ska.engine.save(SCORING_SCHEMA, scores).result()
        ska.log("Saving to Cassandra", labels=["S3saving"], level=logging.INFO)   
    #Save to S3
    if location=="both" or location=="S3":
        bytes_to_write = scoring.to_csv(None, index=False).encode()
        fs = S3FileSystem(key=AWS_ACCESS_KEY_ID, secret=AWS_SECRET_ACCESS_KEY)
        with fs.open(f"s3://{S3_PRIVATE_BUCKET}/{CHURN_MODEL_SCORES}", 'wb') as f:
                f.write(bytes_to_write)
        ska.log("Saving to S3", labels=["S3saving"], level=logging.INFO)
    
            
def save_model(ska, dataset_id, fittedModel, modelType):
    # TODO: Need to put dataset_id back into file name. Ignoring for now.  
    ska.log("Saving model to S3", labels=["S3saving"], level=logging.INFO)
    #fileName = f"dataset_id_{dataset_id}_{modelType}.pkl"
    fileName = f"{modelType}.pkl"
    filePath = f"s3://{S3_PRIVATE_BUCKET}/churn_models/{fileName}"
    print(f"{filePath}", flush=True)
    fs = S3FileSystem(key=AWS_ACCESS_KEY_ID, secret=AWS_SECRET_ACCESS_KEY)
    with fs.open(filePath, 'wb') as f:
        f.write(pickle.dumps(fittedModel))

def get_model(ska, dataset_id, modelType):
    ska.log("Getting model from S3", labels=["S3fetching"], level=logging.INFO)
    #fileName = f"dataset_id_{dataset_id}_{modelType}.pkl"
    fileName = f"{modelType}.pkl"
    filePath = f"s3://{S3_PRIVATE_BUCKET}/churn_models/{fileName}"
    print(f"{filePath}", flush=True)
    fs = S3FileSystem(key=AWS_ACCESS_KEY_ID, secret=AWS_SECRET_ACCESS_KEY)
    with fs.open(filePath, mode="rb") as f:
        return pickle.loads(f.read())
    

#-------------------Data Manipulation Functions ----------------------- 

# Convert categorical variables to dummies
def dummify_columns(xVars, features):
    for column in features:
        if (xVars[column].dtype == 'object'):
            ### HACK TO HANDLE DIRTY DATA IF TOTAL CHARGES IS SELECTED.
            if column != 'total_charges':
                dvars = pd.get_dummies(xVars[column], prefix=xVars[column].name)
                # Remove one column from dvars to handle multi-collinearity
                dvars = dvars.drop(dvars.columns[[-1,]], axis=1)
                xVars = pd.concat([xVars, dvars], axis=1)
                # Remove original non-numeric column
                xVars = xVars.drop(column, axis=1)
            elif column == 'total_charges': #DIRTY HACK Continued + dealing with pandas wonky business
                newDF = xVars['total_charges'].apply(pd.to_numeric)
                xVars = xVars.drop('total_charges', axis=1)
                xVars['total_charges'] = newDF
         
    return xVars     

