from util import Graph,Stack,Queue
import requests 
import json
import time
from functions import instantiate, inventAndCoins, pickUpTreasure, InventoryLimitReached, InventoryList, sellAndConfirm, coinsNeeded,changeName, shrinePray, examine, getProof, mine
from hashtable import *

import pickle


"""
    To-Do:
        - Traversal path (Big Array) ==>will need to hold the data from the rooms, online SQL. [tonight]
        - Note where the wishing well is. [Need to figure this out]
        - Wishing well => Change name
        - mine coin (blockchain, hashtable)
        - Nice Additions:
            - Shrine to get abilities:
                - Fly
                - Dash
            - Pick up equipment & Drop
            - Ghost thing
    
    - DFT => Traverse [WIP]
    - BFS => Shortest paths [WIP]

    DONE:
        - Cool Down Time [DONE]
        - Inventory (limit of how many items we can carry) [DONE]
            - treasure or other items that could help in the rooms
        - 1,000+ coins go to the wishing well (if we know where it is, if not search for it).
          Once found do action there (change name) [Done]
        - Note where the shop is to sell the treasure => BFS back to here everytime
          our inventory is full or over a limit we set (70%) [Done]
        - Once we hit a dead end go back to the nearest room that has not been
          visited. [Done]
        - Add new rooms to graphs with the edges  [Done]
        - Save information in the other vertex in the graph [Done]


    
"""


graph = Graph()
def move(direct):
    headers = {
    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
    'Content-Type': 'application/json',
    }

    data ='{"direction":"' +str(direct)+ '"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)

    # print(f"Current cooldown time {response.json()}")
    time.sleep(response.json()["cooldown"])
    if response.json()["errors"]==True:
        # print("ERRORRRR",response.json()["errors"])
        return
    return response.json()

def wise_move(direct, next_room_id):
    # print("inside WISE MOVE, next_room_id", next_room_id)
    headers = {    'Authorization': 'Token d03435f93859f57fed07afb0ba1d83491ffab7b4',
    'Content-Type': 'application/json',
    }

    data = '{"direction":"' +str(direct)+'", "next_room_id": "'+str(next_room_id)+'"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)
    
    time.sleep(response.json()["cooldown"])
    if response.json()["errors"]==True:
        # print("ERRORRRR",response.json()["errors"])
        return
    return response.json()


wishingWell=None
def traverse(startingRoom):
    #startingRoom represents the room we are currently in as a player. It is coming from the instantiation function in the function file.


    # Will hold path so we can push and pop.
    stack = Stack() 

    # path=[] # Will hold room id
    # Will hold room id of rooms with unvisited directions so we can traverse back to them once we hit a dead end.
    additional_option = Stack() 

    # Will hold the ids of the rooms we visited so we can make sure we hit 500 unique rooms then break.
    visited = set() 

    #Instantiates and gives us our first room in the stack.
    stack.push(startingRoom["room_id"]) 

    
    graph.add_vertex(startingRoom["room_id"], startingRoom["title"], startingRoom["description"], startingRoom["coordinates"], startingRoom["elevation"], startingRoom["terrain"], startingRoom["players"], startingRoom["items"], startingRoom["exits"], startingRoom["cooldown"], startingRoom["errors"], startingRoom["messages"])

    shop = None

    if startingRoom["title"] == "Shop":
        shop = startingRoom["room_id"]

    if startingRoom["title"] == "Wishing Well":
        wishingWell = startingRoom["room_id"]

    while stack.size() > 0:
        # print("Player Stats At The Moment",inventAndCoins())

        room_id = stack.pop()

        if room_id not in visited:
            # print(f"Room {room_id} added to visited")
            visited.add(room_id)

        if len(visited) == 500:
            # return path
            return
        exits = graph.directions[room_id]
        possible_directions = 0
        moved=False
        for key in exits:
            
            #This handle an unexplored room thus "?"
            if exits[key] =="?":

                #possible_directions adds the amount of question marks per direction a node has
                possible_directions +=1

                #This moves us to one of the rooms that is unexplored and adds it to the vertices and adds the edges.
                if moved==False:
                    nextRoom=move(key)
                    
                    graph.add_vertex(nextRoom["room_id"], nextRoom["title"], nextRoom["description"], nextRoom["coordinates"], nextRoom["elevation"], nextRoom["terrain"], nextRoom["players"], nextRoom["items"], nextRoom["exits"], nextRoom["cooldown"], nextRoom["errors"], nextRoom["messages"])
                    graph.add_edge(room_id,key,nextRoom["room_id"])

                    #Checks to see if the room title equals shop and if so we make the variable shop equal to the id
                    if nextRoom["title"] == "Shop":
                        shop = nextRoom["room_id"]

                    #Checks to see if the room title equals Wishing Well and if so we make the variable wishingWell equal to the id
                    if nextRoom["title"] == "Wishing Well":
                        wishingWell = nextRoom["room_id"]
                    
                    #Checks to see if room is a shrine. If it is we pray to get special powers.
                    if nextRoom["title"] == "Shrine":
                        shrinePray()
                    
                    moved=True
                    stack.push(nextRoom["room_id"])        

        #This adds a room id to additional_option since it has a direction with a question mark
        if possible_directions > 1:
            additional_option.push(room_id)

        #Below part triggers BFS since we now hit a dead end.
        if possible_directions == 0:
            return_room = additional_option.pop()
            path_to_room = graph.bfs(room_id, return_room)

            i=0
            next_room_id = None
            while i< len(path_to_room)-1:
                
                current_room_id = path_to_room[i]
                next_room_id = path_to_room[i+1]

                direction=graph.directions[current_room_id]

                for key in direction:
                    if direction[key] == next_room_id:
                        next_room = wise_move(key, next_room_id)               
                if current_room_id not in visited:
                    visited.add(item)
                i+=1
            stack.push(next_room_id)
        # print("These are the rooms we have visited with directions\n", graph.room_info)
    return None


count = 0
# traverse(instantiate())
# pickle.dump(graph.room_info, open( "roomInfo.p", "wb" ))
# pickle.dump(graph.directions, open( "direction.p", "wb" ))
# roomInfo = pickle.load(open("roomInfo.p", 'rb'))
# direction = pickle.load(open("direction.p", 'rb'))
# print("Room Info after pickle",roomInfo)
# print("Direction after pickle",direction)
# for i in graph.directions:
#     graph.room_info[i]["directions"]=graph.directions[i]
# pickle.dump(graph.room_info, open( "direcandRoom.p", "wb" ))

# direcandRoom = pickle.load(open("direcandRoom.p", 'rb'))
# print("direcandRoom, combining direction and room after pickle",direcandRoom)
# if wishingWell is not None:
#     path_to_room = graph.bfs(instantiate(), wishingWell)
#     print("Wishing Well",path_to_room)

#     i=0
#     next_room_id = None
#     while i< len(path_to_room)-1:
        
#         current_room_id = path_to_room[i]
#         next_room_id = path_to_room[i+1]

#         direction=graph.directions[current_room_id]

#         for key in direction:
#             if direction[key] == next_room_id:
#                 next_room = wise_move(key, next_room_id)               
    # changeName()


#TRAVERSE TO SHOP
# path_to_room = graph.bfs(instantiate()['room_id'], 1)
# print("path_to_room",instantiate())
# i=0
# next_room_id = None
# while i< len(path_to_room)-1:
#     current_room_id = path_to_room[i]
#     next_room_id = path_to_room[i+1]
#     direction=graph.directions[current_room_id]
#     for key in direction:
#         print("direction[key]",direction[key],next_room_id)
#         if direction[key] == next_room_id:
#             next_room = wise_move(key, next_room_id)   
#     print("instantiate inside while loop",instantiate()["room_id"])   
#     i+=1
# for i in inventAndCoins()["inventory"]:
#     sellAndConfirm(i)

# # TRAVERSE TO PIRATE RY
# path_to_room = graph.bfs(instantiate()['room_id'], 467)
# print("path_to_room",path_to_room)
# i=0
# next_room_id = None
# while i< len(path_to_room)-1:
#     current_room_id = path_to_room[i]
#     next_room_id = path_to_room[i+1]
#     direction=graph.directions[current_room_id]
#     for key in direction:
#         print("direction[key]",direction[key],next_room_id)
#         if direction[key] == next_room_id:
#             next_room = wise_move(key, next_room_id)   
#     print("instantiate inside while loop",instantiate()["room_id"])   
#     i+=1
# changeName()

# TRAVERSE TO WISHING WELL
# path_to_room = graph.bfs(instantiate()['room_id'], 55)
# print("path_to_room",path_to_room)
# i=0
# next_room_id = None
# while i< len(path_to_room)-1:
#     current_room_id = path_to_room[i]
#     next_room_id = path_to_room[i+1]
#     direction=graph.directions[current_room_id]
#     for key in direction:
#         print("direction[key]",direction[key],next_room_id)
#         if direction[key] == next_room_id:
#             next_room = wise_move(key, next_room_id)   
#     print("instantiate inside while loop",instantiate()['room_id'])   
#     i+=1
# examine()
# print("Description", graph.room_info)


# TRAVERSE TO MINE COIN
path_to_room = graph.bfs(instantiate()['room_id'], 368)
print("path_to_room",path_to_room)
i=0
next_room_id = None
while i< len(path_to_room)-1:
    current_room_id = path_to_room[i]
    next_room_id = path_to_room[i+1]
    direction=graph.directions[current_room_id]
    for key in direction:
        print("direction[key]",direction[key],next_room_id)
        if direction[key] == next_room_id:
            next_room = wise_move(key, next_room_id)   
    print("instantiate inside while loop",instantiate()["room_id"])   
    i+=1

difficulty=6
mine(proof_of_work(getProof()['proof'],difficulty))

# print("proof of work",mine(proof_of_work(getProof()['proof'],difficulty)))