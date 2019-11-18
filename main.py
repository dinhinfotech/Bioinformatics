import argparse
import graph_util as gu
import graph 
import util
from evaluation import Validation


def main(args):
    
    adjacency_folder = args.adj_folder
    training_genes_file = args.train_genes_file
    training_labels_file = args.train_labels_file
    all_genes_file = args.all_genes_file
    list_D = args.list_D
    list_C = args.list_C
    list_d = args.list_d
    list_r = args.list_r
    
    training_genes = util.load_list_from_file(training_genes_file)
    training_labels = [int(l) for l in util.load_list_from_file(training_labels_file)]
    all_genes = util.load_list_from_file(all_genes_file)

    # Creating list of graphs
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
    
    print(auc)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GCN')
    parser.add_argument("--adj_folder", type=str, default="", help="path to adjacency folder")
    parser.add_argument("--train_genes_file", type=str, default="", help="path to the file containing train gene list")
    parser.add_argument("--train_labels_file", type=str, default="", help="path to the file containing train label list")
    parser.add_argument("--all_genes_file", type=str, default="", help="path to the file containing all gene list")
    parser.add_argument("--list_D", type=int, nargs='+', help="List of degree thresholds")
    parser.add_argument("--list_C", type=int, nargs='+', help="List of clique thresholds")
    parser.add_argument("--list_d", type=int, nargs='+', help="List of maximum distance parameter in CDNK")
    parser.add_argument("--list_r", type=int, nargs='+', help="List of maximum radiua parameter in CDNK")
    args = parser.parse_args()

    print(args)
    main(args)
    
                    
    
