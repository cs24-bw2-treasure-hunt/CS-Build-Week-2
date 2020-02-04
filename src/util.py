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

    def add_vertex(self, room_id, title, description, coordinates, elevation, terrain, players, items, exits, cooldown, errors, messages):
        edges = {}
        for direction in exits:
            edges[direction] = "unknown"
        self.vertices[room_id] = {"title": title, "description": description, "coordinates": coordinates, "elevation": elevation, "terrain": terrain,
                                  "players": players, "items": items, "exits": exits, "cooldown": cooldown, "errors": errors, "messages": messages, "edges": edges}

    def add_edge(self, room_id1, direction, room_id2):
        direction_reverse = {"N": "S", "S": "N", "E": "W", "W": "E"}
        if room_id1 in self.vertices and room_id2 in self.vertices:
            self.vertices[room_id1][edges][direction] = room_id2
            reverse = direction_reverse[direction]
            self.vertices[room_id2][edges][reverse] = room_id1
        else:
            raise IndexError("That vertex does not exist")

    def get_neighbors(self, room_id):
        return self.vertices[room_id][edges]

    def bft(self, starting_room_id):
        q = Queue()
        q.enqueue(starting_room_id)
        visited = set()
        while queue.size() > 0:
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
        while queue.size() > 0:
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
