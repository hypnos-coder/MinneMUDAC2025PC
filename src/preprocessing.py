import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import warnings
from missforest import MissForest
warnings.simplefilter("ignore")


def data_cleaning(df: pd.DataFrame, to_be_deleted: list):
    print("cleaning started....")
    df.drop(to_be_deleted, axis=1, inplace=True)
    # convert all column to lower case
    df.columns = (
        df.columns.str.strip()  # Remove leading/trailing spaces
                .str.replace(':', '_', regex=True)  # Replace colons (`:`) with underscores
                .str.replace(r'\s+', '_', regex=True)  # Replace any spaces with underscores
    )
    df.columns = [
        x.lower().\
            replace("contact: ", "").\
            replace("finder - ", "").\
            replace("/","_").\
            replace("_18char","").\
            replace(" ", "_")
        for x in df.columns]
    print("cleaning done...")
    return df

def data_imputation(df: pd.DataFrame):
    print("imputation started...")
    # Identify categorical and datetime columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    datetime_cols = df.select_dtypes(include=['datetime64']).columns
    # Store the datetime column separately
    datetime_df = df[datetime_cols]
    # Drop the datetime column before imputation
    df = df.drop(columns=datetime_cols)
    # Convert categorical columns to 'category' dtype
    for col in categorical_cols:
        df[col] = df[col].astype('category')
    # Save category mappings for conversion after imputation
    category_mappings = {col: dict(enumerate(df[col].cat.categories)) for col in categorical_cols}
    # Convert categorical columns to numerical codes
    for col in categorical_cols:
        df[col] = df[col].cat.codes
        df[col].replace(-1, np.nan, inplace=True)  # Keep missing values as NaN
    # Initialize MissForest imputer
    imputer = MissForest()
    # Perform imputation
    imputed_df = imputer.fit_transform(df)
    # Convert back to dfFrame
    imputed_df = pd.DataFrame(imputed_df, columns=df.columns)
    # Convert categorical columns back to original categories
    for col in categorical_cols:
        imputed_df[col] = imputed_df[col].round().astype(int)
        imputed_df[col] = imputed_df[col].map(category_mappings[col])

    # Add the datetime column back
    imputed_df = pd.concat([imputed_df, datetime_df.reset_index(drop=True)], axis=1)
    imputed_df['big_race_ethnicity'].dropna(inplace=True, axis=0)
    print("imputation done...")
    return imputed_df

def join_training_novice(clean_df: pd.DataFrame, contact_note_df: pd.DataFrame):
    # join both dataframe back
    contact_note_df.rename({
        'Match ID 18Char': "match_id",
        'Completion Date':'completion_date',
        "Match Support Contact Notes":"contact_notes"
    },axis=1, inplace=True)

    # drop missing values in contact notes
    contact_note_df.dropna(axis=0, inplace=True)
    join_df = pd.merge(contact_note_df, clean_df, how='left', on='match_id')

    return join_df
   