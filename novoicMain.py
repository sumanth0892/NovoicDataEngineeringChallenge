import os
import numpy as np
from utils import *
import TARGETS as Ts

#Pyspark is a python based wrapper for the spark framework developed by Apache
from pyspark.sql import SparkSession
from pyspark import SparkContext,SparkConf
#The default mode is running locally using all available cores. 
#This machine has 4 cores.
conf = SparkConf().setAppName('local').setMaster('local')
sc = SparkContext(conf = conf)

#Let us ignore the warnings temporarily
import warnings
warnings.filterwarnings('ignore')

#For each path
if __name__ == '__main__':
	#Data can also be passed as inputs
	metaFile = '' #Replace with the appropriate path for the metadata
	textPath = '' #Replace with the appropriate path for the conversations
	audioPath = '' #Replace with the appropriate path for the audio files. 
	audioFiles = []; textFiles = [] #Lists to store file paths 
	for fFile,fAudio in zip(sorted(os.listdir(textPath)),sorted(os.listdir(audioPath))):
		textFiles.append(os.path.join(textPath,fFile))
		audioFiles.append(os.path.join(audioPath,fAudio))
	
	#Create a Spark session to start the process. Only one spark session can be run at a time
	spark = SparkSession(sc)

	#Run processing tasks in parallel
	Audio = spark.sparkContext.parallelize(audioFiles)
	Text = spark.sparkContext.parallelize(textFiles)

	#Audio and text features here
	#Spark has two processes, Map and Reduce.
	#We can map functions from different modules to transform the files
	audioFeatures = np.array(Audio.map(audio_to_features).collect())
	textFeatures = np.array(Text.map(text_to_features).collect())

	#Get the metadata dataframe
	metaDF = spark.read.csv(metaFile)
	metaData = metaDF.collect() #Get all the data
	columnHeaders = metaData.pop(0) #Get the relevant info to process the targets
	#Now, parallelize the instances and get targets for different datasets
	targets = Ts.targets()
	data = spark.sparkContext.parallelize(metaData)
	target = np.array(data.map(targets.default).collect())
	targetsMMSE = np.array(data.map(targets.MMSE).collect())
	targetsAMDCI = np.array(data.map(targets.AMDCI).collect())
	targetsPreClinical = np.array(data.map(targets.preClinical).collect())
	target = np.reshape(target,(len(target),1))
	targetsMMSE = np.reshape(targetsMMSE,(len(targetsMMSE),1))
	targetsAMDCI = np.reshape(targetsAMDCI,(len(targetsAMDCI),1))
	targetsPreClinical = np.reshape(targetsPreClinical,(len(targetsPreClinical),1))
	print(targetsAMDCI.shape)
	print(audioFeatures.shape)

	#Create the datasets
	DSAudio = np.append(audioFeatures,target,axis = 1)
	DSAudioMMSE = np.append(audioFeatures,targetsMMSE,axis = 1)
	DSAudioAMDCI = np.append(audioFeatures,targetsAMDCI,axis = 1)
	DSAudioPreClinical = np.append(audioFeatures,targetsPreClinical,axis = 1)
	DSText = np.append(textFeatures,target,axis = 1)
	DSTextMMSE = np.append(textFeatures,targetsMMSE,axis = 1)
	DSTextAMDCI = np.append(textFeatures,targetsAMDCI,axis = 1)
	DSTextPreClinical = np.append(textFeatures,targetsPreClinical,axis = 1)

	#Save as a csv file with the last column as a target
	np.savetxt("audioDataset.csv",DSAudio, delimiter=",")
	np.savetxt("MMSEDataset.csv",DSAudioMMSE, delimiter=",")
	np.savetxt("AMDCIDataset.csv",DSAudioAMDCI, delimiter=",")
	np.savetxt("preClinicalDatasetAudio.csv",DSAudioPreClinical, delimiter=",")
	np.savetxt("textDataset.csv",DSText, delimiter=",")
	np.savetxt("DSTextMMSEDataset.csv",DSTextMMSE, delimiter=",")
	np.savetxt("DSTextAMDCI.csv",DSTextAMDCI, delimiter=",")
	np.savetxt("DSTextPreClinical.csv",DSTextPreClinical, delimiter=",")
	#We can also write methods to store the datasets in a BigQuery database on Google Cloud Storage.






