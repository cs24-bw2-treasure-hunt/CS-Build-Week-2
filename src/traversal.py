from util import Graph,Stack,Queue
import requests 
import json
import time
from functions import instantiate, inventAndCoins, pickUpTreasure, InventoryLimitReached, InventoryList, sellAndConfirm, coinsNeeded,changeName,examine,shrinePray
import pickle
from hashtable import proof_of_work


def getProof():
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    }
    response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/', headers=headers)
    time.sleep(response.json()["cooldown"])
    return response.json()

def mine(new_proof):
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }
    data = json.dumps({'proof':new_proof })

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/', headers=headers, data=data)
    print("MINE AWAY", response.json())
    return response.json()

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
graph=Graph()
def move(direct):
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
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
    headers = {    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
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
                        print("SHOP ID", shop)

                    #Checks to see if the room title equals Wishing Well and if so we make the variable wishingWell equal to the id
                    if nextRoom["title"] == "Wishing Well":
                        wishingWell = nextRoom["room_id"]
                    
                    #Checks to see if room is a shrine. If it is we pray to get special powers.
                    if nextRoom["title"] == "Shrine":
                        shrinePray()
                    
                    moved=True

                    #If the next room (the room we have just moved into) has items then we will for loop and pick up the items
                    # if len(nextRoom["items"])>0:
                    #     if coinsNeeded()==False:

                    #         #Checks to see if we are carrying more than our limit or not. If we are not then we pick up items
                    #         if len(InventoryList())<8:
                    #             for item in nextRoom["items"]:
                    #                 # if item == "Small Treasure":
                    #                 # print("ITEM", item)
                    #                 pickUpTreasure(item)
                    #         #If we reached the limit of items we can carry and we know the shop id because we discovered it we then bfs to the shop to sell our treasure and traverse back to the nextRoom id as that was the last room we were in. The functionality is similar to what we did with the bfs when possible_directions===0
                    #         elif shop is not None:
                    #             if InventoryLimitReached()==False:
                    #                 for item in nextRoom["items"]:
                    #                     # if item == "Small Treasure":
                    #                     # print("ITEM", item)
                    #                     pickUpTreasure(item)
                    #                     if len(InventoryList())==10:
                    #                         break
                    #             if InventoryLimitReached()==True:
                    #                 path_to_shop = graph.bfs(nextRoom["room_id"], shop)
                    #                 reverse = path_to_shop[::-1]
                    #                 reverse=reverse[1:]
                    #                 total_path = path_to_shop.extend(reverse)
                    #                 i=0

                    #             next_room_id = None
                    #             while i< len(total_path)-1:


                    #                 current_room_id = total_path[i]
                    #                 next_room_id = total_path[i+1]

                    #                 #Checks to see if the current room we are in is the one that belongs to the shop. If it is we loop through our inventory and sell our treasure.
                    #                 if current_room_id ==shop:
                    #                     inventory_list = InventoryList()
                    #                     for item in inventory_list:
                    #                         sellAndConfirm(item)

                    #                 direction=graph.directions[current_room_id]

                    #                 for key in direction:
                    #                     if direction[key] == next_room_id:
                    #                         next_room = wise_move(key, next_room_id)                 
                    #                 if current_room_id not in visited:
                    #                     visited.add(item)
                    #                 i+=1
                    # #Check to see if we have the 1,000 plus coins we need to purchase a new name.If we do and we know where the wishing well is we bfs there and change our name so we can mine. 


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
                    visited.add(current_room_id)
                i+=1
            stack.push(next_room_id)
        print("These are the rooms we have visited with directions\n", len(visited))
    return None


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
# print("Player Stats At The Moment",inventAndCoins())

print(len(graph.directions))
rooms_left_directions= [131,9, 18, 230, 25, 11, 17, 24, 42, 44, 80, 81, 86, 96, 97, 181, 90, 178, 209, 243, 293, 256, 360, 398, 438, 465, 498, 327, 427, 430, 443, 471, 439, 118, 137, 321]
# print("instantiate",instantiate())
# path_to_room = graph.bfs(instantiate()['room_id'], 131)
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

# for x in rooms_left_directions:
#     print(x,instantiate()['room_id'])
#     if type(int) in  graph.directions[instantiate()['room_id']].keys():
#         path_to_room = graph.bfsAfter(instantiate()['room_id'], x)
#         print("path_to_room",path_to_room)
#         i=0
#         next_room_id = None
   
#         while i< len(path_to_room)-1:
        
#             current_room_id = path_to_room[i]
#             next_room_id = path_to_room[i+1]

#             direction=graph.directions[current_room_id]

#             for key in direction:
#                 print("direction[key]",direction[key],next_room_id)
#                 if direction[key] == next_room_id:
#                     next_room = wise_move(key, next_room_id)   
#             print("instantiate inside while loop",instantiate()["room_id"])   
#             i+=1
#     exits = graph.directions[instantiate()['room_id']]
#     room_id=instantiate()['room_id']
#     possible_directions = 0
#     moved=False
#     for key in exits:
#         print("here")
            
#         #This handle an unexplored room thus "?"
#         if exits[key] =="?":
#             print("INSIDE")
#             nextRoom=move(key)
            
#             graph.add_vertex(nextRoom["room_id"], nextRoom["title"], nextRoom["description"], nextRoom["coordinates"], nextRoom["elevation"], nextRoom["terrain"], nextRoom["players"], nextRoom["items"], nextRoom["exits"], nextRoom["cooldown"], nextRoom["errors"], nextRoom["messages"])
#             graph.add_edge(room_id,key,nextRoom["room_id"])
     
#     print("LENGTH",len(graph.directions),graph.directions)


# while coinsNeeded()==False:
#     print("here", instantiate()["room_id"])
#     room_id=instantiate()["room_id"]
#     exits = graph.directions[room_id]
#     for key in exits:  
#         nextRoom=move(key)
#         print("key", key)
#         if len(nextRoom["items"])>0:
#             for item in nextRoom["items"]:
#                 pickUpTreasure(item)
#                 print(len(inventAndCoins()["inventory"]))
#         break

# TRAVERSE TO SHOP
# print("OUTSIDE OF WHILE LOOP", len(inventAndCoins()["inventory"]))
# print("instantiate",instantiate())
# path_to_room = graph.bfs(instantiate()['room_id'], 1)
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

# for i in inventAndCoins()["inventory"]:
#     sellAndConfirm(i)


#TRAVERSE TO PIRATE RY
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

#TRAVERSE TO SHRINE
# path_to_room = graph.bfs(instantiate()['room_id'], 374)
# print("path_to_room",instantiate(),path_to_room)
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
# shrinePray()

#TRAVERSE TO WISHING WELL
# path_to_room = graph.bfs(instantiate()['room_id'], 55)
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

# examine()

#Traverse to the room returned by the binaries
path_to_room = graph.bfs(instantiate()['room_id'], 185)
print("path_to_room",instantiate(),path_to_room)
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

print("proof of work",mine(proof_of_work(getProof()["proof"],difficulty)))
