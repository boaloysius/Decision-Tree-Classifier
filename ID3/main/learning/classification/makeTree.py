from __init__ import *
from copy import deepcopy
import sys
import math
import numpy as np
import pandas as pd

DEBUG=False

# @param
#   class_values:
#       type : Panda Series
# @return
#   entropy:
#       type : number
#
# Calculates the entropy of the given data set for the target attr

def entropy(class_values):
    etpy = 0.0
    # norm_list contains fractional frequency of each distinct value in class_values as list 
    norm_list = class_values.value_counts(normalize=True).tolist()
    # Iterating over norm_list to calculate entropy
    for p in norm_list:
        etpy += (-p * (math.log(p, 2))) 
    return etpy

# @param
#   data:
#       type : Panda DataFrame
#   class_values :
#       type : Panda Series
#   attribute :
#       type : String
# @return 
#   best:
#       type : dictionaty
#       keys : ["entropy","value"]
#               entropy (type number)
#               split_value (info : attribute value to split the dataset on) 
#
# To find the best split point for numerical attributes

def subEntropyFloat(data,class_values,attribute):
    # Assigns default value to best
    best = { 
            "split_entropy":99999
            }
    # For each distict value in the attribute column calculate the entropy and compare to the best entropy        
    for value in data[attribute].unique():
        # truth series is a list of boolean indicating cell value <= iteration value
        truth_series = data[attribute] <= value
        # p = Probability of values <= iteration value 
        p=truth_series.value_counts(normalize=True)[True]
        # cv1 = class_values following truth_series
        cv1 = class_values[truth_series]
        cv2 = class_values[-truth_series]
        # Calculating sub entropy for value
        sub_entropy = p*entropy(cv1)+(1-p)*entropy(cv1)
        # Replacing best if new entrop is lesser that best
        if sub_entropy < best["split_entropy"]:
            best["split_entropy"] = sub_entropy
            best["split_value"] = value

    return best

# @param
#   data:
#       type : Panda DataFrame
#   class_values :
#       type : Panda Series
#   attribute :
#       type : String
# @return 
#   entropy:
#       type : dict
#       keys : split_entropy
#
# To find entropy of an attribute split of data

def subEntropyChar(data,class_values,attribute):
    # Initialising entropy as 0
    etpy = {"split_entropy":0} 
    # For each distinct attribute value find sub entropy and add main entropy
    for name,fraction in data[attribute].value_counts(normalize=True).to_dict().iteritems():
        # Making truth list for the value
        truth_list = data[attribute] == name
        etpy["split_entropy"] += fraction * entropy(class_values[truth_list])
    return etpy

# @param
#   data:
#       type : Panda DataFrame
#   class_values :
#       type : Panda Series
# @return
#   best:
#       type : dictionary
#       keys : ["name","type","split_entropy","tree_entropy","tree_gain"]
#
# Choose best attibute to split

def chooseAttr(data,class_values):
    
    # Initialising best    
    best={
            "name":"temp",
            "split_entropy":999999
         }

    # DataFrame.dtype.to_dict() returns a dictionary having keys as attribute name and value as attribute type 
    for name,dtype in data.dtypes.to_dict().iteritems():
        attr={"name":name,"type":dtype}
        # If data_type is not number, use subEntropyChar
        # Keys returned by subEntropyChar ["split_entropy"]
        if dtype in np.sctypes["others"] :
            attr.update(subEntropyChar(data,class_values, name)) 
        # If data_type is number, use subEntropyFloat
        # Keys returned by subEntropyFloat ["split_entropy","split_value"]
        else:
            attr.update(subEntropyFloat(data,class_values, name))

        if attr["split_entropy"] < best["split_entropy"]:
            best = attr


    best["tree_entropy"] = entropy(class_values)
    best["gain"] = best["tree_entropy"] - best["split_entropy"]
    
    return best

def set_preference(data,class_values,preference):

    preference = {
        "name":preference,
        "type":data[preference].dtype,
    }

    preference["tree_entropy"] = entropy(class_values.copy())

    if preference["type"] in np.sctypes["others"] :
        preference.update(subEntropyChar(data.copy(),class_values.copy(), preference["name"]))

    else:
        preference.update(subEntropyFloat(data.copy(),class_values.copy(),preference["name"]))

    preference["gain"] = preference["tree_entropy"] - preference["split_entropy"]    

    return preference
        
# @param
# 	kwargs:
#   	data        : Panda DataFrame
#   	class_label : string if metadata is not None else integer
#   	preference  : string if metadata is not None else integer ( Attribute prefered as root )
#   	max_height  : integer > 0 
#
#	recursion: interger used to keep track of height
#   @return
#       tree : (type dictionary)
#       {
#           "info" : @node (type : dictionary)
#                attribute keys:["name","type","index","gain","sub_entropy","tree_entropy","gain","height"]
#                optional: ["split_value"]
#
#                @leaf
#                   attribute keys:["class","tree_entropy","height"]
#       } 

def makeTree(kwargs={},recursion=0):
    # Checks if variables are present else set default values or print error
    data,class_values,preference,max_height = set_var(kwargs)

    # Debug display. Set global variable DEBUG to True to see data division 
    debug_display(recursion,"recursion="+str(recursion),pd.concat([data,class_values],axis=1))


    # Creating fresh node
    node={}
    node['height']=recursion


    # If all values of class_values are the same, class is found and we have reached leaf node. 
    if len(class_values.unique()) == 1:
        node["class"]=class_values.max()
        node["tree_entropy"] = 0        
 
        debug_display(recursion,"class="+node["class"]," ")
 
        return node

    # If data is empty or max height is reached , we reached leaf and return the most frequent value of class_values
    elif data.empty or recursion == max_height:    
        node["class"]=class_values.max()
        node["tree_entropy"]= entropy(class_values.copy())
 
        debug_display(recursion,"class="+node["class"]," ")
 
        return node

    # If not leaf then
    else:
        # If preference is set, the variable best is set as preference
        if preference:
            best=set_preference(data,class_values,preference)
        else:
            # else choosing attribute best
            best= chooseAttr(data.copy(),class_values.copy())

        # Setting tree nodes

        node['info']=best
        node['children']={}    

        if "split_value" in best.keys():
            debug_display(recursion,best["name"]+"="+str(best["split_value"])," ")
        else:
            debug_display(recursion,best["name"]," ")

        recursion += 1 

        # Setting child nodes

        if(best["type"] in np.sctypes["others"]):
            sub={}
            for val in data[best["name"]].unique():
                truth_series = data[best["name"]]==val
                
                sub ={
                        "data":data[truth_series].copy(),
                        "class_values":class_values[truth_series].copy(),
                        "max_height":max_height,
                    }        
                
                if best["type"] in np.sctypes["others"]:
                    sub["data"].drop(best["name"],axis=1,inplace=True)
                elif not best["split_entropy"]:
                    data.drop(best["name"],axis=1,inplace=True)
        

                node['children'][str(val)] = makeTree(sub,recursion)                

        else:

            truth_series = data[best["name"]]<=best["split_value"]
            
            sub1 ={
                    "data":data[truth_series].copy(),
                    "class_values":class_values[truth_series].copy(),
                    "max_height":max_height,
                }

            sub2 ={
                    "data":data[-truth_series].copy(),
                    "class_values":class_values[-truth_series].copy(),
                    "max_height":max_height,
                }

            if best["type"] in np.sctypes["others"]:
                sub1["data"].drop(best["name"],axis=1,inplace=True)
                sub2["data"].drop(best["name"],axis=1,inplace=True)                
            elif not best["split_entropy"]:
                sub1["data"].drop(best["name"],axis=1,inplace=True)
                sub2["data"].drop(best["name"],axis=1,inplace=True)

            node['children']["lesser"] = makeTree(sub1,recursion)
            node['children']["greater"] = makeTree(sub2,recursion)


    return node

def debug_display(space=0,*args):

    global DEBUG
    if DEBUG:
        for item in args:
            if isinstance(item,pd.DataFrame):
                for index,row in item.iterrows():
                    for i in range(space):
                        print "\t",
                    print index,row.tolist()
            else:
                for i in range(space):
                    print "\t",
                print item

def set_var(kwargs):

    error={
        "missing":"not found"
    }

    check={
        "data":{
            "index":0,
            "mising_type":"mandatory",
        },
        "class_values":{
            "index":1,
            "missing_type":"mandatory",
        },
        "preference":{
            "index":2,       
            "missing_type":"ok",
            "default":None,
        },
        "max_height":{
            "index":3,
            "missing_type":"ok",
            "default":10000
        }
    }

    return_list=[0 for x in range(len(check))]

    keys = kwargs.keys()

    for var,meta in check.iteritems():
        if var in keys:
            return_list[meta["index"]] = kwargs[var]
        elif meta["missing_type"] == "mandatory":
            print "Make Tree error: "+var+" not found"
            sys.exit(0)
        elif meta["missing_type"] == "ok":
            return_list[meta["index"]]=meta["default"]
        else:
            print "Make Tree error: Unknown missing type"
            sys.exit(0)

    return tuple(return_list)




