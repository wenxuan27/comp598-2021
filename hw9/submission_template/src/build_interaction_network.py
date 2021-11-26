import numpy as np
import networkx as nx
import pandas as pd

import argparse
import json

import re


def check_bad_names(name):
    if name == None:
        return False
    if re.search(r'\bothers\b', name.lower()) != None:
        return False
    if re.search(r'\bponies\b', name.lower()) != None:
        return False
    if re.search(r'\band\b', name.lower()) != None:
        return False
    if re.search(r'\ball\b', name.lower()) != None:
        return False
    
    return True

def main():
    """
    Builds the interaction network from the dataframe.
    """
    
    argparser = argparse.ArgumentParser(description='Builds the interaction network from the dataframe.')
    argparser.add_argument('-i', '--input', help='Input file', default='data/clean_dialog.csv')
    argparser.add_argument('-o', '--output', help='Output file', default='interaction_network.json')
    
    args = argparser.parse_args()
    
    df = pd.read_csv(args.input)
    
    
    pony_value_counts = df['pony'].value_counts()
    
    top_101_ponies = []
    
    counter = 0
    for i in range(len(pony_value_counts)):
        
        print(counter, pony_value_counts.index[i], pony_value_counts[i])
        if check_bad_names(pony_value_counts.index[i]):
            top_101_ponies.append(pony_value_counts.index[i])
            counter += 1
            
            if counter >= 101:
                break
            
            
    
    print(top_101_ponies)
    
    G = nx.Graph()
    
    for pony in top_101_ponies:
        G.add_node(pony)
    
    prev_pony = None
    prev_episode = None
    
    for i in range(len(df)):
        row = df.iloc[i]
        
        if row['pony'] in top_101_ponies:
            if prev_pony is not None:
                if prev_pony != row['pony']:
                    if prev_episode is not None:
                        if row['title'] == prev_episode:
                            if G.has_edge(prev_pony, row['pony']):
                                G[prev_pony][row['pony']]['weight'] += 1
                            else:
                                G.add_edge(prev_pony, row['pony'], weight=1)
                       
                prev_episode = row['title']
            
            prev_pony = row['pony']
        else:
            prev_pony = None
            
    
    output_dict = {}
    
    for node in G.nodes():
        node_lower = node.lower()
        
        if node_lower in output_dict:
            for neighbor in G.neighbors(node):
                neighbor_lower = neighbor.lower()
                
                if neighbor_lower in output_dict[node_lower]:
                    output_dict[node_lower][neighbor_lower] += G[node][neighbor]['weight']
                else:
                    output_dict[node_lower][neighbor_lower] = G[node][neighbor]['weight']
        else:
            output_dict[node_lower] = {}
            
            for neighbor in G.neighbors(node):
                neighbor_lower = neighbor.lower()
                
                if neighbor_lower in output_dict[node_lower]:
                    output_dict[node_lower][neighbor_lower] += G[node][neighbor]['weight']
                else:
                    output_dict[node_lower][neighbor_lower] = G[node][neighbor]['weight']
            
            
    with open(args.output, 'w') as outfile:
        json.dump(output_dict, outfile, indent=4)
    
    
    
    
if __name__ == '__main__':
    main()