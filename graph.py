# -*- coding: utf-8 -*-
from eden.graph import Vectorizer
from sklearn.metrics import pairwise
from scipy.sparse import vstack

class CDNK_Vectorizer():
    def __init__(self,                 
                 L=None, 
                 n_nodes=None,
                 d=2,
                 r=1,                 
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
        self.L = L           
        self.n_nodes = n_nodes
        self.d = d        
        self.r = r
        self.nbits = nbits
        self.discrete=discrete

    def vectorize(self, g):
        """ Vectorize graph nodes
        
        Return: matrix in which rows are the vectors that represents for nodes        
        """
        
        vec = Vectorizer(nbits=self.nbits, 
                         discrete=self.discrete, 
                         d=self.d,
                         r=self.r
                         )
                         
        M = vec.vertex_transform([g])[0]  
        M_reduce = []
        for idx in range(self.n_nodes):
            vec = M[idx,:]
            for l in range(1, self.L):
                vec = vec + M[idx + l*self.n_nodes,: ]
            M_reduce.append(vec)
        M = vstack(M_reduce)                     
        return M

    def cdnk(self, g=None):
        """Compute graph node kernel matrix encoding node similarities
        
           Return: 
           Kernel matrix
        """            
        M = self.vectorize(g)
        K = pairwise.linear_kernel(M,M)
        
        return K        