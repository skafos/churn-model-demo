# Modeling parameters for this job. 
# These can be modified to adjust the model

TARGET_VARIABLE = 'churn'
UNIQUE_ID = 'customer_id'
MODEL_INPUT_FEATURES = ['internet_service', 'monthly_charges', 'tenure', 'dependents', 'total_charges']
MODEL_TYPE = "LogisticRegression" 