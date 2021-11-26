
import json
# import argparse

import pandas as pd

import os




def main():
    """
    This is the main function.
    """

    if (len(os.sys.argv) < 5):
        print("Usage: python3 extract_to_tsv.py -o <out_file> <json_file> <num_posts_to_output>")
        return

    # Parse the command line arguments
    if (os.sys.argv[1] != "-o"):
        print("Usage: python3 extract_to_tsv.py -o <out_file> <json_file> <num_posts_to_output>")
        return
    
    out_file = os.sys.argv[2]
    json_file = os.sys.argv[3]
    num_posts_to_output = int(os.sys.argv[4])

    input_file = json_file

    # Create a dataframe from the data
    df = pd.DataFrame(columns=['name', 'title', 'coding'])

    # Read the input file
    with open(input_file, 'r', encoding="utf-8") as f:
        i = 0
        for line in f:
            if (i >= num_posts_to_output):
                break            

            # Parse the JSON
            data = json.loads(line.rstrip())

            # Extract the data
            name = data['name']
            title = data['title']
            # coding = data['coding']

            # Add the data to the dataframe
            df = df.append({'name': name, 'title': title, 'coding': ""}, ignore_index=True)

            i += 1


    print(df)


    # Write the dataframe to a TSV file
    df.to_csv(out_file, sep='\t', index=False)



    

if __name__ == "__main__":
    main()