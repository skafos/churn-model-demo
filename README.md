# Predictive Model Example Using Skafos

## Introduction

The purpose of this example is to highlight the utility of Skafos, Metis Machine's data science operationalization and delivery platform. In this example, we will: 

* Build and train a model predicting cell phone churn with data on a public S3 bucket
* Save this model to a private S3 bucket
* Score new customers using this model and save these scores.
* Access these scores via a generated API. 

 ## Pre-requisites

 * Sign up for a Skafos account

 ## Data

The source data for this example is available in a public S3 bucket provided by Metis Machine. _In the steps below, we will describe how to access it. No code modifications are required._

This data has been slightly modified from its source, which is freely available and can be found [here](https://www.ibm.com/communities/analytics/watson-analytics-blog/predictive-insights-in-the-telco-customer-churn-data-set/) or [here](https://www.kaggle.com/blastchar/telco-customer-churn/home). 



