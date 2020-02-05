import requests 
import json
import time


def instantiate():
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
        }

    response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)

    time.sleep(response.json()["cooldown"])
    return response.json()

def inventAndCoins():
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
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
        'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
        'Content-Type': 'application/json',}
    data = '{"name":"' +str(treasure)+'", "confirm":"yes"}'
    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', headers=headers, data=data)
    print("treasure sold", response.json())
    time.sleep(response.json()["cooldown"])

def pickUpTreasure(treasure):
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }

    data ='{"name":"' +str(treasure)+ '"}'
    response =requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=headers, data=data)
    time.sleep(response.json()["cooldown"])
    return response.json

def dropTreasure(treasure):
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }

    data = '{"name":f"{treasure}"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/drop/', headers=headers, data=data)
    
    return response.json()

def wearEquipment(Equipment):
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }

    data = '{"name":"[f"{Equipment}"]"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/wear/', headers=headers, data=data)
    print("Wear Equipment",  response.json())

def dropEquipment(Equipment):
    headers = {
    'Authorization': 'Token 7a375b52bdc410eebbc878ed3e58b2e94a8cb607',
    'Content-Type': 'application/json',
    }

    data = '{"name":"[f"{Equipment}"]"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/undress/', headers=headers, data=data)
    print("Drop Equipment", response.json())

def changeName():
    headers={
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }

    data = '{"name":"[Obaida Albaroudi]"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/change_name/', headers=headers, data=data)
    print("Change Name",response.json())

def shrinePray():
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/pray/', headers=headers)
    print("Shrine Pray", response.json())