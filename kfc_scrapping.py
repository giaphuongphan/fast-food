import os
from requests_html import HTMLSession
import csv
from typing import Dict, List
import pprint
import pandas as pd


DATA_DIR = f"{os.getcwd()}/data"
KFC_URL = "https://www.kfc.com.sg/nutrition-allergen"


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

        current_allergens = ""
        if len(nutrients) >= 9:
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
                    "Servings (g)": weights[0],
                    "Energy (kcal)": weights[1],
                    "Protein (g)": weights[2],
                    "Total Fat (g)": weights[3],
                    "Saturated Fat (g)": weights[4],
                    "Carbohydrate (g)": weights[5],
                    "Sodium (mg)": weights[6]
                }


            current_allergens = ""
    pprint.pprint(scraped_food)

    # Write and save data to a kfc_data.csv file
    write_to_csv(file_path = f"{DATA_DIR}/kfc_data.csv",
                 data=scraped_food)

    df = pd.read_csv(f"{DATA_DIR}/kfc_data.csv", thousands=',')
    print(df.info())

if __name__ == "__main__":
    main()
