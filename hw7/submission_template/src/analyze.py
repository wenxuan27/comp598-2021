# import json

import argparse

import pandas as pd

def main():
    """
    This is the main function.
    """

    parser = argparse.ArgumentParser(description='Collects relationships from whodatedwho')
    parser.add_argument('-i', '--coded_file', help='subreddit', default="subreddit.json")
    parser.add_argument('-o', '--output', help='output file', default=None)

    args = parser.parse_args()


    coded_file = args.coded_file
    output = args.output

    df = pd.read_csv(coded_file, sep='\t')

    categories = df['coding'].value_counts()

    # print(categories)

    categories_dict = {
        'course-related': categories['c'],
        'food-related': categories['f'],
        'residence-related': categories['r'],
        'other': categories['o']
    }


    # print(output)

    if(output == None):
        print(categories_dict)
    else:
        string = "{"

        for key, value in categories_dict.items():
            string += '"' + key + '": ' + str(value) + ', '

        string += "}"
        with open(output, 'w') as f:
            f.write(string)
        




if __name__ == "__main__":
    main()