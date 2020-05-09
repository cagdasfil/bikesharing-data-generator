import json
import random
import threading
import time

import requests
from requests_jwt import JWTAuth

apiAddress = "https://bikesharing-261122.appspot.com"

#r = requests.post("http://35.189.94.121/auth/local", data={"identifier":"cago","password":"cagdas"})

#print(r.json()["jwt"])

def usage_thread(username, user_id):
    response = requests.post(apiAddress+"/auth/local",
                             data={"identifier": username, "password": "cagdas"})
    jwt = response.json()["jwt"]


    time.sleep(random.randint(1,5))
    print(username, "sending add money req")
    header = {'Authorization': 'Bearer ' + jwt}
    payload = {"userId": user_id, "amount": random.randint(20,25)}
    print(payload)
    response = requests.post(apiAddress+"/transactions/addMoney",
                             headers=header,
                             json=payload)
    print("for user:", username ,response.json())


    time.sleep(random.randint(1,5))
    print(username, "sending start session req")
    response = requests.post(apiAddress + "/usages/startSession",
                             headers=header,
                             json={"bikeId": "5eb173ecfc13ae681e000011",
                                   "userId": user_id,
                                   "lastZoneId": "5e8b17a68ffd1f13d88234d5",
                                   "location": [32.7840346, 39.907613]})
    print("for user:", username ,response.json())


    time.sleep(random.randint(1, 5))
    print(username, "sending end session req")
    response = requests.post(apiAddress + "/usages/endSession",
                             headers=header,
                             json={"userId": user_id, "location": [32.7840346, 39.907613]})
    print("for user:", username, response.json())

def get_users_from_db(number_of_active_users):
    users_file = open("users","r")
    user_line = users_file.readline()
    users=[]
    while user_line:
        users.append([json.loads(user_line.strip())["username"],json.loads(user_line.strip())["_id"]["$oid"]])
        user_line = users_file.readline()
    print(len(users))
    users_file.close()
    return random.choices(users, k=number_of_active_users)

def get_bikes_from_db(number_of_active_users):
    bikes_file = open("bikes","r")
    bike_line = bikes_file.readline()
    bikes=[]
    while bike_line:
        bikes.append([json.loads(bike_line.strip())["_id"]["$oid"],json.loads(bike_line.strip())["lastZoneId"]])
        bike_line = bikes_file.readline()
    print(len(bikes))
    bikes_file.close()
    return random.choices(bikes, k=number_of_active_users)

def main():
    #date = datetime.datetime.now(pytz.timezone('Asia/Istanbul'))
    #print(date.hour)
    number_of_active_users = 1
    users = get_users_from_db(number_of_active_users)
    bikes = get_bikes_from_db(number_of_active_users)
    print("chosen users:", users)
    print("chosen bikes:", bikes)

    for username, user_id in users:
        usage_thread_conf = threading.Thread(target=usage_thread(username, user_id))
        usage_thread_conf.start()



if __name__ == '__main__':
    main()