from util import Graph,Stack,Queue
import requests 
import json
import time
from functions import instantiate, inventAndCoins, pickUpTreasure, InventoryLimitReached, InventoryList, sellAndConfirm, coinsNeeded,changeName, shrinePray
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
confirmed_directions = {372: {'n': 441, 's': 363}, 441: {'s': 372}, 363: {'n': 372, 'e': 328}, 328: {'n': 332, 's': 312, 'e': 357, 'w': 363}, 332: {'n': 350, 's': 328}, 350: {'n': 436, 's': 332, 'e': 404}, 436: {'s': 350}, 404: {'n': 481, 'w': 350}, 481: {'s': 404}, 312: {'n': 328, 'e': 268}, 268: {'s': 203, 'e': 411, 'w': 312}, 203: {'n': 268, 's': 165, 'e': 299}, 165: {'n': 203, 's': 125, 'w': 204}, 125: {'n': 165, 'e': 83, 'w': '?'}, 83: {'s': 76, 'e': 130, 'w': 125}, 76: {'n': 83, 'e': 72, 'w': '?'}, 72: {'s': 63, 'w': 76}, 63: {'n': 72, 's': 20, 'w': '?'}, 20: {'n': 63, 's': 19, 'e': '?', 'w': '?'}, 19: {'n': 20, 's': 10, 'w': '?'}, 10: {'n': 19, 's': 0, 'w': '?'}, 0: {'n': 10, 's': 2, 'e': '?', 'w': '?'}, 2: {'n': 0, 's': '?', 'e': 3}, 6: {'n': 2, 'w': 7}, 7: {'n': 8, 'e': 6, 'w': 56}, 8: {'s': 7, 'w': 16}, 16: {'n': 58, 'e': 8, 'w': 67}, 58: {'s': 16, 'w': 65}, 65: {'n': 74, 'e': 58, 'w': 139}, 74: {'n': 87, 's': 65, 'w': 161}, 87: {'s': 74}, 161: {'e': 74}, 139: {'e': 65, 'w': 188}, 188: {'e': 139, 'w': 335}, 335: {'e': 188, 'w': 366}, 366: {'e': 335}, 67: {'e': 16, 'w': 162}, 162: {'e': 67}, 56: {'e': 7, 'w': 61}, 61: {'e': 56, 'w': 171}, 171: {'e': 61}, 3: {'s': 9, 'e': 5, 'w': 2}, 9: {'n': 3, 's': 12, 'e': '?'}, 12: {'n': 9, 's': '?', 'e': 14, 'w': '?'}, 18: {'n': 12, 's': 22, 'w': '?'}, 22: {'n': 18, 's': 78, 'w': '?'}, 78: {'n': 22, 's': 108}, 108: {'n': 78, 's': 117, 'e': '?'}, 117: {'n': 108, 's': 131, 'e': '?', 'w': '?'}, 131: {'n': 117, 's': 244, 'w': '?'}, 244: {'n': 131, 'e': 239}, 239: {'n': 198, 'w': 244}, 198: {'n': 166, 's': 239, 'e': '?'}, 166: {'s': 198, 'e': 150, 'w': '?'}, 150: {'n': 135, 'w': 166}, 135: {'s': 150, 'e': 106}, 106: {'n': 100, 's': '?', 'w': 135}, 100: {'s': 106, 'e': 112, 'w': 68}, 112: {'s': 141, 'e': 140, 'w': 100}, 141: {'n': 112, 'e': 156}, 156: {'s': 168, 'e': 164, 'w': 141}, 168: {'n': 156, 'e': 340}, 340: {'w': 168}, 164: {'n': 217, 'e': 298, 'w': 156}, 217: {'s': 164, 'e': 247}, 247: {'e': 261, 'w': 217}, 261: {'s': 277, 'e': 322, 'w': 247}, 277: {'n': 261, 'e': 323}, 323: {'e': 433, 'w': 277}, 433: {'s': 455, 'e': 460, 'w': 323}, 455: {'n': 433}, 460: {'w': 433}, 322: {'n': 382, 'e': 435, 'w': 261}, 382: {'s': 322, 'e': 388}, 388: {'e': 477, 'w': 382}, 477: {'e': 483, 'w': 388}, 483: {'w': 477}, 435: {'w': 322}, 298: {'s': 324, 'w': 164}, 324: {'n': 298, 's': 349, 'e': 354}, 349: {'n': 324, 's': 352, 'e': 384, 'w': 356}, 352: {'n': 349, 's': 362, 'e': 485}, 362: {'n': 352, 's': 399, 'w': 463}, 399: {'n': 362, 's': 467}, 467: {'n': 399}, 463: {'s': 468, 'e': 362}, 468: {'n': 463}, 485: {'w': 352}, 384: {'w': 349}, 356: {'e': 349}, 354: {'w': 324}, 140: {'w': 112}, 68: {'n': 52, 'e': 100}, 52: {'n': 35, 's': 68, 'e': '?'}, 35: {'s': 52, 'w': 34}, 34: {'n': 14, 's': '?', 'e': 35}, 14: {'s': 34, 'e': 37, 'w': 12}, 37: {'w': 14}, 5: {'w': 3}, 130: {'w': 83}, 411: {'w': 268}, 357: {'w': 328}, 299: {'e': 311, 'w': 203}, 311: {'w': 299}, 204: {'n': 219, 'e': 165, 'w': 216}, 219: {'s': 204}, 216: {'n': 234, 'e': 204, 'w': '?'}, 234: {'n': 368, 's': 216, 'w': 252}, 368: {'s': 234}, 252: {'n': 284, 'e': 234}, 284: {'n': 302, 's': 252, 'w': 303}, 302: {'n': 422, 's': 284}, 422: {'n': 426, 's': 302}, 426: {'n': 457, 's': 422}, 457: {'n': 461, 's': 426}, 461: {'s': 457}, 303: {'n': '?', 'e': 284, 'w': '?'}}

graph = Graph()
def move(direct):
    headers = {
    'Authorization': 'Token 6b62daaa5f05f9ea8b0b1b77a7a9a5d7f4101edb',
    'Content-Type': 'application/json',
    }

    data ='{"direction":"' +str(direct)+ '"}'
    try:
        response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)

    # print(f"Current cooldown time {response.json()}")
        print("Cooldown: ", response.json()["cooldown"], "Errors: ", response.json()["errors"], "Messages: ", response.json()["messages"])
        time.sleep(response.json()["cooldown"])
        return response.json()
    except:
        print("Room_info", graph.room_info, "\n\nDirections", graph.directions)

def wise_move(direct, next_room_id):
    print(f"WISE MOVE: {direct} to {next_room_id}")
    headers = {    'Authorization': 'Token 6b62daaa5f05f9ea8b0b1b77a7a9a5d7f4101edb',
    'Content-Type': 'application/json',
    }

    data = '{"direction":"' +str(direct)+'", "next_room_id": "'+str(next_room_id)+'"}'
    try:
        response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)
        print("Cooldown: ", response.json()["cooldown"], "Errors: ", response.json()["errors"], "Messages: ", response.json()["messages"])
        time.sleep(response.json()["cooldown"])
        return response.json()
    except:
        print("Room_info", graph.room_info, "\n\nDirections", graph.directions)


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
    shrine = None
    shop = None

    if startingRoom["title"] == "Shop":
        shop = startingRoom["room_id"]

    if startingRoom["title"] == "Wishing Well":
        global wishingWell
        wishingWell = startingRoom["room_id"]
    if startingRoom["title"] == "Shrine":
        shrine = startingRoom["room_id"]

    while stack.size() > 0:

        if shop is not None:
            print("shop", shop)
        if wishingWell is not None:
            print("wishingWell", wishingWell)
        # print("Player Stats At The Moment",inventAndCoins())
        # print("\n\ngraph.room_info", graph.room_info)
        room_id = stack.pop()
        print(f"Room {room_id}, # of rooms visited: {len(visited)}")
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
                    if room_id in confirmed_directions.keys():
                        room_directions = confirmed_directions[room_id]
                        nextRoom = wise_move(key, room_directions[key])
                    else:
                        nextRoom=move(key)
                    graph.add_vertex(nextRoom["room_id"], nextRoom["title"], nextRoom["description"], nextRoom["coordinates"], nextRoom["elevation"], nextRoom["terrain"], nextRoom["players"], nextRoom["items"], nextRoom["exits"], nextRoom["cooldown"], nextRoom["errors"], nextRoom["messages"])
                    graph.add_edge(room_id,key,nextRoom["room_id"])
                    print(nextRoom)
                    #Checks to see if the room title equals shop and if so we make the variable shop equal to the id
                    if nextRoom["title"] == "Shop":
                        shop = nextRoom["room_id"]

                    #Checks to see if the room title equals Wishing Well and if so we make the variable wishingWell equal to the id
                    if nextRoom["title"] == "Wishing Well":
                        wishingWell = nextRoom["room_id"]
                    
                    #Checks to see if room is a shrine. If it is we pray to get special powers.
                    if nextRoom["title"] == "Shrine":
                        shrine = nextRoom["room_id"]
                        shrinePray(graph)
                    
                    moved=True

                    # If the next room (the room we have just moved into) has items then we will for loop and pick up the items
                    if len(nextRoom["items"])>0:
                        if coinsNeeded()==False:

                            # Checks to see if we are carrying more than our limit or not. If we are not then we pick up items
                            inventory = inventAndCoins()
                            if inventory["encumbrance"]<8:
                                for item in nextRoom["items"]:
                                    # if item == "Small Treasure":
                                    # print("ITEM", item)
                                    pickUpTreasure(item, graph)
                                    if len(InventoryList())==8:
                                        break
                            # If we reached the limit of items we can carry and we know the shop id because we discovered it we then bfs to the shop to sell our treasure and traverse back to the nextRoom id as that was the last room we were in. The functionality is similar to what we did with the bfs when possible_directions===0
                            elif shop is not None:
                                print(shop)
                                if InventoryLimitReached()==False:
                                    for item in nextRoom["items"]:
                                        # if item == "Small Treasure":
                                        # print("ITEM", item)
                                        pickUpTreasure(item, graph)
                                        if len(InventoryList())==10:
                                            break
                                if InventoryLimitReached()==True:
                                    path_to_shop = graph.bfs(nextRoom["room_id"], shop)
                                    reverse = path_to_shop[::-1]
                                    reverse=reverse[1:]
                                    total_path = path_to_shop.extend(reverse)
                                    i=0

                                next_room_id = None
                                while i< len(total_path)-1:


                                    current_room_id = total_path[i]
                                    next_room_id = total_path[i+1]

                                    #Checks to see if the current room we are in is the one that belongs to the shop. If it is we loop through our inventory and sell our treasure.
                                    if current_room_id ==shop:
                                        inventory_list = InventoryList()
                                        for item in inventory_list:
                                            sellAndConfirm(item, graph)

                                    direction=graph.directions[current_room_id]

                                    for key in direction:
                                        if direction[key] == next_room_id:
                                            next_room = wise_move(key, next_room_id)                 
                                    if current_room_id not in visited:
                                        visited.add(item)
                                    i+=1
                    #Check to see if we have the 1,000 plus coins we need to purchase a new name.If we do and we know where the wishing well is we bfs there and change our name so we can mine. 


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
        print("directions\n", graph.directions)
    return None


count = 0
traverse(instantiate())
pickle.dump(graph.room_info, open( "roomInfo.p", "wb" ))
pickle.dump(graph.directions, open( "direction.p", "wb" ))
roomInfo = pickle.load(open("roomInfo.p", 'rb'))
direction = pickle.load(open("direction.p", 'rb'))
print("Room Info after pickle",roomInfo)
print("Direction after pickle",direction)
for i in graph.directions:
    graph.room_info[i]["directions"]=graph.directions[i]
pickle.dump(graph.room_info, open( "direcandRoom.p", "wb" ))

direcandRoom = pickle.load(open("direcandRoom.p", 'rb'))
print("direcandRoom, combining direction and room after pickle",direcandRoom)
if wishingWell is not None:
    path_to_room = graph.bfs(instantiate(), wishingWell)

    i=0
    next_room_id = None
    while i< len(path_to_room)-1:
        
        current_room_id = path_to_room[i]
        next_room_id = path_to_room[i+1]

        direction=graph.directions[current_room_id]

        for key in direction:
            if direction[key] == next_room_id:
                next_room = wise_move(key, next_room_id)               
    changeName()



