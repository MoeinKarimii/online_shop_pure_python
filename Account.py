import re, hashlib, csv, pandas as pd


class Account:
    def __init__(self, username, password, phone_number, email):
        self.load_account()
        pattern = "[a-z A-Z]+_+[a-z A-Z]"
        if re.match(pattern, username):
            Account.username_pass(username)
            self.username = username
        else:
            raise Exception("invalid username")

        pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\W]{8,}$"
        if re.match(pattern, password):
            self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        else:
            raise Exception("invalid password")

        pattern1 = "^09\d{9}$"
        pattern2 = "^\+989\d{9}$"
        if re.match(pattern1, phone_number):
            self.phone_number = phone_number
        elif re.match(pattern2, phone_number):
            self.phone_number = "0" + phone_number[2:]
        else:
            raise Exception("invalid phone number")

        pattern = "^([\w\.\_\-]+)@([\w\-\_]+)((\.([A-Za-z]){2,5})+)$"
        if re.match(pattern, email):
            Account.email_pass(email)
            self.email = email
        else:
            raise Exception("invalid email")
        self.purchase_history = []
        self.my_ratings = {}
        self.save_account()
        
    def save_account(self):
        f = open('all_accounts.csv', 'a')
        with f:
            
            fnames = ['username', 'password', 'phone_number', 'email', 'purchase_history', 'my_ratings']
            writer = csv.DictWriter(f, fieldnames=fnames)    

            # writer.writeheader()
            writer.writerow({'username' : self.username, 'password': self.password, 'phone_number': self.phone_number, 'email': self.email, 'purchase_history': self.purchase_history, 'my_ratings': self.my_ratings})
        return "Account saved successfully!"
     
    def load_account(self):
        try:
            with open('all_accounts.csv', 'r'):
                pass
        except:
            f = open('all_accounts.csv', 'w')
            with f:
                fnames = ['username', 'password', 'phone_number', 'email', 'purchase_history', 'my_ratings']
                writer = csv.DictWriter(f, fieldnames=fnames)    
                writer.writeheader()


    @staticmethod
    def username_pass(username, exists=False):
        f = open('all_accounts.csv', 'r')
        with f:
            reader = csv.DictReader(f)
            for row in reader:
                if username == row['username']:
                    if exists == True:
                        return True
                    raise Exception ("User already exists")
            if exists == True:
                raise Exception ("User doesn't exist")

    @staticmethod
    def email_pass(email, exists=False):
        f = open('all_accounts.csv', 'r')
        with f:
            reader = csv.DictReader(f)
            for row in reader:
                if email != row['email']:
                    return True
                raise Exception ("User already exists")

    @staticmethod
    def log_in(password, username=None, email=None):
        if username != None and email != None and password != None:
            return ({"password": password, "username": username, "email": email})

        elif password != None and username != None and email == None:
            if "@" in username:
                email = username
                return ({"password": password, "email": email})
            else:
                return ({"password": password, "username": username})

class AccountPrime:
    def __init__(self, username, password):
        row = AccountPrime.validation_checker(username, password)
        self.username = row['username']
        self.password = row['password']
        self.phone_number = row['phone_number']
        self.email = row['email']
        self.purchase_history = eval(row['purchase_history'])
        self.my_ratings = eval(row['my_ratings'])

    @staticmethod
    def validation_checker(username, password, hashed=False):
        if hashed == False:
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        f = open('all_accounts.csv', 'r')
        with f:
            reader = csv.DictReader(f)
            for row in reader:
                if username == row['username'] and password == row['password']:
                    return row
            raise Exception ("username and password are not match")

    def row_num(username):
        f = open('all_accounts.csv', 'r')
        with f:
            reader = csv.DictReader(f)
            for row in reader:
                if username == row['username']:
                    return reader.line_num - 2
    
    def update_row(user):
        row_id = AccountPrime.row_num(user.username)
        df = pd.read_csv('all_accounts.csv')
        df.at[row_id, 'username'] = user.username
        df.at[row_id, 'password'] = user.password
        df.at[row_id, 'phone_number'] = str(user.phone_number)
        df.at[row_id, 'email'] = user.email
        df.at[row_id, 'purchase_history'] = str(user.purchase_history)
        df.at[row_id, 'my_ratings'] = str(user.my_ratings)
        df.to_csv('all_accounts.csv', index=False)
