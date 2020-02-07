import requests 
import json
import time


def instantiate():
    headers = {
    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
        }

    response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)

    time.sleep(response.json()["cooldown"])
    return response.json()

def inventAndCoins():
    headers = {
    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
    'Content-Type': 'application/json',
    }

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', headers=headers)
    return response.json()

# def CarryLimit(inventory = None):
#     if inventory is None:
#         inventory=inventAndCoins()
#     return inventory["strength"]
def InventoryList(inventory = None):
    if inventory==None:
        inventory=inventAndCoins() 
    return inventory["inventory"]

def InventoryLimitReached(inventory = None):
    inventory=inventAndCoins()
    if len(inventory["inventory"])==inventory["strength"]:
        return True 
    else:
        return False

def coinsNeeded(inventory = None):
    inventory=inventAndCoins()
    if inventory["gold"] >=1000:
        return True
    else:
        return False

def sellAndConfirm(treasure):
    headers = {
        'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
        'Content-Type': 'application/json',}
    data = '{"name":"' +str(treasure)+'", "confirm":"yes"}'
    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', headers=headers, data=data)
    print("treasure sold", response.json())
    time.sleep(response.json()["cooldown"])

def pickUpTreasure(treasure):
    headers = {
    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
    'Content-Type': 'application/json',
    }

    data ='{"name":"' +str(treasure)+ '"}'
    response =requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=headers, data=data)
    time.sleep(response.json()["cooldown"])
    return response.json

def dropTreasure(treasure):
    headers = {
    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
    'Content-Type': 'application/json',
    }

    data = '{"name":f"{treasure}"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/', headers=headers, data=data)
    
    return response.json()

def wearEquipment(Equipment):
    headers = {
    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
    'Content-Type': 'application/json',
    }

    data = '{"name":"[f"{Equipment}"]"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/wear/', headers=headers, data=data)
    print("Wear Equipment",  response.json())

def dropEquipment(Equipment):
    headers = {
    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
    'Content-Type': 'application/json',
    }

    data = '{"name":"[f"{Equipment}"]"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/undress/', headers=headers, data=data)
    print("Drop Equipment", response.json())

def changeName():
    headers={
    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
    'Content-Type': 'application/json',
    }

    data = '{"name":"[Jade Lopez]", "confirm":"aye"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/', headers=headers, data=data)
    print("Change Name",response.json())

def shrinePray():
    headers = {
    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
    'Content-Type': 'application/json',
    }

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/', headers=headers)
    print("Shrine Pray", response.json())

def examine():
    headers = {
        'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
        'Content-Type': 'application/json',
        }
    # data ='{"name":"[' +str(spmcdonnell)+ ']"}'
    data='{"name": "well"}'
    print("data",data)
    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/examine/', headers=headers, data=data)
    time.sleep(response.json()["cooldown"])
    print("Examine", response.json() )

def getProof():
    headers = {
    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
    }
    response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/', headers=headers)
    time.sleep(response.json()["cooldown"])
    return response.json()

def mine(new_proof):
    headers = {
    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
    'Content-Type': 'application/json',
    }
    data = json.dumps({'proof':new_proof })
    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/', headers=headers, data=data)
    print("MINE AWAY", response.json())
    return response.json()
