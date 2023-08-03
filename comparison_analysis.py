import csv
import pandas as pd
import matplotlib.pyplot as plt

# access 2 csv files containing data from kfc and macs websites
kfc_file_path = 'kfc_data.csv'
macs_file_path = 'macs_data.csv'

# Initialize empty lists to store data from CSV files
kfc_data = []
macs_data = []

# Read data from kfc CSV file
with open(kfc_file_path, 'r') as kfc:
    kfc_reader = csv.DictReader(kfc)
    for row in kfc_reader:
        kfc_data.append(row)

# Read data from macs CSV file
with open(macs_file_path, 'r') as macs:
    macs_reader = csv.DictReader(macs)
    for row in macs_reader:
        macs_data.append(row)

# Create pandas DataFrames from the lists of data
df_kfc = pd.DataFrame(kfc_data)
df_macs = pd.DataFrame(macs_data)

# Convert numeric columns to appropriate data types
kfc_numeric_columns = ['Energy (kcal)', 'Protein (g)', 'Total Fat (g)', 'Saturated fat (g)', 'Carbohydr ate (g)', 'Sodium (mg)']
# macs_numeric_columns = ['Energy (kcal)', 'Protein (g)', 'Total Fat (g)', 'Saturated fat (g)', 'Carbohydrate (g)', 'Sodium (mg)']
macs_numeric_columns = ['Energy', 'Protein', 'Total Fat', 'Saturated Fat', 'Carbohydrates', 'Sodium']

df_kfc[kfc_numeric_columns] = df_kfc[kfc_numeric_columns].apply(pd.to_numeric, errors='coerce')
df_macs[macs_numeric_columns] = df_macs[macs_numeric_columns].apply(pd.to_numeric, errors='coerce')

# Perform analysis on the DataFrames
kfc_mean = df_kfc.mean()
macs_mean = df_macs.mean()

print(f"Average values for KFC: {kfc_mean}")
print(f"Average values for Macs: {macs_mean}")

# Protein intake: 76.3g (males) and 62.6g (females)
# Total fat intake: 86.5g (males) and 67.9g (females) 
# Saturated fat intake: 28.8g (males) 22.6g (females)
# Carbohydrates intake: 389.3g (males) and 305.7g (females)
# source: National Nutrition Survey 2010 Singapore >>> https://www.hpb.gov.sg/docs/default-source/pdf/nns-2010-report.pdf?sfvrsn=18e3f172_2

# Sodium allowance: 5g/day = 5000mg/day
# source: https://www.healthhub.sg/live-healthy/15/dietary_guidelines_adults

# MORE ADVANCED ANALYSIS - NOT NEEDED AT THIS POINT
# # Perform analysis on the DataFrames
# summary_kfc = df_kfc.describe()
# summary_macs = df_macs.describe()

# # Concatenate the summary DataFrames
# combined_summary = pd.concat([summary_kfc, summary_macs], keys=["KFC Analysis", "McDonald's Analysis"])

# combined_summary.to_csv('summary.csv', index=False)