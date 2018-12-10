"""This module creates a new dataframe with a movie id and its corresponding
mean sentiment score. Mean sentiment score is computed by taking the average of
the sentiment scores for all the movie's comments
"""

from os import listdir
import pandas as pd
import numpy as np
import analyze_comments_tblob as tblob

PATH = "movie_comments"
ANALYZED_PATH = "labeled_comments"

def get_sentiment_score():
    """This function makes a new df with the movie_id and sentiment score
    as columns
    """

    final_df = pd.DataFrame(columns=['movie_id', 'sentiment_score'])
    filenames2 = find_csv_filenames(PATH)
    for name in filenames2:
        new_name = PATH+"/"+name
        df = pd.read_csv(new_name, encoding='latin1')
        sentiment_df = pd.DataFrame(data=df)
        sentiment_df.columns = ["comment"]
        if not sentiment_df.empty:
            sentiment_df = tblob.analyze_comments(sentiment_df)
            if name.endswith('.csv'):
                name = name[:-4]
            sentiment_score = np.asarray(sentiment_df.iloc[:, 1], dtype=np.float).mean()
            final_df = add_row(name, sentiment_score, final_df)
    # final_df.to_csv("sentiment_scores.csv", encoding='latin1')
    return final_df

def find_csv_filenames(path_to_dir, suffix=".csv"):
    """This function returns a list of all the filenames that end with '.csv'
    """

    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

def add_row(movie_id, mean_score, final_df):
    """This function adds a row to the data frame with the movie_id and corresponding
    sentiment_score values
    """

    df2 = pd.DataFrame([[movie_id, mean_score]], columns=['movie_id', 'sentiment_score'])
    final_df = final_df.append(df2, ignore_index=True)
    return final_df
