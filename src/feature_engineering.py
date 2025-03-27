import nltk
import nltk.sentiment
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from config import keywords
import warnings

nltk.download("vader_lexicon")
def timely_features(df: pd.DataFrame):
    print("time engineering..")
    # compute number of day elapsed between calls
    df = df.sort_values(by=["match_id", "completion_date"])
    df['ndays_between_call'] = df.groupby("match_id")["completion_date"].diff().dt.days
    # fill na for data point with no precedent
    df.fillna(0, inplace=True)
    # compute aggs for call notes
    gap_stats = df.groupby('match_id')['ndays_between_call'].agg(['mean', 'max', 'std', 'count']).reset_index()
    gap_stats.rename(
        columns={
            "mean": "avg_cadence_day",
            "max": "max_cadence_day",
            "count": "call_count",
            "std": "number_of_call_std"
        }
        ,inplace=True
    )
    gap_stats = gap_stats.fillna(0)
    # merge gap stat back to original
    df = pd.merge(df, gap_stats, on="match_id", how="left")
    return df


def notes_engineering(df:pd.DataFrame):
    print("note engineering..")
    # Apply the function for each match and concatenate
    df_grouped = df.groupby("match_id").apply(split_call_notes).reset_index()
    # Merge back with the original dataframe
    df_final = pd.merge(df, df_grouped, on="match_id", how="left")
    # dropped used columns
    data = df_final.drop(
        [
            'completion_date',
            'contact_notes',
            "ndays_between_call"],
            axis=1
        ).groupby("match_id").first().reset_index()
    # topic consistency engineering
    data['early_stage_notes'] = data['early_stage_notes'].apply(preprocess)
    data['late_stage_notes'] = data['late_stage_notes'].apply(preprocess)

    # Convert texts into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data['early_stage_notes'].tolist() + data['late_stage_notes'].tolist())

    # Split into early and late vectors
    num_matches = len(data)
    early_tfidf = tfidf_matrix[:num_matches]
    late_tfidf = tfidf_matrix[num_matches:]

    # Compute Cosine Similarity between early and late notes
    similarity_scores = [
        cosine_similarity(
            early_tfidf[i],
            late_tfidf[i])[0, 0] 
            for i in range(num_matches)
    ]
    # Add topic consistency scores to DataFrame
    data['topic_consistency'] = similarity_scores

    # rationale for match engineering
    df_categories = data["rationale_for_match"].apply(categorize_match).apply(pd.Series)
    data = pd.concat([data, df_categories], axis=1)

    return data

def sentiment_engineering(df: pd.DataFrame):
    print("sentiment engineering..")
    # Compute sentiment scores for early and late stages
    df["early_stage_score"] = df["early_stage_notes"].apply(get_sentiment)
    df["late_stage_score"] = df["late_stage_notes"].apply(get_sentiment)
    df.reset_index(inplace=True)
    # Compute sentiment change
    df["sentiment_change"] = df["late_stage_score"] - df["early_stage_score"]
    # Categorize sentiment trend
    df["sentiment_trend"] = df["sentiment_change"].apply(categorize_change)
    return df


# Helpers
def split_call_notes(match_df):
    num_calls = len(match_df)
    
    # Edge case: no calls or only one call
    if num_calls == 0:
        return pd.Series(["unavailable", "unavailable"], index=["early_stage_notes", "late_stage_notes"])
    
    elif num_calls == 1:
        return pd.Series([match_df["contact_notes"].iloc[0], "unavailable"],index=["early_stage_notes", "late_stage_notes"])
    
    # Split the match calls into early and late stages based on call count
    early_stage = match_df.head(num_calls // 2)["contact_notes"].str.cat(sep=" ")  # First 50% of the calls
    late_stage = match_df.tail(num_calls - (num_calls // 2))["contact_notes"].str.cat(sep=" ")  # Remaining calls
    
    return pd.Series([early_stage, late_stage], index=["early_stage_notes", "late_stage_notes"])

# Text Preprocessing Function
def preprocess(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)  # Remove punctuation
    return text

# Function to compute sentiment score
def get_sentiment(text):
    sia = nltk.sentiment.SentimentIntensityAnalyzer()
    if text == "unavailable":  # Handle missing data
        return 0.0
    return sia.polarity_scores(text)["compound"]

def categorize_match(text):
    text = text.lower()
    categories = {key: any(word in text for word in words) for key, words in keywords.items()}
    return categories

def categorize_change(change):
    if change > 0.5:
        return "Improved"
    elif change < -0.5:
        return "Declined"
    else:
        return "Stable"
