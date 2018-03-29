import sys
import util
import graph_util as gu
from graph import CDNK_Vectorizer


if __name__=='__main__':
    #if len(sys.argv) < 2:
    #    sys.exit("python main_netkit.py dataset iterations")
        
    #adjacency_folder = sys.argv[1]
    #deg_threshold = int(sys.argv[2])  
    #cli_threshold = int(sys.argv[3])
    #max_node_ID = int(sys.argv[4])

    #r = int(sys.argv[5])
    #d = int(sys.argv[6])

    adjacency_folder = "/media/dinh/DATA/Test_ECCB/adjs/"
    training_genes_path = ""
    training_labels_path = ""
    all_genes_path = ""    
    deg_threshold = 15
    cli_threshold = 4
    max_node_ID = 22000
    r = 2
    d = 2
    
    graphs = gu.create_graphs(adjacency_folder_path= adjacency_folder)    
    g_union = gu.union_graphs(graphs=graphs, deg_threshold=deg_threshold, cli_threshold=cli_threshold, max_node_ID=max_node_ID)      
    vec = CDNK_Vectorizer(r=2, d=2)        
    K = vec.cdnk(g_union)