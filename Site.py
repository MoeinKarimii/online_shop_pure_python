import hashlib, csv, pandas as pd
from Account import Account, AccountPrime
from Product import Product, ProductPrime

class Site:
    def __init__(self, url, active_users = []):
        self.load_urls
        self.save_url(url)
        self.url = url
        self.load_url_detail
        self.active_users = active_users
        self.products = {}

    @property
    def load_urls(cls):
        try:
            with open('all_urls.csv', 'r'):
                pass
        except:
            f = open('all_urls.csv', 'w')
            with f:
                fnames = ['url_address']
                writer = csv.DictWriter(f, fieldnames=fnames)    
                writer.writeheader()

    def save_url(cls, url):
        f = open('all_urls.csv', 'r')
        with f:
            reader = csv.DictReader(f)
            for row in reader:
                if url == row['url_address']:
                    raise Exception ("Url already exists")
        f = open('all_urls.csv', 'a')
        with f:
            fnames = ['url_address']
            writer = csv.DictWriter(f, fieldnames=fnames)    
            writer.writerow({'url_address' : url})
            return

    @property
    def load_url_detail(self):
        try:
            with open(f'{self.url}-registered_users.csv', 'r'):
                pass
        except:
            f = open(f'{self.url}-registered_users.csv', 'w')
            with f:
                fnames = ['usernames']
                writer = csv.DictWriter(f, fieldnames=fnames)    
                writer.writeheader()
        try:
            with open(f'{self.url}-product_ids.csv', 'r'):
                pass
        except:
            f = open(f'{self.url}-product_ids.csv', 'w')
            with f:
                fnames = ['product_ids']
                writer = csv.DictWriter(f, fieldnames=fnames)    
                writer.writeheader()
        try:
            with open(f'{self.url}-purchases.csv', 'r'):
                pass
        except:
            f = open(f'{self.url}-purchases.csv', 'w')
            with f:
                fnames = ['product_ids', 'product_name', 'customer_username', 'price']
                writer = csv.DictWriter(f, fieldnames=fnames)    
                writer.writeheader()

    def add_registered_users(self, user):
        f = open(f'{self.url}-registered_users.csv', 'a')
        with f:
            fnames = ['usernames']
            writer = csv.DictWriter(f, fieldnames=fnames)    
            writer.writerow({'usernames': user.username})
            return

    def add_product_ids(self, product):
        f = open(f'{self.url}-product_ids.csv', 'a')
        with f:
            fnames = ['product_ids']
            writer = csv.DictWriter(f, fieldnames=fnames)
            writer.writerow({'product_ids': product.product_id})
            return

    def add_purchases(self, purchase_detail):
        f = open(f'{self.url}-purchases.csv', 'a')
        with f:
            fnames = ['product_ids', 'product_name', 'customer_username', 'price']
            writer = csv.DictWriter(f, fieldnames=fnames)  
            writer.writerow({'product_ids': purchase_detail[0], 'product_name': purchase_detail[1], 'customer_username': purchase_detail[2], 'price': purchase_detail[3]})
            return

    def print_items(file_name):
        f = open(file_name, 'r')
        with f:
            reader = csv.DictReader(f)
            for row in reader:
                    
                print(row)
        return

    def register(self, user):
        Account.username_pass(user.username, True)
        Site.value_pass(user.username, f'{self.url}-registered_users.csv', 'usernames')
        self.add_registered_users(user)
        return "register successful"

    @staticmethod
    def value_pass(value, file_name, header, exists=False):
        f = open(file_name, 'r')
        with f:
            reader = csv.DictReader(f)
            for row in reader:
                if value == row[header]:
                    if exists == True:
                        return row
                    raise Exception ("Value already exists")
            if exists == True:
                raise Exception ("the value doesn't exist")

    @staticmethod
    def len_rows(file_name):
        results = pd.read_csv(file_name)
        return len(results)

    def login(self, acc):
        password = hashlib.sha256(acc["password"].encode('utf-8')).hexdigest()
        if "username" in acc and "password" in acc and "email" in acc:
            if acc['username'] not in self.active_users:
                Site.value_pass(acc['username'], f'{self.url}-registered_users.csv', 'usernames', True)
                row = Site.value_pass(acc['username'], 'all_accounts.csv', 'usernames', True)
                if row['email'] == acc['email'] and row['password'] == password:
                    self.active_users.append(acc['username'])
                    return "login successful"
                else:
                    return 'invalid login'
            else:
                return "user already logged in"
            
        elif "username" in acc and "password" in acc:
            if acc['username'] not in self.active_users:
                Site.value_pass(acc['username'], f'{self.url}-registered_users.csv', 'usernames', True)
                row = Site.value_pass(acc['username'], 'all_accounts.csv', 'usernames', True)
                if row['password'] == password:
                    self.active_users.append(acc['username'])
                    return "login successful"
                else:
                    return 'invalid login'
            else:
                return "user already logged in"

        elif "password" in acc and "email" in acc:
            row = Site.value_pass(acc['email'], 'all_accounts.csv', 'email', True)
            if row['username'] not in self.active_users:
                if row['password'] == password:
                    self.active_users.append(row['username'])
                else:
                    return 'invalid login'
            else:
                return 'user already logged in'

    def logout(self, user):
        if user.username in self.active_users:
            self.active_users.remove(user.username)
            return "logout successful"
        else:
            return "user is not logged in"

    def add_product(self, product):
        Site.value_pass(product.product_id, f'{self.url}-product_ids.csv', 'product_ids')
        self.add_product_ids(product)
        return "The product has been saved successfully"

    def see_items(self, user):
        if user.username in self.active_users:
            Site.print_items(f'{self.url}-product_ids.csv')
        return "This user is not logged-in"
    
    def buy_items(self, user, prod_id):
        if user.username in self.active_users:
            Site.value_pass(prod_id, f'{self.url}-product_ids.csv', 'product_ids', True)
            prod = ProductPrime(prod_id)
            if prod.quantity == 0:
                return "Sorry, the item is sold-out"
            prod.quantity -= 1
            user.purchase_history.append([self.url, prod_id, prod.name, prod.price])
            self.add_purchases([prod_id, prod.name, user.username, str(prod.price)])
            user.update_row()
            prod.update_row()
            return "You've purchased the item"
        return "This user is not logged-in"

    def rate_item(self, user, prod, rate, comment=None):
        if not 0 < rate <= 5:
            return "Your rate must be 1, 2, 3, 4 or 5"
        if prod.name in user.my_ratings:
            return "You have rated this product already"
        if comment != None:
            result = prod.rating(rate, [user.username, comment])
            user.my_ratings.update({prod.name: [rate, comment]})
        else:
            result = prod.rating(rate)
            user.my_ratings.update({prod.name: rate})
        user.update_row()
        return result

class SitePrime(Site):
    def __init__(self, url, active_users=[]):
        self.load_urls
        SitePrime.url_checker(url)
        self.url = url
        self.load_url_detail
        self.active_users = active_users

    def url_checker(url):
        f = open('all_urls.csv', 'r')
        with f:
            reader = csv.DictReader(f)
            for row in reader:
                if url == row['url_address']:
                    return
            raise Exception ("Url doesn't exist")