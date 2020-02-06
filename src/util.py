

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


class Graph:
    def __init__(self):
        self.directions = {}
        self.room_info = {}

    def add_vertex(self, room_id, title, description, coordinates, elevation, terrain, players, items, exits, cooldown, errors, messages):
        if room_id in self.room_info:
            return
        edges = {}
        for direction in exits:
            edges[direction] = "?"
        self.directions[room_id] = edges

        self.room_info[room_id] = {"title": title, "description": description, "coordinates": coordinates, "elevation": elevation, "terrain": terrain,
                                   "players": players, "items": items, "exits": exits, "cooldown": cooldown, "errors": errors, "messages": messages}

    def add_edge(self, room_id1, direction, room_id2):
        direction_reverse = {"n": "s", "s": "n", "e": "w", "w": "e"}
        if room_id1 in self.directions and room_id2 in self.directions:
            self.directions[room_id1][direction] = room_id2
            reverse = direction_reverse[direction]
            self.directions[room_id2][reverse] = room_id1
        else:
            raise IndexError("That vertex does not exist")

    def get_neighbors(self, room_id):
        # print("get_neighbors", room_id)
        # print("self.directions[room_id]",room_id, self.directions[room_id])
        return self.directions[room_id]

    def bft(self, starting_room_id):
        q = Queue()
        q.enqueue(starting_room_id)
        visited = set()
        while q.size() > 0:
            room_id = q.dequeue()
            if room_id not in visited:
                print(room_id)
                visited.add(room_id)
                for next_room in self.get_neighbors(room_id):
                    q.enqueue(next_room)

    def bft_to_unknown(self, room_id):
        print("BFT TO UNKNOWN")
        q = Queue()
        q.enqueue([room_id])
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            room_id = path[-1]
            if room_id not in visited:
                if "?" in self.directions[room_id].values():
                    # print(self.direction)
                    print("BTF TO UNKNOWN ROOM", path[-1])
                    return path[-1]
                visited.add(room_id)
                for next_room in self.get_neighbors(room_id):
                    new_path = list(path)
                    append_path = self.directions[room_id][next_room]
                    if append_path != "?":
                        new_path.append(append_path)
                    q.enqueue(new_path)

    def bfs(self, starting_room_id, destination_room_id):
        # print("BFS starting_room_id, destination_room_id", starting_room_id, destination_room_id)
        q = Queue()
        q.enqueue([starting_room_id])
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            # print("path in bfs", path)
            room_id = path[-1]
            # print("room_id bfs",room_id)
            if room_id not in visited:
                if room_id == destination_room_id:
                    # print("INSIDE",path[1:])
                    return path
                visited.add(room_id)
                for next_room in self.get_neighbors(room_id):
                    new_path = list(path)
                    # print("new_path_1", new_path)
                    append_path = self.directions[room_id][next_room]
                    if append_path != "?":
                        new_path.append(append_path)
                    # print("new_path", new_path)
                    q.enqueue(new_path)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        stack = Stack()
        stack.push([starting_vertex])
        visited = set()
        while stack.size() > 0:
            path = stack.pop()
            vertex = path[-1]
            if vertex not in visited:
                if vertex == destination_vertex:
                    return path
                visited.add(vertex)
                for next_vertex in self.get_neighbors(vertex):
                    new_path = list(path)
                    new_path.append(next_vertex)
                    stack.push(new_path)

    def traverse(self):
        stack = Stack()
        path = []
        additional_option = Stack()
        visited = set()
        stack.push(0)
        while stack.size() > 0:
            room = stack.pop()

            if room not in visited:
                visited.add(room)
                path.append(room)
            if len(visited) == len(self.rooms):
                return path
            potential_rooms = self.connections[room]
            potential_rooms.sort()
            possible_directions = 0
            for next_room in potential_rooms:
                if next_room not in visited:
                    possible_directions += 1
                    stack.push(next_room)
            if possible_directions > 1:
                additional_option.push(room)
            if possible_directions == 0:
                next_room = additional_option.pop()
                path_to_room = self.bfs(room, next_room)
                path.extend(path_to_room[1:])
                for item in path_to_room:
                    if item not in visited:
                        visited.add(item)
                stack.push(path[-1])
        return None


# headers = {
#     'Authorization': 'Token 483f54da97f902a54b1a93b0d6409362f3cf847e',
#     'Content-Type': 'application/json',
# }

# data = '{"direction":"s"}'

# response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/adv/move/', headers=headers, data=data)
# print(response.json())


# class MiniGraph:
#     def __init__(self):
#         self.vertices = {}

#     def add_vertex(self, vertex_id):
#         self.vertices[vertex_id] = {}

#     def add_edges(self, vertex_id, connections):
#         self.vertices[vertex_id] = connections

#     def get_neighbors(self, vertex_id):
#         return self.vertices[vertex_id]

#     def bfs(self, starting_id, destination_id):
#         q = Queue()
#         q.enqueue([starting_id])
#         visited = set()
#         while q.size() > 0:
#             path = q.dequeue()
#             vertex = path[-1]
#             if vertex not in visited:
#                 if vertex == destination_id:
#                     return path
#                 visited.add(vertex)
#                 for next_vertex in self.get_neighbors(vertex):
#                     if self.vertices[vertex][next_vertex] != "?":
#                         new_path = list(path)
#                         new_path.append(self.vertices[vertex][next_vertex])
#                         q.enqueue(new_path)
#                     # print(self.vertices[vertex][next_vertex])
