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

    headers = data[list(data.keys())[0]].keys()

    with open(file=file_path, mode="w") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
        csv_writer.writeheader()

        for food in data.keys():
            csv_writer.writerow(data[food])

    csv_file.close()

def main():

    session = HTMLSession()
    result = session.get(KFC_URL)
    result.html.render()

    # Extract data from nutrion tables on kfc website
    tables = result.html.find("table.table.table-bordered.tableChartNutrition.table-sm")
    scraped_food = {}

    for table in tables:
        table_body = table.find("tbody")[0]
        table_rows = table_body.find("tr")

        header = table_rows[0]
        nutrients = header.find("th")

        current_allergens = None
        if len(nutrients) >= NUM_NUTRIENTS:
            food_list = table_rows[1:]
            for idx, food in enumerate(food_list):
                name = food.find("td")[0].text

                if idx == 0:
                    current_allergens_list = food.find("td")[1].find("ul")[0].find("li")
                    current_allergens = ",".join([allergen.text for allergen in current_allergens_list])
                    weights =  [val.text for val in food.find("td")[2:9]]
                else:
                    weights = [val.text for val in food.find("td")[1:8]]

                scraped_food[name] = {
                    "Food": name,
                    "Allergens": current_allergens,
                    "Servings (g or ml)": weights[0],
                    "Energy (kcal)": weights[1],
                    "Protein (g)": weights[2],
                    "Total Fat (g)": weights[3],
                    "Saturated Fat (g)": weights[4],
                    "Carbohydrate (g)": weights[5],
                    "Sodium (mg)": weights[6]
                }


            current_allergens = None
    pprint.pprint(scraped_food)

    # Write and save data to a kfc_data.csv file
    csv_file_path = f"{DATA_DIR}/kfc_data.csv"
    write_to_csv(file_path=csv_file_path,
                 data=scraped_food)

    df = pd.read_csv(filepath_or_buffer=csv_file_path, thousands=",")

    new_servings = []
    for val in df["Servings (g or ml)"]:
        if "ml" not in val:
            val += "g"
        new_servings.append(val)

    new_column = pd.Series(new_servings, name='Servings (g or ml)')
    df.update(new_column)

    df.to_csv(path_or_buf=csv_file_path, index=False)

if __name__ == "__main__":
    main()
