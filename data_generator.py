import json
import random
import threading
import time

import requests
from requests_jwt import JWTAuth

apiAddress = "https://bikesharing-261122.appspot.com"

#r = requests.post("http://35.189.94.121/auth/local", data={"identifier":"cago","password":"cagdas"})

#print(r.json()["jwt"])

def user_thread(username, user_id):
    response = requests.post(apiAddress+"/auth/local",
                             data={"identifier": username, "password": "cagdas"})
    jwt = response.json()["jwt"]
    #time.sleep(random.randint(1,10))
    print(username, "sending req")
    header = {'Authorization': 'Bearer ' + jwt}
    response = requests.post(apiAddress+"/transactions/addMoney",
                             headers=header,
                             data={"userId": user_id, "amount": random.randint(5,10)})
    print("for user:", username ,response.json())

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

def main():
    #date = datetime.datetime.now(pytz.timezone('Asia/Istanbul'))
    #print(date.hour)
    number_of_active_users = 5
    users = get_users_from_db(number_of_active_users)
    print("chosen users:", users)

    for username, user_id in users:
        user_thread_conf = threading.Thread(target=user_thread(username, user_id))
        user_thread_conf.start()


if __name__ == '__main__':
    main()