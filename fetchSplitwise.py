import sys
import configparser
import requests
import json
from dataclasses import dataclass

jsondata = []
parser = configparser.RawConfigParser()
parser.read("config.ini")
if (len(sys.argv) == 1):
    endpoint = parser.get("config", "endpoint")
    cookie = parser.get("config", "cookie")
    requestHeaders = {'Cookie' : cookie}

    response = requests.get(endpoint, headers=requestHeaders)
    if (response.status_code != 200):
        print("There is a problem with the response!")
        print(response.json())
        quit()
    else:
        print("Server response has been successfully received!")
        f = open("output.json", "a")
        jsondata = json.dumps(response.json())
        f.write(jsondata)
        f.close()
else:
    f = open(sys.argv[1], "r")
    jsondata = f.read()
    f.close()

splitwiseUserId = int(parser.get("config", "splitwise_userid"))

@dataclass
class Expense:
    id          : int
    cost        : float
    description : str
    date        : str
    category    : str

personalExpenses = []
expenses = json.loads(jsondata)["expenses"]
for expense in expenses:
    users = expense["users"]
    for user in users:
        if user["user_id"] == splitwiseUserId and float(user["owed_share"]) != 0.0:
            personalExpenses.append(
                Expense(
                    id          = expense["id"],
                    cost        = float(user["owed_share"]),
                    description = expense["description"],
                    date        = expense["date"],
                    category    = expense["category"]["name"]
                ))
            break

totalPersonalExpense = sum(expense.cost for expense in personalExpenses)
print(totalPersonalExpense)
