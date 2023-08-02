nutrition_dict_values = ['507.00 kcal','32.00 g','25.00 g','13.00 g','3.00 g','1265.00 mg']

nutrition_dict_numbers = []

for value in nutrition_dict_values:
    element = value.split()
    del element[1]
    nutrition_dict_numbers.append(' '.join(element)) 
    
print(nutrition_dict_numbers)