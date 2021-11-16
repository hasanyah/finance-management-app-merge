import sys
import configparser
import requests
import json

jsondata = []
if (len(sys.argv) == 1):
    parser = configparser.RawConfigParser()
    parser.read("config.ini")
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
        jsondata = f.write(json.dumps(response.json()))
        f.close()
else:
    f = open(sys.argv[1], "r")
    jsondata = f.read()
    f.close()

print(jsondata)
