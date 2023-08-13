import os
from requests_html import HTMLSession
import csv
import concurrent.futures
from typing import Dict, List
import pprint

# scrape data from the main menu page of Macs
def prefetch_urls(url: str) -> List:
    session = HTMLSession()
    result = session.get(url)
    result.html.render(timeout=120)

    target_elements = result.html.find('ul.category-list__items > li.category-item > a')

    extracted_name = []
    #find the name of all menu items
    for element in target_elements:
        food_name = element.text
        extracted_name.append(food_name)

    #remove empty entries from the list and store all valid entries in 'food' list
    food_final = [] # extract data from individual URLs of individual food items
    for item in extracted_name:
        if item:
            food_final.append(item)

    #find all links to individual food items
    extracted_link = []
    for element in target_elements:
        link  = element.attrs['href']
        extracted_link.append(link)

    #remove duplicate links
    def remove_duplicates_preserve_order(extracted_link):
        unique_links = []
        for item in extracted_link:
            if item not in unique_links:
                unique_links.append(item)
        return unique_links

    link_list = remove_duplicates_preserve_order(extracted_link)

    # the list 'URLs' contains all the full URLs corresponding to their food items
    URLs = []
    for item in link_list:
        full_link = f'https://www.mcdonalds.com.sg{item}'
        URLs.append(full_link)

    session.close()
    return URLs

# extract data from individual URLs of individual food items
def task(url: str) -> Dict:
    session = HTMLSession()
    result = session.get(url)
    result.html.render()
    nutrition_table = result.html.find('table.card__table')

    item_name = url.split("/")[-1]
    item_name = " ".join([word.capitalize() for word in item_name.split("-")])
    # extract all nutrion facts listed in tables
    nutrition_facts_text = ["Food", item_name]
    for table in nutrition_table:
        nutrition_facts_text.extend([element.text for element in table.find('td')])

    # delete Cholesterol and Dietary Fibres from the nutrition fact lists for comparison with kfc
    del nutrition_facts_text[8:10]
    del nutrition_facts_text[9:11]
    # create key-value pairs for dictionaries
    nutrition_dict_keys = nutrition_facts_text[::2]

    # add the units to each key/header 
    nutrition_dict_keys = [key.replace('Energy', 'Energy (kcal)') for key in nutrition_dict_keys]
    nutrition_dict_keys = [key.replace('Protein', 'Protein (g)') for key in nutrition_dict_keys]
    nutrition_dict_keys = [key.replace('Total Fat', 'Total Fat (g)') for key in nutrition_dict_keys]
    nutrition_dict_keys = [key.replace('Saturated Fat', 'Saturated fat (g)') for key in nutrition_dict_keys]
    nutrition_dict_keys = [key.replace('Carbohydrates', 'Carbohydrate (g)') for key in nutrition_dict_keys]
    nutrition_dict_keys = [key.replace('Sodium', 'Sodium (mg)') for key in nutrition_dict_keys]

    nutrition_dict_values = nutrition_facts_text[1::2]
    # remove the unnecessary information and retain only the numeral values for the nutrition data
    nutrition_dict_numbers = []

    for value in nutrition_dict_values:
        # element = value.split(" ")[0]
        # del element[1]
        # nutrition_dict_numbers.append(" ".join(element))
        element = value.split(" ")[0]
        nutrition_dict_numbers.append(element)   
    
    print(nutrition_dict_numbers)
    macs_nutrition_dict = {key: value for key, value in zip(nutrition_dict_keys, nutrition_dict_numbers)}
    session.close()
    return macs_nutrition_dict

# write all the scrapped data to the csv file
def write_to_csv(data: List) -> None:
    first_item = data[0]
    headers = first_item.keys()

    file_path = f'{os.getcwd()}/data/macs_data.csv'
    with open(file_path,'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, headers)
        csv_writer.writeheader()
        csv_writer.writerows(data)

    csv_file.close()

# execute the tasks concurrently
def main():
    """
    Entry point of scraping program
    """
    macs_url = 'https://www.mcdonalds.com.sg/full-menu'

    URLs = prefetch_urls(macs_url)
    macs_nutrition_data = []

    # Create a ThreadPoolExecutor to run the tasks in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        results = executor.map(task, URLs)

        for result in results:
            macs_nutrition_data.append(result)
    print(macs_nutrition_data)
    write_to_csv(macs_nutrition_data)

if __name__ == "__main__":
    main()

