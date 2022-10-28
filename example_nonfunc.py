# from https://pythonexamples.org/run.php?pgm=import+numpy+as+np%0A%0Aa+%3D+3+%0Ab+%3D+4%0Aoutput+%3D+np.dot%28a%2Cb%29%0Aprint%28output%29

'''
This file services as an example of liner operation

'''

import numpy as np
import torch

#nncp np array
val1=np.array([[1, 2], [3, 4]])

val2=val1[:, 2]

#nncp np array
val3=np.array([[5, 6], [-2, 4]])

val4=val1*val3
