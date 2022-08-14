import os
import json

class Product:
    
    def __init__(self):
        self.product = self.read_json()
    
    def read_json(self):
        files = os.listdir()
        if 'products.json' not in files:
            self.create_db_file()
        with open('products.json', 'r', encoding='utf-8') as f:
            file = json.load(f)
        self.product = file
        
    def create_db_file(self):
        # check if products.json available before calling the function.
        products = {'products': {},
                    'beads': {}}
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=4)
            
    def update_json(self):
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(self.product, f, ensure_ascii=False, indent=4)
        
    def add_new_bead(self, number_of_piece, total_price, bead_name):
        # calculate unit price,
        try:
            unit_price = total_price / number_of_piece
        except:
            raise Exception("Error occured while calculating unit price, please check inputs.")
        # save item into json file with all information
        beads = self.product['beads']   # beads is a dictionary
        if bead_name in beads:
            raise Exception("This name has already used on another item. Please write another name")
        
        info = {'Item_Name': bead_name,
                'Unit_Price': unit_price,
                'Number_of_Piece': number_of_piece,
                'Total_Price': total_price}
        self.product['beads'][bead_name] = info
        self.update_json()
            
    def add_new_necklace(self, item_list, necklace_name):
        # item_list = bean names: # of piece,
        necklaces = self.product['products']
        if necklace_name in necklaces:
            raise Exception("This name has already used on another item. Please write another name")
        
        beads = self.product['beads']
        product_price = 0
        for item, piece in item_list.items():
            item_price = beads[item]['Unit_Price'] * piece
            product_price += item_price
        necklace = {'Item_Name': necklace_name,
                    'Price': product_price,
                    'Beads': item_list}
        
        self.product['products'][necklace_name] = necklace
        self.update_json()   
    