# Predictive Modeling Using Skafos

## Introduction

The purpose of this example is to highlight the utility of Skafos, Metis Machine's data science operationalization and delivery platform. In this example, we will: 

* Build and train a model predicting cell phone churn with data on a public S3 bucket
* Save this model to a private S3 bucket
* Score new customers using this model and save these scores.
* Access these scores via a generated API and S3. 

## Pre-requisites

1. [Sign up](https://dashboard.metismachine.io/sign-up) for a Skafos account
2. [Install skafos on your machine](https://docs.metismachine.io/docs/installation)
3. Authenticate your account via the `skafos auth` command.

## Input Data

The source data for this example is available in a public S3 bucket provided by Metis Machine. _In the steps below, we will describe how to access it. No code modifications to the input data are required to run this model._

This data has been slightly modified from its source, which is freely available and can be found [here](https://www.ibm.com/communities/analytics/watson-analytics-blog/predictive-insights-in-the-telco-customer-churn-data-set/) or [here](https://www.kaggle.com/blastchar/telco-customer-churn/home). 

## Tutorial

In the following step-by-step guide, we will walk you through how to use the code in this repository to run a job on Skafos. Following completion of this tutorial, you should also be able to replace the provided data and model with your own data and model. 

### Step 1: Fork or clone the repo 

1. Clone the [churn-model-demo](https://github.com/skafos/churn-model-demo) from github. This code is freely available as part of the Skafos organization. Note that the README is a copy of these instructions. 
2. Create your own remote on github for this repo, in the usual fashion, so you can push code changes.  


### Step 2: Delete or rename `metis.config.yml`

Each Skafos project will need its own project token and unique `metis.config.yml` file. The example `metis.config.yml` provided in this repo is the identical to what you will need, but the project token and job ids are tied to another Skafos account and organization. Creating your own `metis.config.yml` file is simple and described below. 

### Step 3: Initialize your own Skafos project 

Once in the working directory of this project, type: `skafos init` on the command line. This will generate a new `metis.config.yml` file that is tied to your Skafos account and organization. 

Open up this config file and edit the first job id to match the example .yml file included in the repo. Specifically, modify the following: 

> `language: python` 
> 
> `name: build-churn model`
> 
> `entrypoint: build-churn-model.py`

**Note: Do _not_ edit the project token or job_ids in the .yml file. Otherwise, Skafos will not recognize and run your job.** 

### Step 4: Add a second job to your Skafos project and `metis.config.yml`

In the example `metis.config.yml` file, you'll not that there are two jobs: one to build a model, and one to score new users. You will need to add a second job to your Skafos project via the following command on the command line: 

` skafos create job score-new-users --project <insert-your-project-token-here>`

This will output a job_id on the command line. Copy this job id to your `metis.config.yml` file, again using the example yaml file as a template, and including the following:

> `language: python` 
> 
> `name: score-new-users`
> 
> `entrypoint: score-new-users.py`
> 
> `dependencies: [<job-id for build-churn-model.py>]`

This dependency will ensure that new users are not scored until the churn model has been built. If `build-churn-model.py` does not complete, then `score-new-users.py` will not run. 

### Step 5: Add Skafos to the github repo

### Step 6: Modify the AWS Keys and Private S3 bucket

 


