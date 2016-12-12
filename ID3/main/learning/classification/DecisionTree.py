# Written by Boby Aloysius Johnson
# Last modified 12th June 2016
# Main external file used  :
#   DataRetrival.py : For retriving data class_values and attribute from csv file
#   makeTree : Contains main function to make decision tree given data ,class_values and attributes
from __init__ import *
from dataFormating.DataRetrival import DataRetrival
from makeTree import makeTree

class DecisionTree():
    def __init__(self):
        # Details of Decision Tree are stored in a dictionary called info 
        # Data type:
        #   data         : Panda DataFrame (Training Data)
        #   class_values : Panda Series (Training values)
        #   preference   : string if metadata is not None else integer ( Attribute prefered as root )
        #   max_height   : integer > 0 

        self.info={
                    "data":pd.DataFrame(),
                    "class_values":pd.Series(),
                    "preference":None,
                    "max_height":100,
                }

        #   tree :
        #   {
        #       "info" : @node (type : dictionary)
        #                attribute keys:["name","type","index","gain","sub_entropy","tree_entropy","gain","height"]
        #                optional: ["split_value"]
        #
        #                @leaf
        #                   attribute keys:["class","tree_entropy","height"]
        #   }        

        self.tree={}

    #   Training function
    #   @param
    #       kwargs (type : dictionary)
    #              (caution : Need to fill atleast data and class_label before training)
    #   @return 
    #       decision tree ( type:dictionary )

    def train(self,**kwargs):
        self.info.update(kwargs)        
        # Checking for input errors
        self.trainInputErrors(self.info)
        self.tree=makeTree(deepcopy(self.info))
        return self.tree

    # Function to detect train input error
    # @param:
    #   kwargs : {type : dictionary}

    def trainInputErrors(self,kwargs):
        # Checking if data is Panda Data Frame
        if not isinstance(self.info["data"],pd.DataFrame):
            print "Data must be panda DataFrame"
            sys.exit(0)

        # Checking if data is Panda Data Frame
        if not isinstance(self.info["class_values"],pd.Series):
            print "Data must be panda Series"
            sys.exit(0)

    # Function to predict class_values for data with multiple rows
    # @param
    #   tree {type : json}
    #   data {type : pandas DataFrame}
    # @return 
    #   class_value {type : np.array}

    def predict(self,tree,data):
        prediction=[]
        for index,row in data.iterrows():
            prediction.append(self.predict_single(self.tree,row)) 
    
        return np.array(prediction)

    # Function to predict class_values for data with multiple rows
    # @param
    #   tree {type : json}
    #   row {type : pandas Series}
    # @return 
    #   class_value {type : string}

    def predict_single(self,tree,row):
        # If the current pointing node have attribute class it is a leaf
        if "class" in tree.keys():
            return tree["class"]         
        else:
            split_attr = tree["info"]["name"]
            attr_value   = row[split_attr]
            dtype       = tree["info"]["type"]
            # check if split attribute is int or char
            if dtype in np.sctypes["others"] :
                # Find the value of split attribute in the row and take corresponding path 
                # ie, child having that as key
                if attr_value in tree["children"].keys():
                    return self.predict_single(tree["children"][attr_value],row)
                else:
                    print tree["children"].keys()
                    # If no corresponding key found then return None
                    return np.nan
            else:                
                #Check if value is greater or less than split_value and take the branch
                split_value = tree["info"]["split_value"]
                if attr_value <= split_value:
                    return self.predict_single(tree["children"]["lesser"],row)
                else:
                    return self.predict_single(tree["children"]["greater"],row)


