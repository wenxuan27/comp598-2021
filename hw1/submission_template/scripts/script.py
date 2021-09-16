import pandas as pd


og_df = pd.read_csv('data/IRAhandle_tweets_1.csv')


# print(og_df.keys())

data_10000_df = og_df.head(10000)
# print(data_10000_df)

# print(data_10000_df['language'])
english_data_10000_df = data_10000_df.loc[lambda df: df['language'] == 'English']
print(english_data_10000_df)

# contains_question_mark_df = english_data_10000_df.content.str.contains('\?')
contains_question_mark_df = english_data_10000_df[english_data_10000_df.content.str.contains('^((?!\?).)*$', regex=True)]
print(contains_question_mark_df)




# count_q_mark = contains_question_mark_df.value_counts()
# print(count_q_mark)



annotated_df = contains_question_mark_df

annotated_df['trump_mention'] = annotated_df.content.str.contains('(?<![a-zA-Z0-9])Trump(?![a-zA-Z0-9])')

print(annotated_df)


count_trump_mention = annotated_df.trump_mention.value_counts()
print(count_trump_mention)



myDataframe.to_csv('dataset.tsv', sep = '\t', index=False)
