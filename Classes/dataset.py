import numpy as np
import scipy
import scipy.io as sio

from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
# from sklearn.preprocessing import Imputer


class Dataset:
    
    def __init__(self):
        
        # each dataset will have training and test data with labels
        self.trainData = np.array([[]])
        self.trainLabels = np.array([[]])
        self.testData = np.array([[]])
        self.testLabels = np.array([[]])
        
    def setStartState(self, nStart):
        ''' This functions initialises fields indicesKnown and indicesUnknown which contain the indices of labelled and unlabeled datapoints
        Input:
        nStart -- number of labelled datapoints (size of indicesKnown)
        '''
        
        self.nStart = nStart
        # first get 1 positive and 1 negative point so that both classes are represented and initial classifer could be trained.
        cl1 = np.nonzero(self.trainLabels==1)[0]
        indices1 = np.random.permutation(cl1)
        self.indicesKnown = np.array([indices1[0]]);
        cl2 = np.nonzero(self.trainLabels==0)[0]
        indices2 = np.random.permutation(cl2)
        self.indicesKnown = np.concatenate(([self.indicesKnown, np.array([indices2[0]])]));
        # combine all the rest of the indices that have not been sampled yet
        indicesRestAll = np.concatenate(([indices1[1:], indices2[1:]]));
        # permute them
        indicesRestAll = np.random.permutation(indicesRestAll)
        # if we need more than 2 datapoints, select the rest nStart-2 at random
        if nStart>2:
            self.indicesKnown = np.concatenate(([self.indicesKnown, indicesRestAll[0:nStart-2]]));             
        # the rest of the points will be unlabeled at the beginning
        self.indicesUnknown = indicesRestAll[nStart-2:]
        

class DatasetCheckerboard2x2(Dataset):
    '''Loads XOR-like dataset of checkerboard shape of size 2x2.
    Origine of the dataset: generated by us. '''
    
    def __init__(self):
        
        Dataset.__init__(self)
                
        filename = './data/checkerboard2x2_train.npz'
        dt = np.load(filename)
        self.trainData = dt['x']
        self.trainLabels = dt['y']
                
        scaler = preprocessing.StandardScaler().fit(self.trainData)
        self.trainData = scaler.transform(self.trainData)
        
        filename = './data/checkerboard2x2_test.npz'
        dt = np.load(filename)
        self.testData = dt['x']
        self.testLabels = dt['y']
        self.testData = scaler.transform(self.testData)

        
class DatasetCheckerboard4x4(Dataset):
    '''Loads XOR-like dataset of checkerboard shape of size 4x4.
    Origine of the dataset: generated by us. '''
    
    def __init__(self):
        
        Dataset.__init__(self)
          
        filename = './data/checkerboard4x4_train.npz'
        dt = np.load(filename)
        self.trainData = dt['x']
        self.trainLabels = dt['y']
                
        scaler = preprocessing.StandardScaler().fit(self.trainData)
        self.trainData = scaler.transform(self.trainData)
        
        filename = './data/checkerboard4x4_test.npz'
        dt = np.load(filename)
        self.testData = dt['x']
        self.testLabels = dt['y']
        self.testData = scaler.transform(self.testData)
        
        
class DatasetRotatedCheckerboard2x2(Dataset):
    '''Loads XOR-like dataset of checkerboard shape of size 2x2 that is rotated by 45'.
    Origine of the dataset: generated by us. '''

    def __init__(self):
        
        Dataset.__init__(self)
                
        filename = './data/rotated_checkerboard2x2_train.npz'
        dt = np.load(filename)
        self.trainData = dt['x']
        self.trainLabels = dt['y']
                
        scaler = preprocessing.StandardScaler().fit(self.trainData)
        self.trainData = scaler.transform(self.trainData)
        
        filename = './data/rotated_checkerboard2x2_test.npz'
        dt = np.load(filename)
        self.testData = dt['x']
        self.testLabels = dt['y']
        self.testData = scaler.transform(self.testData)   
        
        
class DatasetSimulatedUnbalanced(Dataset):
    '''Simple dataset with 2 Gaussian clouds is generated by this class. '''
    
    def __init__(self, sizeTrain, n_dim):
        
        Dataset.__init__(self)
        cl1_prop = np.random.rand()
        # we want the proportion of class 1 to vary from 10% to 90%
        cl1_prop = (cl1_prop-0.5)*0.8+0.5
        trainSize1 = int(sizeTrain*cl1_prop)
        trainSize2 = sizeTrain-trainSize1
        # the test dataset will be 10 times bigger than the train dataset.
        testSize1 = trainSize1*10
        testSize2 = trainSize2*10
        
        # generate parameters (mean and covariance) of each cloud
        mean1 = scipy.random.rand(n_dim)
        cov1 = scipy.random.rand(n_dim,n_dim)-0.5
        cov1 = np.dot(cov1,cov1.transpose())
        mean2 = scipy.random.rand(n_dim)
        cov2 = scipy.random.rand(n_dim,n_dim)-0.5
        cov2 = np.dot(cov2,cov2.transpose())
   
        # generate train data
        trainX1 = np.random.multivariate_normal(mean1, cov1, trainSize1)
        trainY1 = np.ones((trainSize1,1))
        trainX2 = np.random.multivariate_normal(mean2, cov2, trainSize2)
        trainY2 = np.zeros((trainSize2,1))
        # the test data
        testX1 = np.random.multivariate_normal(mean1, cov1, testSize1)
        testY1 = np.ones((testSize1,1))
        testX2 = np.random.multivariate_normal(mean2, cov2, testSize2)
        testY2 = np.zeros((testSize2,1))
        
        # put the data from both clouds togetehr
        self.trainData = np.concatenate((trainX1, trainX2), axis=0)
        self.trainLabels = np.concatenate((trainY1, trainY2))
        self.testData = np.concatenate((testX1, testX2), axis=0)
        self.testLabels = np.concatenate((testY1, testY2))        
        
        
class DatasetStriatumMini(Dataset):
    
    '''Dataset from CVLab. https://cvlab.epfl.ch/data/em
    Features as in A. Lucchi, Y. Li, K. Smith, and P. Fua. Structured Image Segmentation Using Kernelized Features. ECCV, 2012'''

    def __init__(self):
        
        Dataset.__init__(self)

        filename = './data/striatum_train_features_mini.mat'
        dt = sio.loadmat(filename)
        self.trainData = dt['features']
        filename = './data/striatum_train_labels_mini.mat'
        dt = sio.loadmat(filename)
        self.trainLabels = dt['labels']
        self.trainLabels[self.trainLabels==-1] = 0
        
        scaler = preprocessing.StandardScaler().fit(self.trainData)
        self.trainData = scaler.transform(self.trainData)
        
        filename = './data/striatum_test_features_mini.mat'
        dt = sio.loadmat(filename)
        self.testData = dt['features']
        filename = './data/striatum_test_labels_mini.mat'
        dt = sio.loadmat(filename)
        self.testLabels = dt['labels']
        self.testLabels[self.testLabels==-1] = 0
        self.testData = scaler.transform(self.testData)
        
