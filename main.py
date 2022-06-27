from Site import Site, SitePrime
from Account import Account, AccountPrime
from Product import Product, ProductPrime


# user1 = Account("moien_karimi", "Llllll4555555", "09115480301", "moein@gmail.com")
# site1 = Site("amazon.com")
site2 = SitePrime('amazon.com')
# # user2 = Account("mobin_karimi", "Llllll455frs555", "09215480301", "mobin@gmail.com")
user1 = AccountPrime("moien_karimi", "Llllll4555555")
# # print(AccountPrime.row_num(user1.username))
# print(site2.register(user1))
# print(AccountPrime.update_row(user1))
# print(site2.registered_use)
# # the first argumant must be password. username or email can be second or third
print(site2.login(Account.log_in("Llllll4555555", "moein@gmail.com")))
# print(site1.active_users)
# prod1 = Product("chewing gum", 23, 10000)
# prod2 = Product("butter ice cream", 2, 20000)
prod3 = ProductPrime('29002502154131')
# print(prod3.rating(5,['moein', 'amazing product']))
# print(ProductPrime.update_row(prod3))
#site2.add_product(prod3)
# site1.add_product(prod2)
site2.see_items(user1)
print(site2.buy_items(user1, '29002502154131'))
# print(site1.products)
# print(user1.purchase_history)
# print(site2.rate_item(user1, prod3, 5, "pretty good"))
# print(site1.rate_item(user1, prod2, 2, "ok"))
# print(prod2.rate)
# print(prod2.comment)
# print(user1.my_ratings)