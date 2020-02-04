from util import Graph,Stack,Queue
import requests 
import json

"""
    Take into Account:
        - Cool Down Time
        - Inventory (limit of how many items we can carry)
        - treasure or other items that could help in the rooms
        - 1,000+ coins go to the wishing well (if we know where it is, if not search for it).
          Once found do action there (change name)

    Directions:
        - Traversal path (Big Array) ==>will need to hold the data from the rooms
        - Note where the shop is to sell the treasure => BFS back to here everytime
          our inventory is full or over a limit we set (70%)
        - Note where the wishing well is.
        - Once we hit a dead end go back to the nearest room that has not been
          visited.

    
    Information:
        - Add new rooms to graphs with the edges
        - Save information in the other vertex in the graph
    
    - DFT => Traverse
    - BFS => Shortest paths

    
"""

graph = Graph()
def move(direction):
    headers = {
    'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
    'Content-Type': 'application/json',
    }

    data = '{"direction":"s"}'


    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)
    return response.json()

def traverse(startingRoom):
    stack = Stack()
    path=[]
    additional_option = Stack()
    visited = set()
    stack.push(0)
    while stack.size() > 0:
        room = stack.pop()

        if room not in visited:
            visited.add(room)
            # graph.add_vertex(room_id, title, description, coordinates, elevation, terrain, players, items, exits, cooldown, errors, messages)
            path.append(room)
        if len(visited) == len(graph.rooms):
            return path
        potential_rooms = graph.directions[room]
        # potential_rooms.sort()
        possible_directions = 0
        for next_room in potential_rooms:
            if next_room not in visited:
                possible_directions +=1
                stack.push(next_room)
        if possible_directions > 1:
            additional_option.push(room)
        if possible_directions == 0:
            next_room = additional_option.pop()
            path_to_room = graph.bfs(room, next_room)
            path.extend(path_to_room[1:])
            for item in path_to_room:
                if item not in visited:
                    visited.add(item)
            stack.push(path[-1])
    return None


def instantiate():
    headers = {
    'Authorization': 'Token 7a375b52bdc410eebbc878ed3e58b2e94a8cb607',
}

    response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/adv/init/', headers=headers)

    
    return response.json()

traverse(instantiate())

print(graph.vertices)
