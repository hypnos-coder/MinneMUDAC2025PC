
import pandas as pd

from prediction import prediction, prediction2
df = pd.read_excel("modeling.xlsx")

fisrt_pred = prediction(df)
second_pred = prediction2(df)


# pred = fisrt_pred+second_pred