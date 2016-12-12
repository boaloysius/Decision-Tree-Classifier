from __init__ import *
from learning.classification.DecisionTree import DecisionTree
from dataFormating.DataRetrival import *
import json_print

def main():
	clf=DecisionTree()
	training_data=DataRetrival(file="database/mixed/train_mixed.csv")

	print '\n\n'+'Training Dataset: '
	print training_data
	
	class_label = "class"
	class_values = training_data[class_label]
	training_data.drop(class_label,axis=1,inplace=True)

	# Inputs to classifier
	#   data         : Panda DataFrame (Training Data)
    #   class_values : Panda Series (Training values)
    #   preference   : string if metadata is not None else integer ( Attribute prefered as root )
    #   max_height   : integer > 0 
    
	tree = clf.train(data=training_data,class_values=class_values,max_height=2)
	
	# You can print the tree. It is in json format. 
	print '\n\n'+'Tree: '
	json_print.print_tree(tree)

	test_set = pd.DataFrame(columns = training_data.columns)
	test_set.loc[0] = ["sunny","mild",7,'False']
	test_set.loc[1] = ["rainy","mild",4,'True']
	test_set.loc[2] = ["overcast","cool",4,'False']
	
	print '\n\n'+'Testing Data: '
	print test_set
	
	print '\n\n'+'Predicted values'
	print clf.predict(clf.tree,test_set)

main()
