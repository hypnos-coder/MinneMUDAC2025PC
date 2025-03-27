import pandas as pd
import preprocessing
import config
import feature_engineering as fe
df = pd.read_excel("../data/Test_Truncated.xlsx")

novice_format = df.drop(
    ["Completion Date", "Match Support Contact Notes"],
    axis=1
)
contact_note_df = df[['Match ID 18Char', "Completion Date", "Match Support Contact Notes"]]

# data cleaning
cleaned_df = preprocessing.data_cleaning(novice_format, config.to_be_deleted)
# data imputation
imputed_df = preprocessing.data_imputation(cleaned_df)
# join novice_format and contact notest back.
final = preprocessing.join_training_novice(imputed_df, contact_note_df)

# time feature engineering
final = fe.timely_features(final)
# note engineering
data = fe.notes_engineering(final)
# sentiment engineering
data = fe.sentiment_engineering(data)


data.to_excel("modeling.xlsx", index=False)






