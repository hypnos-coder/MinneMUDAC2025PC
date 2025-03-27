
import pandas as pd


df = pd.read_excel("modeling.xlsx")
df.drop([
    'match_id',
    'sentiment_trend',
    "program_type",
    "big_race_ethnicity",
    "little_participant__race_ethnicity",
    "rationale_for_match",
    "index",
    "little_gender",
    "big_gender",
    "big_occupation",
    "program",

    ], axis=True, inplace=True)
print()