import pandas as pd

from prediction import prediction, prediction2

# Load data
df = pd.read_excel("modeling.xlsx")
ids = df['match_id']
# Generate predictions (assumed to be lists)
first_pred = prediction(df)   # Returns a list
second_pred = prediction2(df) # Returns a list

# Compute final prediction by element-wise addition
final_prediction = [p1 + p2 for p1, p2 in zip(first_pred, second_pred)]

# Create a new DataFrame with the id column from df
result_df = pd.DataFrame({
    "match_id": ids,  
    "final_prediction": final_prediction
})

# Display or save the final DataFrame
print(result_df.head())  
result_df.to_excel("final_predictions.xlsx", index=False)  
