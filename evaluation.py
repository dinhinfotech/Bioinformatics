import numpy as np
from cvxopt import matrix
from sklearn import metrics
from sklearn import cross_validation
import util
from sklearn import svm

class Validation():
    def __init__(self,
                 kernels=None,
                 all_genes=None, 
                 training_genes=None,
                 training_labels=None,
                 n_folds=5):
                     
        self.kernels = kernels
        self.all_genes = all_genes
        self.training_genes = training_genes
        self.training_labels = training_labels
        self.n_folds = n_folds


    def select_parameters(self, training_genes=None, training_labels=None):
        
        list_c = [10e-4, 10e-3, 10e-2, 10e-1, 1, 10e+1, 10e+2, 10e+3, 10e+4]
        
        dict_gene_idx = {}
        for idx, gene in enumerate(self.all_genes):
            dict_gene_idx[gene]=idx
            
        dict_paras_auc = {}
        
        for kernel_idx in range(len(self.kernels)):
            for c_idx in range(len(list_c)):
                dict_paras_auc[(kernel_idx,c_idx)] = 0

        kf = cross_validation.KFold(len(training_genes), n_folds = 3)
        
        for train_index, test_index in kf:
            training_genes_left = [training_genes[idx] for idx in train_index]
            training_indices = [dict_gene_idx[gene] for gene in training_genes_left]
            training_labels_left = [training_labels[idx] for idx in train_index]
            
            
            test_genes_left = [training_genes[idx] for idx in test_index]
            test_indices = [dict_gene_idx[gene] for gene in test_genes_left]
            test_labels_left = [training_labels[idx] for idx in test_index]
            unknown_genes = []
            unknown_genes.extend(test_genes_left)
            for gene in self.all_genes:
                if gene not in training_genes:
                    unknown_genes.append(gene)
            unknown_indices = [dict_gene_idx[gene] for gene in unknown_genes]
        
            for kernel_idx, kernel in enumerate(self.kernels):
                training_kernel = util.extract_submatrix(training_indices,training_indices,kernel)
                unknown_kernel = util.extract_submatrix(unknown_indices,training_indices,kernel)
                
                
                for c_idx, c in enumerate(list_c):                        
                    clf = svm.LinearSVC(C=c, kernel='precomputed')
                    clf.fit(training_kernel, training_labels_left)
                    
                    scores = clf.decision_function(unknown_kernel)
                    
                    qscores = []
                    
                    for s in scores[:len(test_indices)]:
                        qscore = float(sum([int(s >= value) for value in scores]))/len(scores)
                        qscores.append(qscore)
                    fpr, tpr, thresholds = metrics.roc_curve(test_labels_left, qscores, pos_label= 1)
                    auc = metrics.auc(fpr, tpr)
                    
                    dict_paras_auc[(kernel_idx,c_idx)]+=auc
                
        return max(dict_paras_auc, key=dict_paras_auc.get)        
                
    def validation(self):
        
        list_c = [10e-4, 10e-3, 10e-2, 10e-1, 1, 10e+1, 10e+2, 10e+3, 10e+4]
        aucs = 0
        
        dict_gene_idx = {}
        for idx, gene in enumerate(self.all_genes):
            dict_gene_idx[gene]=idx
            
        dict_paras_auc = {}
        
        for kernel_idx in range(len(self.kernels)):
            for c_idx in range(len(list_c)):
                dict_paras_auc[(kernel_idx,c_idx)] = 0

        kf = cross_validation.KFold(len(self.training_genes), n_folds = self.n_folds)
        
        for train_index, test_index in kf:
            training_genes_left = [self.training_genes[idx] for idx in train_index]
            training_indices = [dict_gene_idx[gene] for gene in training_genes_left]
            training_labels_left = [self.training_labels[idx] for idx in train_index]
            
            
            test_genes_left = [self.training_genes[idx] for idx in test_index]
            test_indices = [dict_gene_idx[gene] for gene in test_genes_left]
            test_labels_left = [self.training_labels[idx] for idx in test_index]
            unknown_genes = []
            unknown_genes.extend(test_genes_left)
            for gene in self.all_genes:
                if gene not in self.training_genes:
                    unknown_genes.append(gene)
            unknown_indices = [dict_gene_idx[gene] for gene in unknown_genes]
            
            (kernel_idx,c_idx) = self.select_parameters(self.training_genes=training_genes_left, self.training_labels=training_labels_left)
            
            training_kernel = util.extract_submatrix(training_indices,training_indices,self.kernels[kernel_idx])
            unknown_kernel = util.extract_submatrix(unknown_indices,training_indices,self.kernels[kernel_idx])
            
                       
            clf = svm.LinearSVC(C=c_idx, kernel='precomputed')
            clf.fit(training_kernel, training_labels_left)
            
            scores = clf.decision_function(unknown_kernel)
            
            qscores = []
            
            for s in scores[:len(test_indices)]:
                qscore = float(sum([int(s >= value) for value in scores]))/len(scores)
                qscores.append(qscore)
            fpr, tpr, thresholds = metrics.roc_curve(test_labels_left, qscores, pos_label= 1)
            auc = metrics.auc(fpr, tpr)
            
            aucs+=auc
                
        return aucs/self.n_folds      