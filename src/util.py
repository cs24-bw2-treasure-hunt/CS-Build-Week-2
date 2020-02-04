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
        self.vertices = {}
        self.room_info = {}

    def add_vertex(self, room_id, title, description, coordinates, elevation, terrain, players, items, exits, cooldown, errors, messages):
        edges = {}
        for direction in exits:
            edges[direction] = "unknown"
        self.room_info[room_id] = {"title": title, "description": description, "coordinates": coordinates, "elevation": elevation, "terrain": terrain,
                                  "players": players, "items": items, "exits": exits, "cooldown": cooldown, "errors": errors, "messages": messages}
        self.vertices[room_id] = edges
    def add_edge(self, room_id1, direction, room_id2):
        direction_reverse = {"N": "S", "S": "N", "E": "W", "W": "E"}
        if room_id1 in self.vertices and room_id2 in self.vertices:
            self.vertices[room_id1][direction] = room_id2
            reverse = direction_reverse[direction]
            self.vertices[room_id2][reverse] = room_id1
        else:
            raise IndexError("That vertex does not exist")

    def get_neighbors(self, room_id):
        return self.vertices[room_id]

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

    def bfs(self, starting_room_id, destination_room_id):
        q = Queue()
        q.enqueue([starting_room_id])
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            room_id = path[-1]
            if room_id not in visited:
                if room_id == destination_room_id:
                    return path
                visited.add(room_id)
                for next_room in self.get_neighbors(room_id):
                    new_path = list(path)
                    new_path.append(next_room)
                    q.enqueue(new_path)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        stack = Stack()
        stack.push(starting_vertex)
        visited = set()
        while stack.sadditional_option = Stack()ize() > 0:
            vertex = stack.pop()
            if vertex not in visited:
                print(vertex)
                visited.add(vertex)
                for next_vert in self.get_neighbors(vertex):
                    stack.push(next_vert)

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
        path=[]
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
                    possible_directions +=1
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