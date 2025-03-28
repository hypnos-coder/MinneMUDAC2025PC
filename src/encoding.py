import pandas as pd
from config import busyness_mapping, job_attributes, default_attributes
# Tokenize and compute Jaccard Similarity (intersection / union)
def jaccard_similarity(str1, str2):
    set1 = set(str(str1).lower().split(' '))
    set2 = set(str(str2).lower().split(' '))
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

# Function to assign busyness score
def get_busyness(occupation):
    return busyness_mapping.get(occupation, 3)  # Default to 3 if not found (moderate busyness)
# Function to match occupation and assign attributes
def get_job_features(occupation):
    for key in job_attributes:
        if key.lower() in occupation.lower():
            return job_attributes[key]
    return default_attributes  # Assign default values if no match found

def encoding(df):
    job_features = df['big_occupation'].apply(get_job_features).apply(pd.Series)
    df = pd.concat([df, job_features], axis=1)

    # some features engineering
    df["big_age_match_start"] = abs(df['big_birthdate'].dt.year - df["match_activation_date"].dt.year)
    df["little_age_match_start"] = abs(df['little_birthdate'].dt.year - df["match_activation_date"].dt.year)
    df["same_gender"] = df['little_gender']==df['big_gender']

    df.drop([
    "big_occupation", "big_gender", "little_gender", "big_birthdate",
    "match_activation_date", "little_birthdate", "late_stage_notes", "early_stage_notes",
    "program", 
    ], axis=1, inplace=True)

    df['race_similarity'] = df.apply(lambda row: jaccard_similarity(row['big_race_ethnicity'], row['little_participant__race_ethnicity']), axis=1)

    return df