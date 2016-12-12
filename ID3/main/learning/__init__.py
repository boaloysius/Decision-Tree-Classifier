import os
import sys
ROOT_NAME="main"
ROOT_PATH=""
DS=os.path.sep
path_list= os.path.realpath(__file__).split(DS)

for name in reversed(path_list):
	if name != ROOT_NAME:
		path_list.pop()
		continue

	break

ROOT_PATH=DS.join(path_list)

sys.path.append(ROOT_PATH)

from loader import *