import pandas as pd
import os

import json

import argparse


def compile_word_counts(input_file):
    punctuations = ['(', ')', '[', ']', ',', '-', '.', '?', '!', ':', ';', '#', '&']

    ponies_list = [
        ["twilight sparkle", "Twilight Sparkle"], 
        ["applejack", "Applejack"], 
        ["rarity", "Rarity"],
        ["pinkie pie", "Pinkie Pie"],
        ["rainbow dash", "Rainbow Dash"],
        ["fluttershy", "Fluttershy"],
    ]

    ponies_dict = { 

    }

    all_words_dict = {}

    word_counts_threshold = 5

    stop_words = {}

    # print(os.getcwd())
    # print(__file__)
    # print(os.listdir())
    # print(os.path.dirname(__file__) + "/stopwords.txt")
    stop_words_file = os.path.dirname(__file__) + "/stopwords.txt"
    # read the stop words file
    with open(stop_words_file, "r") as f:
        for line in f:
            line_str = line.strip()
            if(line_str != ""):
                if line_str[0] != "#":
                    stop_words[line_str] = 1


    # # Read in the data
    df = pd.read_csv(input_file)

    # print(df.head())
    # print(df.columns)

    # print(df['pony'].value_counts())

    # # print(df[df['pony'] == "Rarity"]['dialog'])
    # filtered_df = df[df['pony'] == "Twilight Sparkle"]['dialog']
    # # filtered_df = filtered_df.lower()
    # harmony_df = filtered_df[filtered_df.str.contains("harmony")]
    # Harmony_df = filtered_df[filtered_df.str.contains("Harmony")]

    for pony in ponies_list:
        ponies_dict[pony[0]] = {}
        for name in pony:
            # print(name)
            filtered_df = df[df['pony'] == name]['dialog']
            
            # print(df[df['pony'] == name])

            i = 0
            for line in filtered_df:
                line_str1 = line.lower()

                for punctuation in punctuations:
                    line_str1 = line_str1.replace(punctuation, " ")
            
                line_str1 = line_str1.replace(",", " ")
                # print(i, name, line_str1)

                splitted = line_str1.split(" ")

                for word in splitted:
                    if word in stop_words:
                        continue

                    if word == "":
                        continue

                    if word == " ":
                        continue

                    if word.isalpha() == False:
                        continue
                    
                    if word in ponies_dict[pony[0]]:
                        ponies_dict[pony[0]][word] += 1
                    else:
                        ponies_dict[pony[0]][word] = 1

                    if word in all_words_dict:
                        all_words_dict[word] += 1
                    else:
                        all_words_dict[word] = 1

                i+=1

    ponies_dict2 = {}

    # print(all_words_dict)

    for pony in ponies_dict:
        ponies_dict2[pony] = {}
        for word in ponies_dict[pony]:
            if all_words_dict[word] >= word_counts_threshold:
                ponies_dict2[pony][word] = ponies_dict[pony][word]

    return ponies_dict2


def main():
    """
    This function reads the file word_counts.csv and compiles the data into a
    single dataframe.
    """

    parser = argparse.ArgumentParser(description='Collects relationships from whodatedwho')
    parser.add_argument('-o', '--output', help='output file', default="word_counts.json")
    parser.add_argument('-d', '--input', help='clean_dialog.csv file', default="data/clean_dialog.csv")

    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    res = compile_word_counts(input_file)

    # Write the data to a json file
    json.dump(res, open(output_file, "w"), indent=4)


    

if __name__ == '__main__':
    main()