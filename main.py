"""
Usage:
  evaluation -a <folder> -t <file> -l <file> -C <list> -D <list> -d <list> -r <list>
              

Options:
    -a <folder>                 Specify folder which contains adjacency matrices
    -t <file>                   Specify file which contains list of training genes
    -l <file>                   Specify file which contains list of training labels
    -g <file>                   Specify file which contains list of all labels    
    -D <list>                   List of degree thresholds    
    -C <list>                   List of clique thresholds
    -d <list>                   List of maximal distances
    -r <list>                   List of maximal radiuses
  
"""
 
from docopt import docopt
import graph_util as gu
import graph 
import util
from evaluation import Validation

def main(args):
    
    adjacency_folder = args['-a']    
    training_genes_file = args['-t']    
    training_labels_file = args['-l']
    all_genes_file = args['-g']
    list_D = [int(c) for c in args['-D'].rsplit(',')]    
    list_C = [int(c) for c in args['-C'].rsplit(',')]
    list_d = [int(c) for c in args['-d'].rsplit(',')]
    list_r = [int(c) for c in args['-r'].rsplit(',')]
    
    training_genes = util.load_list_from_file(training_genes_file)
    training_labels = [int(l) for l in util.load_list_from_file(training_labels_file)]
    all_genes = util.load_list_from_file(all_genes_file)

    # Creating graphs
    graphs = gu.create_graphs(adjacency_folder_path=adjacency_folder)
    
    # Computing kernel matrices
    kernel_matrices = []    
    for D in list_D:
        for C in list_C:
            g_union = gu.union_graphs(graphs=graphs, deg_threshold=D, cli_threshold=C)
            
            for d in list_d:
                for r in list_r:
                    vec = graph.CDNK_Vectorizer(d=d, r=r, L=len(graphs), n_nodes=len(graphs[0].nodes()))
                    kernel_matrices.append(vec.cdnk(g=g_union))

    val = Validation(kernels=kernel_matrices, all_genes=all_genes, training_genes=training_genes, training_labels=training_labels)
    
    auc = val.validation()
    
    print auc

if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)    
    
    
    
    
                    
    
