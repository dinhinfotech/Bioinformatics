**DiGI**

This repository consists of the data and source code which are used to evaluate the performances of the DiGI method proposed in the paper entitled "Heterogeneous Networks Integration for Disease Gene Prioritization with Node Kernels", submitted to Bioinformatics journal. 

DiGI is also implemented as a web tool and it is available at: http://rna.informatik.uni-freiburg.de/DiGI/Input.jsp

**Dependency:**
- Python >= 2.7
- scikit-learn >= 0.17.1
- networkx >= 2.2
- scipy >= 1.3.0
- EDeN: https://github.com/fabriziocosta/EDeN.git

**How to run DiGI**

Under the root directory of this repository, run the main.py. Following is an example with a test data:

python main.py\  
--adj_folder data/test_data/adj_matrices\\  
--train_genes_file data/test_data/train_genes\\  
--train_labels_file data/test_data/train_labels\\  
--all_genes_file data/test_data/all_genes\\  
--list_D 10 15\\  
--list_C 5\\  
--list_d 1 2\\  
--list_r 1 2


