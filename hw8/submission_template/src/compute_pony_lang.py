import pandas as pd
import json
import math
import argparse

def num_ponies_using_word(word, word_dict):
    return len(word_dict[word]['ponies'])

def num_times_pony_uses_word(word, word_dict, pony):
    return word_dict[word]['ponies'][pony]

def tf(word, word_dict, pony):
    if word in word_dict:
        if pony in word_dict[word]['ponies']:
            return num_times_pony_uses_word(word, word_dict, pony) / num_ponies_using_word(word, word_dict)
    return 0
    

def idf(word, word_dict, total_num_ponies):
    return math.log(total_num_ponies / num_ponies_using_word(word, word_dict))

def tf_idf(word, word_dict, total_num_ponies, pony):
    return tf(word, word_dict, pony) * idf(word, word_dict, total_num_ponies)

def compute_pony_lang(input_file, num_words):
    ponies_out_dict = {}

    f_open = open(input_file)
    ponies_json_input = json.load(f_open)

    total_num_ponies = len(ponies_json_input)

    words_dict = {}

    for pony in ponies_json_input:
        for word in ponies_json_input[pony]:
            if word in words_dict:
                words_dict[word]['total'] += ponies_json_input[pony][word]
            else:
                words_dict[word] = {'total': ponies_json_input[pony][word], 'ponies': {}}
                
            if pony in words_dict[word]['ponies']:
                # print(pony)
                words_dict[word]['ponies'][pony] += ponies_json_input[pony][word]
            else:
                words_dict[word]['ponies'][pony] = ponies_json_input[pony][word]


    

    for pony in ponies_json_input:
        pony_words = []

        for word in ponies_json_input[pony]:
            pony_words.append({'word': word, 'tf_idf': tf_idf(word, words_dict, total_num_ponies, pony)})


        sorted_pony_words = sorted(pony_words, key=lambda x: x['tf_idf'], reverse=True)

        # print(ponies_json_input[pony])

        ponies_out_dict[pony] = []
        
        our_list = sorted_pony_words[:num_words]

        # print(our_list)

        for word in our_list:
            ponies_out_dict[pony].append(word['word'])

    f_open.close()

    return ponies_out_dict

def main():
    """
    This function reads the file word_counts.csv and compiles the data into a
    single dataframe.
    """

    parser = argparse.ArgumentParser(description='Collects relationships from whodatedwho')
    parser.add_argument('-c', '--count', help='input file', default="word_counts.json")
    parser.add_argument('-n', '--num', help='<num_words>', default="10")

    args = parser.parse_args()

    input_file = args.count

    num_words = int(args.num)

    ponies_out_dict = compute_pony_lang(input_file, num_words)

    print(json.dumps(ponies_out_dict, indent=4))           








if __name__ == "__main__":
    main()