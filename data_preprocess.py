'''

Generate the 'poem_title_sentence.csv' file with cleaned title and cleaned first sentence of a poem.

'''
import numpy as np
import pandas as pd
import re
from html import unescape

def rm_html(raw):
    return(unescape(str(raw)).lower()) #not all objects are string, some maybe float
    
def rm_nonalphabet(raw):
    pre1 = re.sub(r'[^a-zA-Z\s\d]','', raw) #not all objects are string, some maybe float
    pre2 = re.sub(r'[\s]{2,}', ' ', pre1)
    return pre2

def clean_text(raw):
    pre1 = re.sub(r'[^\x01-\x7F]+','', raw) #ascii index 1-127 is alphanumeric + space
    pre2 = re.sub('â', '', pre1)
    pre3 = re.sub(r'[\s]{2,}', ' ', pre2)
    return pre3

def first_sentence_tokenized(poem):
    return re.split(r'[,.!]', poem)[0]


if __name__ == '__main__':
    # read in data
    poem_data = 'data/poki.csv'
    df = pd.read_csv(poem_data)

    # clean title
    df['title_clean'] = df['title'].apply(rm_html)
    df['title_clean'] = df['title_clean'].apply(rm_nonalphabet)

    # clean text and create first_sentence
    df['text_clean'] = df['text'].apply(clean_text)
    df['first_sentence'] = df['text_clean'].apply(first_sentence_tokenized)

    # create cleaned pd dataframe
    df_cleaned = df.filter(['title_clean','first_sentence'], axis = 1)
    
    # when the first sentence exceeds 50 characters, drop them
    final_df = df_cleaned[df_cleaned['first_sentence'].str.len() <= 50]
    final_df.head()
    final_df.to_csv('data/poem_title_sentence.csv', index = False)


