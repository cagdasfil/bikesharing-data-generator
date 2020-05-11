import json
import random
import threading
import time
import requests
import datetime
import pytz

apiAddress = "https://bikesharing-261122.appspot.com"
zonePoints = {
    "5e8b17a68ffd1f13d88234d5" : [32.7840346, 39.907613],
    "5e9dbe5f1c9d44000063fbe3" : [32.7833453, 39.8926391],
    "5e9dbe901c9d44000063fbe4" : [32.793425, 39.891464],
    "5e9dbf191c9d44000063fbe5" : [32.77587, 39.8975965],
    "5eb15e0675a718000a67e8e8" : [32.7775329, 39.8867738],
    "5eb15f2175a718000a67e8e9" : [32.7896351, 39.8894925],
    "5eb15fe475a718000a67e8ea" : [32.7816823, 39.9004917],
    "5eb160c875a718000a67e8eb" : [32.7831441, 39.8968742]
}

def usage_thread(username, userId, bikeId, startZoneId, endZoneId):

    # User logs in and retrieves jwt token
    time.sleep(random.randint(5, 120))
    header = login(username)

    # User starts a session
    time.sleep(random.randint(60,30*60))
    status = start_session(header, userId, bikeId, startZoneId)
    # User loads money until starting a session
    i=0
    while status!=200 and i<2:
        # User loads money on its account
        time.sleep(random.randint(5, 60))
        load_money(header, userId, random.randint(5, 25))
        # User starts a session
        time.sleep(random.randint(5, 60))
        status = start_session(header, userId, bikeId, startZoneId)
        i+=1

    # Usage time
    time.sleep(random.randint(5*60, 75*60))

    # User ends the session
    end_session(header, userId, endZoneId)

def login(username):
    response = requests.post(apiAddress + "/auth/local",
                             data={"identifier": username, "password": "cagdas"})
    print("==>", username, response.json())
    jwt = response.json()["jwt"]
    header = {'Authorization': 'Bearer ' + jwt}
    return header

def load_money(header, userId, amount):
    print(userId, "sending add money req")
    response = requests.post(apiAddress + "/transactions/addMoney",
                             headers=header,
                             json={"userId": userId, "amount": amount})
    print("for user:", userId, response.json())

def start_session(header, userId, bikeId, lastZoneId):
    print(userId, "sending start session req")
    response = requests.post(apiAddress + "/usages/startSession",
                             headers=header,
                             json={"bikeId": bikeId,
                                   "userId": userId,
                                   "lastZoneId": lastZoneId,
                                   "location": zonePoints[lastZoneId]})
    print("for user:", userId, response.json())
    return response.json()["status"]

def end_session(header, userId, endZoneId):
    print(userId, "sending end session req")
    response = requests.post(apiAddress + "/usages/endSession",
                             headers=header,
                             json={"userId": userId, "location": zonePoints[endZoneId]})
    print("for user:", userId, response.json())

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
    return random.choices(bikes, k=(number_of_active_users*2))

def main():

    for i in range(50):
        date = datetime.datetime.now(pytz.timezone('Asia/Istanbul'))

        if 0 < date.hour < 1:
            number_of_active_users = 20
        elif 1 < date.hour < 2:
            number_of_active_users = 15
        elif 2 < date.hour < 7:
            number_of_active_users = 5
        elif 7 < date.hour < 8:
            number_of_active_users = 30
        elif 8 < date.hour < 9:
            number_of_active_users = 50
        elif 9 < date.hour < 11:
            number_of_active_users = 30
        elif 11 < date.hour < 13:
            number_of_active_users = 60
        elif 13 < date.hour < 16:
            number_of_active_users = 30
        elif 16 < date.hour < 19:
            number_of_active_users = 40
        elif 19 < date.hour < 23:
            number_of_active_users = 25
        else :
            number_of_active_users = 15

        users = get_users_from_db(number_of_active_users)
        bikes = get_bikes_from_db(number_of_active_users)

        print("chosen active users:", users)
        print("chosen active bikes:", bikes)

        threads = []
        for i in range(len(users)):
            usage_thread_conf = threading.Thread(
                target=usage_thread,
                args=(users[i][0], users[i][1], bikes[i][0], bikes[i][1], bikes[i+number_of_active_users][1]))
            threads.append(usage_thread_conf)

        print("threads starting")

        for t in range(len(threads)):
            print(t, "started")
            threads[t].start()
            if t%10 == 9:
                time.sleep(60)

        print("threads started")

        for t in threads:
            t.join()

if __name__ == '__main__':
    main()