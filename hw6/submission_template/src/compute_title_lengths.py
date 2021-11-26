import json
import sys
from typing import Counter


def main():
    """
    This function computes the number of words in each title.
    """

    if len(sys.argv) < 2:
        input_file = "sample1.json"
    else:
        input_file = sys.argv[1]
    
    print(input_file)

    counter = 0
    sum_lengths = 0
    # Read the titles from the file 1
    with open(input_file, 'r') as f:
        for line in f:
            input_str = line.rstrip()
            input_json = json.loads(input_str)
            # print(input_json)

            sum_lengths += len(input_json['title'])
            counter+=1

    print("number of elements: ", counter)
    print("sum", sum_lengths)
    print("Average length of titles: ", sum_lengths/counter)


if __name__ == "__main__":
    main()