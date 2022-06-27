import csv, pandas as pd, uuid

class Product:
    def __init__(self, name, quantity, price):
        self.load_product()
        self.name = name
        self.quantity = quantity
        self.price = price
        self.id = uuid.uuid4().node
        self.rate = [["avrage of rates", 0.0], ["number of rates", 0],["sum of rates", 0]]
        self.comment = {}
        self.save_product()

    def rating(self, new_rating, comment=None):
        self.rate[1][1] += 1
        self.rate[2][1] += new_rating
        self.rate[0][1] = self.rate[2][1] / self.rate[1][1]
        if comment != None:
            self.comment.update({comment[0]: comment[1]})
        ProductPrime.update_row(self)
        return "Thanks for rating us!"

    def save_product(self):
        f = open('all_products.csv', 'a')
        with f:
            fnames = ['product_id', 'name', 'quantity', 'price', 'rate', 'comment']
            writer = csv.DictWriter(f, fieldnames=fnames)    
            writer.writerow({'product_id' : str(self.id), 'name': self.name, 'quantity': self.quantity, 'price': self.price, 'rate': self.rate, 'comment': self.comment})
        return "Product saved successfully!"
     
    def load_product(self):
        try:
            with open('all_products.csv', 'r'):
                pass
        except:
            f = open('all_products.csv', 'w')
            with f:
                fnames = ['product_id', 'name', 'quantity', 'price', 'rate', 'comment']
                writer = csv.DictWriter(f, fieldnames=fnames)    
                writer.writeheader()

class ProductPrime(Product):
    def __init__(self, id):
        row = ProductPrime.product_finder(id)
        self.product_id = row['product_id']
        self.name = row['name']
        self.quantity = int(row['quantity'])
        self.price = int(row['price'])
        self.rate = eval(row['rate'])
        self.comment = eval(row['comment'])

    def product_finder(id):
        f = open('all_products.csv', 'r')
        with f:
            reader = csv.DictReader(f)
            for row in reader:
                if id == row['product_id']:
                    return row
            raise Exception ("Product doesn't exist!")
    
    def row_num(id):
        f = open('all_products.csv', 'r')
        with f:
            reader = csv.DictReader(f)
            for row in reader: 
                if id == row['product_id']:
                    return (reader.line_num - 2)

    def update_row(prod):
        row_id = ProductPrime.row_num(prod.product_id)
        df = pd.read_csv('all_products.csv')
        df.loc[row_id, 'product_id'] = prod.product_id
        df.loc[row_id, 'name'] = prod.name
        df.loc[row_id, 'quantity'] = str(prod.quantity)
        df.loc[row_id, 'price'] = prod.price
        df.loc[row_id, 'rate'] = str(prod.rate)
        df.loc[row_id, 'comment'] = str(prod.comment)
        df.to_csv('all_products.csv', index=False)
