"""
SÜSSE WURST ADDRESS GENERATOR
AUTHOR: N.F. DESMOND
DATE: JULY 2025
DESCRIPTION: This is a short program to generate random street addresses for employees who work
for Süsse Wurst. It imports a series of lists from address_generator_lists.py to create a variety 
of addresses for the greater Phoenix, AZ and Henderson/Las Vegas, NV areas.
"""

import random
from address_generator_lists import ADJECTIVE, NOUN, NAME, DIRECTIONAL, ADDRESS_PATH, \
                                    STREET_NAME, PHX_STORE, TEMPE_STORE, MESA_STORE, \
                                    PV_SCOTTS_STORE, GLEN_STORE, CHANDLER_STORE, HEND_STORE



def address_gen(address_count, directional_list, path_list, naming_option, adj_list,
                noun_list, name_list, store_list, output_path):
    with open(output_path, 'w') as output_file:
        for count in range(address_count):
            address_number = random.randint(1000, 20000)
            address_direction = random.choice(directional_list)
            name_choice = random.choice(naming_option)
            address_path = random.choice(path_list)
            address_city = random.choice(store_list)
            address_zip = random.randint(85250, 85271)
            if name_choice == NAME:
                address_name = random.choice(name_list)
                output_file.write(f'{address_number} {address_direction} {address_name} {address_path} {address_city} AZ {address_zip} \n')
            elif name_choice == NOUN:
                address_adj = random.choice(adj_list)
                address_noun = random.choice(noun_list)
                output_file.write(f'{address_number} {address_direction} {address_adj} {address_noun} {address_path} {address_city} AZ {address_zip} \n')
            elif name_choice == 'numbered':
                street_number = random.randint(1, 100)
                numbered_path_options = ['Street', 'Avenue']
                address_path = random.choice(numbered_path_options)
                if str(street_number) == '1' or (str(street_number)[-1] == '1' and len(str(street_number)) == 2) and str(street_number) != '11':
                    output_file.write(f'{address_number} {address_direction} {street_number}st {address_path} {address_city} AZ {address_zip} \n')
                elif str(street_number) == '2' or (str(street_number)[-1] == '2' and len(str(street_number)) == 2) and str(street_number) != '12':
                    output_file.write(f'{address_number} {address_direction} {street_number}nd {address_path} {address_city} AZ {address_zip} \n')
                elif str(street_number) == '3' or (str(street_number)[-1] == '3' and len(str(street_number)) == 2) and str(street_number) != '13':
                    output_file.write(f'{address_number} {address_direction} {street_number}rd {address_path} {address_city} AZ {address_zip} \n')
                else:
                    output_file.write(f'{address_number} {address_direction} {street_number}th {address_path} {address_city} AZ {address_zip} \n')


if __name__ == '__main__':
    address_gen(20, DIRECTIONAL, ADDRESS_PATH, STREET_NAME, 
                ADJECTIVE, NOUN, NAME, PHX_STORE, 
                output_path='susse_wurst_addresses.txt')