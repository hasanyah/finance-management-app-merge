import sys
import configparser
import requests
import json
from dataclasses import dataclass

@dataclass
class Category:
    id          : int
    name        : str

@dataclass
class Account:
    id          : int
    book_id     : int
    name        : str
    balance     : float
    unit        : str

@dataclass
class Expense:
    id          : int
    account_id  : int
    amount      : float
    description : str
    date        : str
    type        : str
    category_id : int

def get(endpoint, cookie, outputFilename):
    requestHeaders = {'Cookie' : cookie}
    response = requests.get(endpoint, headers=requestHeaders)
    if (response.status_code != 200):
        print("There is a problem with the response from {}!".format(endpoint))
        print(response.json())
        quit()
    else:
        f = open(outputFilename, "a")
        jsondata = json.dumps(response.json())
        f.write(jsondata)
        f.close()
        return jsondata

def getAccounts():
    accountsJson = []
    if (len(sys.argv) >= 2):
        f = open(sys.argv[1], "r")
        accountsJson = f.read()
        f.close()
    else:
        endpoint = parser.get("accountbook", "account_endpoint")
        cookie = parser.get("accountbook", "cookie")
        accountsJson = get(endpoint, cookie, "accountbook_output.json")

    accounts = []
    details = json.loads(accountsJson)["account"]
    for account in details:
        accounts.append(Account(
            id      = int(account["id"]),
            book_id = int(account["book_id"]),
            name    = account["name"],
            balance = float(account["balance"]["total"]),
            unit    = account["unit"]["symbol_global"]
        ))
    return accounts

def getCategories():
    categoriesJson = []
    if (len(sys.argv) >= 3):
        f = open(sys.argv[2], "r")
        categoriesJson = f.read()
        f.close()
    else:
        endpoint = parser.get("accountbook", "category_endpoint")
        cookie = parser.get("accountbook", "cookie")
        categoriesJson = get(endpoint, cookie, "accountbook_category_output.json")

    categories = []
    details = json.loads(categoriesJson)["category"]
    for category in details:
        if ("hidden" in category and int(category["hidden"]) == 1) or ("hide" in category and int(category["hide"]) == 1):
            continue

        categories.append(Category(
            id      = int(category["id"]),
            name    = category["name"]
        ))
    return categories

def getExpenses():
    expensesJson = []
    if (len(sys.argv) >= 4):
        f = open(sys.argv[3], "r")
        expensesJson = f.read()
        f.close()
    else:
        endpoint = parser.get("accountbook", "expenses_endpoint")
        cookie = parser.get("accountbook", "cookie")
        expensesJson = get(endpoint, cookie, "accountbook_expenses_output.json")

    # expenses = []
    # details = json.loads(expensesJson)["category"]
    # for expense in details:
    #     if ("hidden" in category and int(category["hidden"]) == 1) or ("hide" in category and int(category["hide"]) == 1):
    #         continue

    #     expenses.append(Category(
    #         id      = int(category["id"]),
    #         name    = category["name"]
    #     ))
    return expensesJson

parser = configparser.RawConfigParser()
parser.read("config.ini")

accounts = getAccounts()
categories = getCategories()
expenses = getExpenses()

for ex in expenses:
    print(ex)
