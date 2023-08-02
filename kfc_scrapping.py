from requests_html import HTMLSession, HTML
import csv

kfc_url = 'https://www.kfc.com.sg/nutrition-allergen'

session = HTMLSession()
result = session.get(kfc_url)
result.html.render()

# extract data from nutrion tables on kfc website
tables = result.html.find('table.table.table-bordered.tableChartNutrition.table-sm')
rows = result.html.find('tr')
# rows = tables[0].find('tr')

kfc_nutrition_data = []

header_row = rows[0]
kfc_headers = [header.text for header in header_row.find('th')]

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

