import requests 
import json
import time

def inventAndCoins():
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/status/', headers=headers)
    return response.json()

def CarryLimit():
    Inventory=inventAndCoins()
    return Inventory["strength"]
def InventoryList():
    Inventory=inventAndCoins()
    return Inventory["inventory"]
def InventoryLimitReached():
    if len(InventoryList())==CarryLimit():
        return True
    else:
        return False
def coinsNeeded():
    Inventory=inventAndCoins()
    if Inventory.gold >=1000:
        return True
    else:
        return False
def coinsCarried():
    Inventory=inventAndCoins()
    return Inventory.gold

def sellAndConfirm(treasure):
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }

    data = '{"name":f"{treasure}"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', headers=headers, data=data)
    print(response.json().messages)
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }

    data = '{"name":f"{treasure}", "confirm":"yes"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/sell/', headers=headers, data=data)
    return coinsCarried()

def pickUpTreasure(treasure):
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }

    data ='{"name":"' +str(treasure)+ '"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/take/', headers=headers, data=data)
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