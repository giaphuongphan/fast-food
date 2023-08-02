from requests_html import HTMLSession, HTML
import csv

macs_url = 'https://www.mcdonalds.com.sg/full-menu'

session = HTMLSession()
result = session.get(macs_url)
result.html.render()

# extract names of food/dish macs website
food = result.html.find('a')
print(food)
# rows = result.html.find('tr')

# kfc_nutrition_data = []

# header_row = rows[0]
# kfc_headers = [header.text for header in header_row.find('th')]

# # Loop through all cells in the table except for the second column (index 1)
# for row in rows[1:]:
#     values = [cell.text for cell in row.find('td.align-middle')]
#     nutrition_dict = dict(zip(kfc_headers, values))
#     kfc_nutrition_data.append(nutrition_dict)

# csv_writer.writerow(kfc_headers)
# csv_writer.writerow(kfc_nutrition_data)
# # for interation in range(len(nutrition_data)):
# #     csv_writer.writerow([val[interation] for val in nutrition_data])

# headers = dict_obj.keys()

# file_path = '/Users/giaphuong/Desktop/Dev/fast food data scrapping/macs_data.csv'
# with open(file_path,'w') as csv_file:
#     csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
#     csv_writer.writeheader()
#     csv_writer.writerows(dict_obj)

# csv_file.close()

