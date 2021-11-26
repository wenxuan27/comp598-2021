

import pandas as pd

import sys


input_file = sys.argv[1]

output_file = sys.argv[2]


df = pd.read_csv(input_file, sep='\t')


for i in range(len(df)):
    print(i, df.iloc[i, 1])

    choice = input('Enter your choice: ')
    # choice = "c"

    df.iloc[i, 2] = choice


df.to_csv(output_file, sep='\t', index=False)