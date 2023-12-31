import os
from requests_html import HTMLSession
import csv
from typing import Dict, List
import pprint
import pandas as pd


DATA_DIR = f"{os.getcwd()}/data"
KFC_URL = "https://www.kfc.com.sg/nutrition-allergen"
NUM_NUTRIENTS = 9

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def write_to_csv(file_path: str,
                 data: Dict):

# Loop through all cells in the table except for the second column (index 1)
for row in rows[1:]:
    values = [cell.text for cell in row.find('td.align-middle')]
    # save the data to dictionaries with respective key-value pairs
    nutrition_dict = dict(zip(kfc_headers, values))
    kfc_nutrition_data.append(nutrition_dict)

# filtered out items with missing key-value pairs
filtered_data = []
for dictionary in kfc_nutrition_data:
    if len(dictionary.keys()) == 9:
          filtered_data.append(dictionary)

#delete irrelevant key-value pairs (Allergens, Servings) from dictionaries on the list
for dictionaries in filtered_data:
    del dictionaries['Food']
    del dictionaries['Allergens']
    del dictionaries['Servings (g)']

first_item = filtered_data[0]
headers = first_item.keys()

# write and save data to a csv file
file_path = '/Users/giaphuong/Desktop/Dev/fast food data scrapping/kfc_data.csv'
with open(file_path,'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
    csv_writer.writeheader()
    csv_writer.writerows(filtered_data)

csv_file.close()

