<p align="center"><a href="https://novoic.com"><img src="https://assets.novoic.com/logo_320px.png" alt="Novoic logo" width="160"/></a></p>

# Novoic data engineering challenge
This pipeline is used to create datasets to classify Alzheimer's disease in various ways such as:
Classification of AD (Alzheimer's disease; status = 1) vs HC (healthy control, i.e. status = 0).
Classification of AD-MCI (mild cognitive impairment due to Alzheimer's disease; status = 1 AND mmse > 26) vs HC.
Classification of AD vs HC for patients in a certain age range. For example classification of AD vs HC for patients who are less than 60 years old (a loose proxy for preclinical Alzheimer’s).
Classification of AD vs HC based on Mini-Mental State Examination (MMSE) scores where ranges describe different progression of disease, starting from No Dementia to Severe Dementia (A score of MMSE less than 13):
Target 0: MMSE score of >24 -> No Dementia
Target 1: MMSE score between 20 and 24 -> Mild Dementia
Target 2: MMSE score between 13 and 20 -> Moderate Dementia
Target 3: MMSE score less than 13 -> Severe Dementia
The feature set is created using both sound and audio for different types of targets shown above to build differnet products. 

Files:
utils.py -> Has two functions to convert text (.xml) and audio (.wav) files to features of (96x1) length arrays. 
TARGETS.py -> A class to process targets into different datasets.

Frameworks and Languages:
The main language used to program this is Python using Spark framework. Pyspark is a wrapper for Spark which is used for distributed data processing. 
Spark has replaced Hadoop in terms of popularity due to a few advantages:
Default spark object is in SQL mode which makes it easier for business applications. 
Faster data processing (up to 100 times in RAM and 10 times in Storage)
Spark's Resilient Distributed Datasets (RDD) makes it faster to process data repeatedly.
Spark is far better suited for real-time data processing and makes for good streaming applications and we can get business value using Time series data. Refer to the section below on "Streaming data/architecture".
Machine learning libraries and modules in Spark including functions such as Regression. 
When we need to combine huge datasets, Spark is faster even though Hadoop is better if shuffling and sorting is needed. 

Finally, please zip your preprocessed dataset and include it in the repo for convenience. Alternatively, feel free to upload it to Google Drive or S3 and share it separately with jack@novoic.com. You are free to pick the output dataset format which you believe to be best suited for downstream applications.


How would you deploy this repository on a Kubernetes cluster?
Deploying this repository on a Kubernetes cluster.
There are a couple of ways we can deploy an application on a Kubernetes cluster. 
Quite simply, we can use Humanitec (https://humanitec.com/deploy-from-github-to-kubernetes) and use its API with UI to deploy a repo to a Kubernetes cluster. 
Step 1: Using GitHub, login to the Humanitec UI. GitHub builds container images from our repositories.
Step 2: View the images and select the ones to be deployed as an application to a Kubernetes cluster. 
Any application can be deployed to Kubernetes using the following steps:
1. Build the Docker image
2. Deploy the application:
    Account Settings -> Integrations -> Configure
    Then, Add New Service -> Deploy
    Specify the parameters of the service/application
3. Finally, automate the deployment using pipelines. 


Assume we now are using this repository as part of a product that we have deployed. How would you ensure that we can stream the data preprocessing? What technologies would you use? 
Streaming the data preprocessing/architecture:
A streaming data architecture is a framework of software components built to ingest and process large volumes of streaming data from multiple sources.
Traditional methods have focused on processing data in batches while streaming data architecture focuses on immediately ingesting and processing the data and store them. The main challenge is the presence/absence of a Schema to attach a framework and sort the data that's coming in. Stream processing is a complex challenge rarely solved with a single database or ETL tool – hence the need to ‘architect’ a solution consisting of multiple building blocks.
The two main advantages of streaming architecture is that it helps in detecting Time series patterns and allows for data scalability. The first advantage is easily explained by the fact that we get real-time data and can be analyzed to make decisions. The second advantage is an even bigger boon since a large batch can break the system (if the hardware doesn't support it) while the system can easily handle smaller streams. 
The standard components of a stream processing architecture are The message broker/stream processor (converts data into a standard message format and sends it), batch-processing ETL tools, Analytics Engine and storage. 
Some of the technologies we can use, in reverse order are:
Database/Data warehouse such as Amazon Redshift
Analytics engine to make sense of the data - Amazon provides excellent tools such as ElasticSearch and Amazon RedShift
ETL tools - These process the data that's coming in and structures them. Apache Spark streaming provides good options here. 
Message broker - Use Apache Kafka here which is a hyper-performant messaging platform. 
We can ensure stream processing by making sure that the system handles small bits of new data coming in. To get more value out of it, we can form a rough schema in the analytics engine to quickly process and store it. 
Apache Flink is also another option here. 
