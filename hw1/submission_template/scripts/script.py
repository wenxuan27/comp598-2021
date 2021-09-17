import pandas as pd
import math

# this function truncates the final answer to any given amount of decimals
def truncate_to_decimal(number, decimals):
    move = 10 ** decimals
    tmp = number * move
    tmp = math.trunc(tmp)
    return tmp / (move)


# import the csv file into a pandas dataframe
og_df = pd.read_csv('data/IRAhandle_tweets_1.csv')


# keep only the 10000 first rows of the csv file
data_10000_df = og_df.head(10000)
# print(data_10000_df)

# keep only the english tweets
english_data_10000_df = data_10000_df.loc[lambda df: df['language'] == 'English']
# print(english_data_10000_df)

# get only tweets with no
no_question_mark_df = english_data_10000_df[english_data_10000_df.content.str.match(
    '^((?!\?).)*$')]

# previous way I used to match no question marks. using str.contains caused a warning which was annoying so I switched to str.match()
# no_question_mark_df = english_data_10000_df[english_data_10000_df.content.str.contains(
#     '^((?!\?).)*$', regex=True)]
    
# print(no_question_mark_df)

# count the number of tweets without question marks. there are exactly 4802 such tweets.
count_q_mark = english_data_10000_df.content.str.match(
    '^((?!\?).)*$').value_counts()
print(count_q_mark)


# create a new column with trump_mentions
annotated_df = no_question_mark_df
annotated_df['trump_mention'] = annotated_df.content.str.contains(
    '(?<![a-zA-Z0-9])Trump(?![a-zA-Z0-9])')

# print(annotated_df)

# count the number of tweets with trump_mentions
count_trump_mention = annotated_df.trump_mention.value_counts()
# print(count_trump_mention)

# rearrange the columns and only keep the ones that we need
annotated_df2 = annotated_df[['tweet_id',
                              'publish_date', 'content', 'trump_mention']]
# print(annotated_df2)


# output the annotated dataset into a file
annotated_df2.to_csv('dataset.tsv', sep='\t', index=False)


# calculate the fraction of tweets that have trump mention
frac_trump_mentions = count_trump_mention / count_q_mark


# print(frac_trump_mentions[True])
# print(type(frac_trump_mentions[True]))

# truncate the results to 3 decimals
truncated_frac_trump_mentions = truncate_to_decimal(
    frac_trump_mentions[True], 3)
print(truncated_frac_trump_mentions)


# output the results into a file
data = {'result': "frac-trump-mentions",
        "value": truncated_frac_trump_mentions}
results_df = pd.DataFrame(data, columns=['result', 'value'], index=[0])
results_df.to_csv('results.tsv', sep='\t', index=False)
