import pandas as pd

# Example summary DataFrames (replace these with your actual DataFrames)
data1 = {'Metric': ['Mean', 'Std', 'Min', 'Max'],
         'Value': [10, 2, 5, 15]}
summary_df1 = pd.DataFrame(data1)

data2 = {'Metric': ['Mean', 'Std', 'Min', 'Max'],
         'Value': [25, 3, 18, 30]}
summary_df2 = pd.DataFrame(data2)

# Concatenate the summary DataFrames
combined_summary = pd.concat([summary_df1, summary_df2], keys=['Analysis 1', 'Analysis 2'])

# Save the combined summary to a CSV file
combined_summary.to_csv('combined_summary.csv', index=False)
