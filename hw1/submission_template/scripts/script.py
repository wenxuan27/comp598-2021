import pandas as pd
import math


def truncate_to_decimal(number, decimals):
    move = 10 ** decimals
    tmp = number * move
    tmp = math.trunc(tmp)
    return tmp / (move)


og_df = pd.read_csv('data/IRAhandle_tweets_1.csv')


# print(og_df.keys())

data_10000_df = og_df.head(10000)
# print(data_10000_df)

# print(data_10000_df['language'])
english_data_10000_df = data_10000_df.loc[lambda df: df['language'] == 'English']
print(english_data_10000_df)

# contains_question_mark_df = english_data_10000_df.content.str.contains('\?')
contains_question_mark_df = english_data_10000_df[english_data_10000_df.content.str.contains(
    '^((?!\?).)*$', regex=True)]
print(contains_question_mark_df)


count_q_mark = english_data_10000_df.content.str.contains(
    '^((?!\?).)*$', regex=True).value_counts()
# print("fjdkls;ajfldjasf")
print(count_q_mark)


annotated_df = contains_question_mark_df

annotated_df['trump_mention'] = annotated_df.content.str.contains(
    '(?<![a-zA-Z0-9])Trump(?![a-zA-Z0-9])')

print(annotated_df)


count_trump_mention = annotated_df.trump_mention.value_counts()
print(count_trump_mention)


annotated_df.to_csv('dataset.tsv', sep='\t', index=False)


# print("fjdkls;ajfldjasf")
print(count_q_mark[True])
print(count_trump_mention[True])

frac_trump_mentions = count_trump_mention / count_q_mark


print(frac_trump_mentions[True])
print(type(frac_trump_mentions[True]))


truncated_frac_trump_mentions = truncate_to_decimal(
    frac_trump_mentions[True], 3)
print(truncated_frac_trump_mentions)


data = {'result': "frac-trump-mentions",
        "value": truncated_frac_trump_mentions}
results_df = pd.DataFrame(data, columns=['result', 'value'], index=[0])


print(results_df)


results_df.to_csv('results.tsv', sep='\t', index=False)