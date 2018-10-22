# Predictive Modeling Using Skafos

## Introduction

The purpose of this example is to highlight the utility of Skafos, Metis Machine's data science operationalization and delivery platform. In this example, we will: 

* Build and train a model predicting cell phone churn with data on a public S3 bucket
* Save this model to a private S3 bucket
* Score new customers using this model and save these scores.
* Access these scores via a generated API and S3. 

## Functional Architecture + Code

The figure below provides a functional architecture, linking each piece to the code found in [churn-model-demo](https://github.com/skafos/churn-model-demo) on github.  

TODO: Include functional architecture

## Pre-requisites

1. [Sign up](https://dashboard.metismachine.io/sign-up) for a Skafos account
2. [Install skafos on your machine](https://docs.metismachine.io/docs/installation)
3. Authenticate your account via the `skafos auth` command.
4. A working knowledge of how to use git. 

## Input Data

The source data for this example is available in a public S3 bucket provided by Metis Machine. _In the steps below, we will describe how to access it. No code modifications are required to access the input data._

This data has been slightly modified from its source, which is freely available and can be found [here](https://www.ibm.com/communities/analytics/watson-analytics-blog/predictive-insights-in-the-telco-customer-churn-data-set/) or [here](https://www.kaggle.com/blastchar/telco-customer-churn/home). 

## Tutorial

In the following step-by-step guide, we will walk you through how to use the code in this repository to run a job on Skafos. Following completion of this tutorial, you should be able to: 

1. Run the existing code and access its output on S3.
2. Replace the provided data and model with your own data and model. 

### Step 1: Fork or clone the repo 

1. Clone the [churn-model-demo](https://github.com/skafos/churn-model-demo) from github. This code is freely available as part of the Skafos organization. Note that the README is a copy of these instructions. 
2. Create your own remote on github for this repo, in the usual fashion, so you can push code changes.  


### Step 2: Examine `metis.config.yml.example`

Each Skafos project will need its own project token and unique `metis.config.yml` file. The example `metis.config.yml.example` provided in this repo is the identical to what you will need, but the project token and job ids are tied to another Skafos account and organization. 

Creating your own `metis.config.yml` file is simple and described below. 

### Step 3: Initialize your own Skafos project 

Once in the working directory of this project, type: `skafos init` on the command line. This will generate a new `metis.config.yml` file that is tied to your Skafos account and organization. 

Open up this config file and edit the first job id to match the example .yml file included in the repo. Specifically, modify the following: 

``` yaml
language: python
name: build-churn model 
entrypoint: build-churn-model.py
```

**Note: Do _not_ edit the project token or job_ids in the .yml file. Otherwise, Skafos will not recognize and run your job.** 

### Step 4: Add a second job to your Skafos project and `metis.config.yml`

In the example `metis.config.yml` file, you'll not that there are two jobs: one to build a model, and one to score new users. You will need to add a second job to your Skafos project via the following command on the command line: 

` skafos create job score-new-users --project <insert-your-project-token-here>`

This will output a job_id on the command line. Copy this job id to your `metis.config.yml` file, again using the example yaml file as a template, and including the following:

``` yaml
language: python 
name: score-new-users`
entrypoint: score-new-users.py`
dependencies: [<job-id for build-churn-model.py>]
```

This dependency will ensure that new users are not scored until the churn model has been built. If `build-churn-model.py` does not complete, then `score-new-users.py` will not run. 

### Step 5: Add `metis.config.yml` to your repo

Now that your `metis.config.yml` file has all the necessary components, add it to the repo, commit, and push.  

### Step 6: Add Skafos to the github repo
In Steps 3 and 4 above, you initialized a Skafos project so you can run the cloned repo in Skafos. Now, you will need to [add the Skafos app](https://github.com/apps/skafos) to your github repository. 

To do this, navigate to the Settings page for your organization, click on _Installed GitHub Apps_ to add the Skafos app to this repository. Alternatively, if this repo is not part of an organization, navigate to your _Settings_ page, click on _Applications_, and install the Skafos app. 

### Step 7: Modify the AWS Keys and Private S3 bucket

In [`common/data.py`](https://github.com/skafos/churn-model-demo/blob/master/common/data.py), the AWS information to retrieve input data and store output models and data is provided. The input S3 bucket and file names do not need to be modified; however, the [location of the output models and scores](https://github.com/skafos/churn-model-demo/blob/master/common/data.py#L19) will need to be updated in the code, as well as the specified keyspace.

To make these changes, do the following: 

1. Create a private S3 bucket to save your output models and scores. This bucket will replace the existing value for `S3_PRIVATE_BUCKET` in the code. 
2. You will need to provide Skafos with your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` [via the command line](https://docs.metismachine.io/docs/usage#section-setting-environment-variables). `skafos env AWS_ACCESS_KEY_ID --set <key>` and `skafos env AWS_SECRET_ACCESS_KEY --set <key>` will do this. 
3. Update the [`KEYSPACE`](https://github.com/skafos/churn-model-demo/blob/master/common/data.py#L26) to be the `project_token` that was generated with the `metis.config.yml` file. 

### Step 8: Commit and Push All Code Changes to the github repo

In step 7, you generated several changes to `common/data.py.` These changes now need to be pushed to github. In doing so, the Skafos app will pick them up and run both the training and scoring jobs. 

### Step 9: Monitor your jobs

Navigate to [dashboard.metismachine.io](https://dashboard.metismachine.io/) to monitor the status of the job you just pushed. Additional documentation about how to use the dashboard can be found [here](https://docs.metismachine.io/docs/dashboard)

### Additional Steps to Document:

* Checking status on S3 bucket.
* Using API with Cassandra to grab results
* Which pieces of code to modify to use alternate data. 





 


