from util import Graph,Stack,Queue
import requests 
import json
import time
from functions import inventAndCoins,pickUpTreasure,InventoryLimitReached

"""
    Take into Account:
        - Cool Down Time [DONE]
        - Inventory (limit of how many items we can carry) [tonight]
            - treasure or other items that could help in the rooms
        - 1,000+ coins go to the wishing well (if we know where it is, if not search for it).
          Once found do action there (change name) [tonight]

    Directions:
        - Traversal path (Big Array) ==>will need to hold the data from the rooms, online SQL. [tonight]

        - Note where the shop is to sell the treasure => BFS back to here everytime
          our inventory is full or over a limit we set (70%)
        - Note where the wishing well is.


        - Once we hit a dead end go back to the nearest room that has not been
          visited. [Done]

    
    Information:
        - Add new rooms to graphs with the edges  [Done]
        - Save information in the other vertex in the graph [Done]
    
    - DFT => Traverse [WIP]
    - BFS => Shortest paths [WIP]

    
"""

graph = Graph()
def move(direct):
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }

    data ='{"direction":"' +str(direct)+ '"}'

    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)

    
    time.sleep(response.json()["cooldown"])
    if response.json()["errors"]==True:
        print("ERRORRRR",response.json()["errors"])
        return
    return response.json()

def traverse(startingRoom):
    # print("startingRoom",startingRoom,startingRoom["room_id"])
    stack = Stack() # Will hold path
    path=[] # Will hold room id
    additional_option = Stack() # Will hold room id of rooms with unvisited directions
    visited = set() # Will hold the ids of the rooms we visited
    stack.push(startingRoom["room_id"])
    graph.add_vertex(startingRoom["room_id"], startingRoom["title"], startingRoom["description"], startingRoom["coordinates"], startingRoom["elevation"], startingRoom["terrain"], startingRoom["players"], startingRoom["items"], startingRoom["exits"], startingRoom["cooldown"], startingRoom["errors"], startingRoom["messages"])
    while stack.size() > 0:
        room_id = stack.pop()
        print("room_id",room_id,"inventAndCoins()",inventAndCoins())

        if room_id not in visited:
            visited.add(room_id)
            # graph.add_vertex(room_id, title, description, coordinates, elevation, terrain, players, items, exits, cooldown, errors, messages)
            path.append(room_id)
        if len(visited) == 500:
            return path
        exits = graph.directions[room_id]
        # print("EXITS", exits)
        # potential_rooms.sort()
        possible_directions = 0
        moved=False
        for key in exits:
            # print("Breaks Here 1")
            if exits[key] =="?":
                # print("Breaks Here 4",)
                # print("key",key,"exits[key]",exits[key],"current Room", room_id, graph.directions[room_id])
                possible_directions +=1
                if moved==False:
                    nextRoom=move(key)
                    print("nextRoom",nextRoom)
                    if len(nextRoom["items"])>0:
                        print("InventoryLimitReached",InventoryLimitReached())
                        if InventoryLimitReached()==False:
                            for i in nextRoom["items"]:
                                pickUpTreasure(i)
                    graph.add_vertex(nextRoom["room_id"], nextRoom["title"], nextRoom["description"], nextRoom["coordinates"], nextRoom["elevation"], nextRoom["terrain"], nextRoom["players"], nextRoom["items"], nextRoom["exits"], nextRoom["cooldown"], nextRoom["errors"], nextRoom["messages"])
                    # print("graph.directions",graph.directions)
                    graph.add_edge(room_id,key,nextRoom["room_id"])
                    # print("graph.directions After",graph.directions)
        
                    stack.push(nextRoom["room_id"])
                    moved=True
                
            # print("Breaks Here 5")
        if possible_directions > 1:
            # print("Breaks Here 2")
            additional_option.push(room_id)
        #Another if to check for Inventory limit
        #Another if to check for treasure limit
        if possible_directions == 0:
            # print("Breaks Here 3")
            next_room = additional_option.pop()
            # print("next_room",next_room, "room id",room_id)
            path_to_room = graph.bfs(room_id, next_room)
            # print("path_to_room",path_to_room)
            path.extend(path_to_room[1:])
            for item in path_to_room:
                # print("Item in path ro room", item)
                direction=graph.directions[item]
                # direction=graph.directions[room_id].keys(item)
                # move(direction)
                for key in direction:
                    # print("Key in direction", key,direction[key],item, graph.directions[item].values())
                    if direction[key] in graph.directions[item].values():
                        # print("INSIDE direction HUGE SUCCESS")
                        move(key)                    
                if item not in visited:
                    visited.add(item)
            # print("End of path", path[-1], "Instantiate",instantiate()["room_id"])
            stack.push(path[-1])
        print("graph vertices", graph.directions)
    return None


def instantiate():
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
        }

    response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)

    time.sleep(response.json()["cooldown"])
    return response.json()

count = 0
traverse(instantiate())

print(graph.directions)

