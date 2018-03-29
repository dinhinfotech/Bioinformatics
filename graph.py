# -*- coding: utf-8 -*-
from eden.graph import Vectorizer
from sklearn.metrics import pairwise
from scipy.sparse import vstack

class CDNK_Vectorizer():
    def __init__(self,
                 r=1,
                 d=2,
                 nbits=20,
                 discrete=True,
                 n_jobs=1):
        """ Constructor
        
        Parameters:
            - max_deg: 
            - cli_threshold:
            - r: r
            - d: distance
            - nbits:
            - n_jobs:
                
        """                     
        self.r = r
        self.d = d
        self.nbits = nbits
        self.discrete=discrete

    def vectorize(self, g):
        """ Vectorize graph nodes
        
        Return: matrix in which rows are the vectors that represents for nodes        
        """
        
        vec = Vectorizer(nbits=self.nbits, 
                         discrete=self.discrete, 
                         r=self.r, 
                         d=self.d)
                         
        M = vec.vertex_transform([g])[0]  
        M_reduce = []
        for idx in range(7311):
            vec = M[idx,:] + M[idx + 7311,: ] + M[idx+(2*7311),:]
            M_reduce.append(vec)
        M = vstack(M_reduce)                     
        return M

    def cdnk(self, g):
        """Compute graph node kernel matrix encoding node similarities
        
           Return: 
           Kernel matrix
        """            
        M = self.vectorize(g)
        K = pairwise.linear_kernel(M,M)
        
        return K        