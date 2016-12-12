
# Written by Boby Aloysius Johnson
# last modified 10th July 2016

from __init__ import *

# @param
#	file 	 : string          (name of the file)
#	metadata : integer or None (header of data is present in which row)
# @return
#	data 	 : Panda DataFrame

def DataRetrival(file,metadata=0):
	data=pd.read_csv(ROOT_PATH+DS+file,header=metadata)
	return data

 

