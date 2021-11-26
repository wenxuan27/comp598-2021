import networkx as nx



import argparse
import json



def main():
    """
    Computes the network statistics.
    """
    parser = argparse.ArgumentParser(description="Computes the network statistics.")
    parser.add_argument("-i", "--input", help="Input json file", default="interaction_network.json")
    parser.add_argument("-o", "--output", help="Output json file", default="stats.json")
    args = parser.parse_args()

    # print(args.input)
    
    input_json = json.load(open(args.input))
    
    G = nx.Graph()
    
    
    for key in input_json:
        G.add_node(key)
        
    
    for key in input_json:
        for value in input_json[key]:
            G.add_edge(key, value, weight=input_json[key][value])
            
    betweenness_list = nx.betweenness_centrality(G)
    
    output_json = {
        "most_connected_by_num": [x[0] for x in sorted(G.degree(), key=lambda x: x[1], reverse=True)[:3]],
        "most_connected_by_weight": [x[0] for x in sorted(G.degree(weight='weight'), key=lambda x: x[1], reverse=True)[:3]],
        "most_central_by_betweenness": [x[0] for x in sorted(betweenness_list.items(), key=lambda x: x[1], reverse=True)[:3]],
    }
    
    
    
    json.dump(output_json, open(args.output, "w"), indent=4)
        
        
if __name__ == "__main__":
    main()