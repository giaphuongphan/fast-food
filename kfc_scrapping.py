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

# print(kfc_nutrition_data)
# filtered_nutrition_data = filter(lambda x: x.get('Sodium (mg)') and x.get('Allergens') and x.get('Protein (g)') and x.get('Servings (g)') and x.get('Total Fat (g)') and x.get('Saturated fat (g)') and x.get('Carbohydrate (g)') and x.get('Energy (kcal)'), kfc_nutrition_data)
filtered_nutrition_data = filter(lambda x: x['Sodium (mg)'] and x['Allergens'] and x['Protein (g)'] and x['Servings (g)'] and x['Total Fat (g)'] and x['Saturated fat (g)'] and x['Carbohydr ate (g)'] and x['Energy (kcal)'] in None, kfc_nutrition_data)
print(kfc_nutrition_data)

headers = nutrition_dict.keys()

# file_path = '/Users/giaphuong/Desktop/Dev/fast food data scrapping/kfc_data.csv'
# with open(file_path,'w') as csv_file:
#     csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
#     csv_writer.writeheader()
#     csv_writer.writerows(filtered_nutrition_data)

# # csv_writer.writerow(kfc_headers)
# # csv_writer.writerow(kfc_nutrition_data)
# # for interation in range(len(nutrition_data)):
# #     csv_writer.writerow([val[interation] for val in nutrition_data])

# csv_file.close()

