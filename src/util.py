

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
        q.enqueue(room_id)
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            # print("PATH", path)
            room_id = path
            if room_id not in visited:
                # print(room_id, " not in visited")
                print(self.directions[room_id].values())
                if "?" in self.directions[room_id].values():
                    # print(self.direction)
                    print("BTF TO UNKNOWN ROOM", path)
                    return room_id
                visited.add(room_id)
                for next_room in self.get_neighbors(room_id):
                    # new_path = list(path)
                    next_room_id = self.directions[room_id][next_room]
                    print("Next room", next_room_id)
                    if next_room_id == "?":
                        print("NOT THERE")
                        return room_id
                    if next_room_id not in visited:
                        # new_path.append(append_room_id)
                    # if next_room not in visited:
                        q.enqueue(next_room_id)

        print("what? how?")

    def bfs(self, starting_room_id, destination_room_id):
        print("BFS starting_room_id, destination_room_id", starting_room_id, destination_room_id)
        q = Queue()
        q.enqueue([starting_room_id])
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            # print("path in bfs", path)
            room_id = path[-1]
            print("BFS room_id", room_id)
            # print("room_id bfs",room_id)
            if room_id not in visited:
                # print("PATH", path)
                if room_id == destination_room_id:
                    print("INSIDE",path[1:])
                    return path
                visited.add(room_id)
                for next_room in self.directions[room_id]:
                    new_path = list(path)
                    # print("new_path_1", new_path)
                    append_path = self.directions[room_id][next_room]
                    if append_path != "?":
                        new_path.append(append_path)
                    # print("new_path", new_path)
                    q.enqueue(new_path)
        print("this didn't work")

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
                for next_vertex in self.directions[vertex]:
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



# Room 131, # of rooms visited: 278
# WISE MOVE: s to 244
# Cooldown:  7.5 Errors:  [] Messages:  ['You have walked south.', 'Wise Explorer: -50% CD']
# RETURNED FROM WISE MOVE {'room_id': 244, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(61,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['shiny treasure', 'shiny treasure'], 'exits': ['n', 'e'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked south.', 'Wise Explorer: -50% CD']}
# 193 NextRoom {'room_id': 244, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(61,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['shiny treasure', 'shiny treasure'], 'exits': ['n', 'e'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked south.', 'Wise Explorer: -50% CD']}
# nextRoom {'room_id': 244, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(61,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['shiny treasure', 'shiny treasure'], 'exits': ['n', 'e'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked south.', 'Wise Explorer: -50% CD']}
# errors []
# wishingWell 55
# Room 244, # of rooms visited: 279
# WISE MOVE: e to 131
# Cooldown:  22.5 Errors:  [] Messages:  ['You have walked east.', 'Foolish Explorer: +50% CD']
# RETURNED FROM WISE MOVE {'room_id': 239, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 22.5, 'errors': [], 'messages': ['You have walked east.', 'Foolish Explorer: +50% CD']}
# 193 NextRoom {'room_id': 239, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 22.5, 'errors': [], 'messages': ['You have walked east.', 'Foolish Explorer: +50% CD']}
# nextRoom {'room_id': 239, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 22.5, 'errors': [], 'messages': ['You have walked east.', 'Foolish Explorer: +50% CD']}
# errors []
# # wishingWell 55
# Room 239, # of rooms visited: 280
# WISE MOVE: n to 198
# Cooldown:  7.5 Errors:  [] Messages:  ['You have walked north.', 'Wise Explorer: -50% CD']
# RETURNED FROM WISE MOVE {'room_id': 198, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked north.', 'Wise Explorer: -50% CD']}
# 193 NextRoom {'room_id': 198, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked north.', 'Wise Explorer: -50% CD']}
# nextRoom {'room_id': 198, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked north.', 'Wise Explorer: -50% CD']}
# errors []
# wishingWell 55
# Room 198, # of rooms visited: 281
# WISE MOVE: n to 166
# Cooldown:  10.0 Errors:  [] Messages:  ['You have walked north.', 'Uphill Penalty: 5s CD', 'Wise Explorer: -50% CD']
# RETURNED FROM WISE MOVE {'room_id': 166, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(62,52)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 10.0, 'errors': [], 'messages': ['You have walked north.', 'Uphill Penalty: 5s CD', 'Wise Explorer: -50% CD']}
# 193 NextRoom {'room_id': 166, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(62,52)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 10.0, 'errors': [], 'messages': ['You have walked north.', 'Uphill Penalty: 5s CD', 'Wise Explorer: -50% CD'




# ##INCORRECT INFORMATION

# Room 307, # of rooms visited: 442
# WISE MOVE: w to 475
# Cooldown:  22.5 Errors:  [] Messages:  ['You have walked west.', 'Foolish Explorer: +50% CD']
# RETURNED FROM WISE MOVE {'room_id': 321, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 22.5, 'errors': [], 'messages': ['You have walked west.', 'Foolish Explorer: +50% CD']}


# Room 307, # of rooms visited: 442
# WISE MOVE: w to 475
# Cooldown:  22.5 Errors:  [] Messages:  ['You have walked west.', 'Foolish Explorer: +50% CD']
# RETURNED FROM WISE MOVE {'room_id': 321, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 22.5, 'errors': [], 'messages': ['You have walked west.', 'Foolish Explorer: +50% CD']}
# 193 NextRoom {'room_id': 321, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 22.5, 'errors': [], 'messages': ['You have walked west.', 'Foolish Explorer: +50% CD']}
# nextRoom {'room_id': 321, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 22.5, 'errors': [], 'messages': ['You have walked west.', 'Foolish Explorer: +50% CD']}
# errors []
# wishingWell 55
# Room 321, # of rooms visited: 442

# ##CORRENT INFORMATION
# {1: {'e': '0'}, 0: {'n': 10, 's': 2, 'e': 4, 'w': '1'}, 10: {'n': 19, 's': 0, 'w': 43}, 19: {'n': 20, 's': 10, 'w': 77}, 20: {'n': 63, 's': 19, 'e': 27, 'w': 46}, 63: {'n': 72, 's': 20, 'w': 73}, 72: {'s': 63, 'w': 76}, 76: {'n': 83, 'e': 72, 'w': 110}, 83: {'s': 76, 'e': 130, 'w': 125}, 130: {'w': 83}, 125: {'n': 165, 'e': 83, 'w': 237}, 165: {'n': 203, 's': 125, 'w': 204}, 203: {'n': 268, 's': 165, 'e': 299}, 268: {'s': 203, 'e': 411, 'w': 312}, 411: {'w': 268}, 312: {'n': 328, 'e': 268}, 328: {'n': 332, 's': 312, 'e': 357, 'w': 363}, 332: {'n': 350, 's': 328}, 350: {'n': 436, 's': 332, 'e': 404}, 436: {'s': 350}, 404: {'n': 481, 'w': 350}, 481: {'s': 404}, 357: {'w': 328}, 363: {'n': 372, 'e': 328}, 372: {'n': 441, 's': 363}, 441: {'s': 372}, 299: {'e': 311, 'w': 203}, 311: {'w': 299}, 204: {'n': 219, 'e': 165, 'w': 216}, 219: {'s': 204}, 216: {'n': 234, 'e': 204, 'w': 218}, 234: {'n': 368, 's': 216, 'w': 252}, 368: {'s': 234}, 252: {'n': 284, 'e': 234}, 284: {'n': 302, 's': 252, 'w': 303}, 302: {'n': 422, 's': 284}, 422: {'n': 426, 's': 302}, 426: {'n': 457, 's': 422}, 457: {'n': 461, 's': 426}, 461: {'s': 457}, 303: {'n': 361, 'e': 284, 'w': 405}, 361: {'n': 408, 's': 303}, 408: {'n': 458, 's': 361, 'w': 423}, 458: {'s': 408, 'w': 459}, 459: {'e': 458}, 423: {'e': 408, 'w': 454}, 454: {'n': 470, 'e': 423}, 470: {'s': 454}, 405: {'n': 406, 'e': 303}, 406: {'s': 405, 'w': 415}, 415: {'e': 406, 'w': 418}, 418: {'n': 425, 's': 474, 'e': 415}, 425: {'s': 418, 'w': 469}, 469: {'e': 425}, 474: {'n': 418}, 218: {'s': 263, 'e': 216, 'w': 242}, 263: {'n': 218}, 242: {'n': 287, 's': 259, 'e': 218, 'w': 275}, 287: {'s': 242, 'w': 339}, 339: {'e': 287, 'w': 445}, 445: {'n': 447, 'e': 339, 'w': 450}, 447: {'s': 445}, 450: {'e': 445}, 259: {'n': 242, 'w': 310}, 310: {'e': 259, 'w': 412}, 412: {'s': 488, 'e': 310}, 488: {'n': 412}, 275: {'e': 242, 'w': 456}, 456: {'e': 275, 'w': 499}, 499: {'e': 456}, 237: {'e': 125, 'w': 245}, 245: {'s': 254, 'e': 237}, 254: {'n': 245, 'w': 314}, 314: {'e': 254}, 110: {'e': 76}, 73: {'e': 63}, 27: {'n': 40, 's': 28, 'e': 30, 'w': 20}, 40: {'s': 27}, 28: {'n': 27}, 30: {'s': 31, 'e': 32, 'w': 27}, 31: {'n': 30, 'e': 33}, 33: {'e': 38, 'w': 31}, 38: {'s': 59, 'e': 66, 'w': 33}, 59: {'n': 38, 's': 104, 'e': 92}, 104: {'n': 59, 'e': 107}, 107: {'s': 120, 'e': 121, 'w': 104}, 120: {'n': 107, 'e': 127}, 127: {'e': 184, 'w': 120}, 184: {'e': 221, 'w': 127}, 221: {'s': 253, 'e': 240, 'w': 184}, 253: {'n': 221, 'e': 258}, 258: {'e': 306, 'w': 253}, 306: {'e': 397, 'w': 258}, 397: {'w': 306}, 240: {'n': 249, 'e': 386, 'w': 221}, 249: {'n': 265, 's': 240, 'e': 282}, 265: {'n': 279, 's': 249, 'e': 270}, 279: {'s': 265}, 270: {'n': 416, 'e': 338, 'w': 265}, 416: {'s': 270}, 338: {'s': 379, 'w': 270}, 379: {'n': 338, 'e': 395}, 395: {'s': 403, 'e': 421, 'w': 379}, 403: {'n': 395}, 421: {'n': 440, 'w': 395}, 440: {'s': 421, 'w': 476}, 476: {'e': 440}, 282: {'w': 249}, 386: {'e': 414, 'w': 240}, 414: {'w': 386}, 121: {'n': 128, 'e': 143, 'w': 107}, 128: {'s': 121, 'e': 189}, 189: {'e': 255, 'w': 128}, 255: {'w': 189}, 143: {'e': 212, 'w': 121}, 212: {'w': 143}, 92: {'w': 59}, 66: {'n': 169, 'e': 123, 'w': 38}, 169: {'s': 66, 'e': 186}, 186: {'e': 205, 'w': 169}, 205: {'s': 241, 'e': 479, 'w': 186}, 241: {'n': 205, 'e': 266}, 266: {'w': 241}, 123: {'w': 66}, 479: {'w': 205}, 32: {'n': 39, 'e': 54, 'w': 30}, 39: {'n': 53, 's': 32, 'e': 51, 'w': 41}, 53: {'n': 95, 's': 39, 'w': 88}, 95: {'n': 119, 's': 53, 'w': 115}, 119: {'n': 134, 's': 95}, 134: {'n': 147, 's': 119, 'e': 144}, 147: {'n': 200, 's': 134, 'e': 153, 'w': 151}, 200: {'n': 227, 's': 147, 'e': 206}, 227: {'n': 269, 's': 200}, 269: {'n': 319, 's': 227}, 319: {'n': 359, 's': 269, 'e': 345}, 359: {'s': 319}, 345: {'s': 375, 'w': 319}, 375: {'n': 345, 'e': 385}, 385: {'w': 375}, 206: {'n': 288, 'e': 380, 'w': 200}, 288: {'s': 206}, 380: {'n': 424, 'w': 206}, 424: {'s': 380, 'e': 473}, 473: {'e': 494, 'w': 424}, 494: {'w': 473}, 153: {'e': 329, 'w': 147}, 329: {'w': 153}, 151: {'n': 172, 'e': 147, 'w': 207}, 172: {'n': 267, 's': 151}, 267: {'n': 285, 's': 172, 'w': 271}, 285: {'n': 286, 's': 267}, 286: {'n': 336, 's': 285, 'w': 291}, 336: {'s': 286}, 291: {'n': 410, 'e': 286, 'w': 347}, 410: {'s': 291}, 347: {'n': 452, 's': 442, 'e': 291}, 452: {'s': 347}, 442: {'n': 347}, 271: {'n': 337, 'e': 267}, 337: {'s': 271}, 207: {'n': 231, 'e': 151, 'w': 290}, 231: {'s': 207, 'w': 248}, 248: {'n': 296, 'e': 231, 'w': 280}, 296: {'s': 248}, 280: {'n': 325, 'e': 248}, 325: {'n': 353, 's': 280, 'w': 374}, 353: {'s': 325}, 374: {'e': 325}, 290: {'e': 207}, 144: {'e': 155, 'w': 134}, 155: {'s': 187, 'e': 316, 'w': 144}, 187: {'n': 155}, 316: {'n': 344, 'w': 155}, 344: {'n': 392, 's': 316, 'e': 390}, 392: {'s': 344, 'e': 462}, 462: {'w': 392}, 390: {'w': 344}, 115: {'n': 116, 'e': 95}, 116: {'n': 132, 's': 115}, 132: {'s': 116}, 88: {'e': 53, 'w': 122}, 122: {'n': 124, 'e': 88}, 124: {'n': 157, 's': 122}, 157: {'n': 210, 's': 124, 'w': 182}, 210: {'s': 157}, 182: {'e': 157, 'w': 208}, 208: {'e': 182}, 51: {'n': 69, 'e': 57, 'w': 39}, 69: {'n': 94, 's': 51, 'e': 103}, 94: {'n': 152, 's': 69}, 152: {'s': 94}, 103: {'n': 160, 'w': 69}, 160: {'s': 103}, 57: {'e': 145, 'w': 51}, 145: {'n': 174, 'e': 220, 'w': 57}, 174: {'n': 192, 's': 145, 'e': 224}, 192: {'n': 201, 's': 174, 'e': 223}, 201: {'s': 192}, 223: {'n': 283, 'w': 192}, 283: {'n': 331, 's': 223, 'e': 313}, 331: {'s': 283, 'e': 446}, 446: {'e': 466, 'w': 331}, 466: {'s': 486, 'e': 472, 'w': 446}, 486: {'n': 466}, 472: {'w': 466}, 313: {'w': 283}, 224: {'w': 174}, 220: {'w': 145}, 41: {'e': 39}, 54: {'w': 32}, 46: {'e': 20, 'w': 62}, 62: {'n': 64, 'e': 46, 'w': 84}, 64: {'s': 62, 'w': 82}, 82: {'n': 191, 'e': 64}, 191: {'s': 82}, 84: {'e': 62, 'w': 91}, 91: {'n': 180, 's': 101, 'e': 84, 'w': 99}, 180: {'s': 91}, 101: {'n': 91, 'w': 113}, 113: {'s': 114, 'e': 101}, 114: {'n': 113, 'w': 176}, 176: {'e': 114, 'w': 402}, 402: {'e': 176, 'w': 451}, 451: {'e': 402, 'w': 453}, 453: {'s': 464, 'e': 451}, 464: {'n': 453}, 99: {'n': 190, 'e': 91, 'w': 146}, 190: {'s': 99}, 146: {'n': 215, 's': 177, 'e': 99, 'w': 257}, 215: {'n': 246, 's': 146}, 246: {'s': 215}, 177: {'n': 146, 'w': 346}, 346: {'e': 177}, 257: {'n': 320, 'e': 146, 'w': 364}, 320: {'n': 348, 's': 257}, 348: {'s': 320}, 364: {'n': 429, 's': 381, 'e': 257, 'w': 448}, 429: {'s': 364}, 381: {'n': 364, 'w': 394}, 394: {'e': 381}, 448: {'e': 364}, 77: {'e': 19}, 43: {'e': 10, 'w': 47}, 47: {'n': 71, 'e': 43}, 71: {'s': 47}, 2: {'n': 0, 's': 6, 'e': 3}, 6: {'n': 2, 'w': 7}, 7: {'n': 8, 'e': 6, 'w': 56}, 8: {'s': 7, 'w': 16}, 16: {'n': 58, 'e': 8, 'w': 67}, 58: {'s': 16, 'w': 65}, 65: {'n': 74, 'e': 58, 'w': 139}, 74: {'n': 87, 's': 65, 'w': 161}, 87: {'s': 74}, 161: {'e': 74}, 139: {'e': 65, 'w': 188}, 188: {'e': 139, 'w': 335}, 335: {'e': 188, 'w': 366}, 366: {'e': 335}, 67: {'e': 16, 'w': 162}, 162: {'e': 67}, 56: {'e': 7, 'w': 61}, 61: {'e': 56, 'w': 171}, 171: {'e': 61}, 3: {'s': 9, 'e': '?', 'w': 2}, 9: {'n': 3, 's': 12, 'e': '?'}, 12: {'n': 9, 's': 18, 'e': 14, 'w': 21}, 18: {'n': 12, 's': 22, 'w': '?'}, 22: {'n': 18, 's': 78, 'w': 36}, 78: {'n': 22, 's': 108}, 108: {'n': 78, 's': 117, 'e': 93}, 117: {'n': 108, 's': 131, 'e': 166, 'w': 133}, 131: {'n': 117, 's': 244, 'w': '?'}, 244: {'n': 131, 'e': 239}, 239: {'n': 198, 'w': 244}, 198: {'n': 166, 's': 239, 'e': 199}, 166: {'s': 198, 'e': 150, 'w': 117}, 150: {'n': 135, 'w': 166}, 135: {'s': 150, 'e': 106}, 106: {'n': 100, 's': 111, 'w': 135}, 100: {'s': 106, 'e': 112, 'w': 68}, 112: {'s': 141, 'e': 140, 'w': 100}, 141: {'n': 112, 'e': 156}, 156: {'s': 168, 'e': 164, 'w': 141}, 168: {'n': 156, 'e': 340}, 340: {'w': 168}, 164: {'n': 217, 'e': 298, 'w': 156}, 217: {'s': 164, 'e': 247}, 247: {'e': 261, 'w': 217}, 261: {'s': 277, 'e': 322, 'w': 247}, 277: {'n': 261, 'e': 323}, 323: {'e': 433, 'w': 277}, 433: {'s': 455, 'e': 460, 'w': 323}, 455: {'n': 433}, 460: {'w': 433}, 322: {'n': 382, 'e': 435, 'w': 261}, 382: {'s': 322, 'e': 388}, 388: {'e': 477, 'w': 382}, 477: {'e': 483, 'w': 388}, 483: {'w': 477}, 435: {'w': 322}, 298: {'s': 324, 'w': 164}, 324: {'n': 298, 's': 349, 'e': 354}, 349: {'n': 324, 's': 352, 'e': 384, 'w': 356}, 352: {'n': 349, 's': 362, 'e': 485}, 362: {'n': 352, 's': 399, 'w': 463}, 399: {'n': 362, 's': 467}, 467: {'n': 399}, 463: {'s': 468, 'e': 362}, 468: {'n': 463}, 485: {'w': 352}, 384: {'w': 349}, 356: {'e': 349}, 354: {'w': 324}, 140: {'w': 112}, 68: {'n': 52, 'e': 100}, 52: {'n': 35, 's': 68, 'e': 75}, 35: {'s': 52, 'w': 34}, 34: {'n': 14, 's': 50, 'e': 35}, 14: {'s': 34, 'e': 37, 'w': 12}, 37: {'w': 14}, 21: {'e': 12, 'w': 29}, 29: {'s': 45, 'e': 21, 'w': 49}, 45: {'n': 29, 's': 60}, 60: {'n': 45, 'e': 36, 'w': 70}, 36: {'s': 48, 'e': 22, 'w': 60}, 48: {'n': 36, 's': 105, 'w': 149}, 105: {'n': 48, 'w': 202}, 202: {'e': 105}, 149: {'e': 48}, 70: {'s': 163, 'e': 60, 'w': 98}, 163: {'n': 70}, 98: {'n': 102, 's': 126, 'e': 70, 'w': 109}, 102: {'s': 98, 'w': 142}, 142: {'e': 102, 'w': 159}, 159: {'e': 142, 'w': 196}, 196: {'n': 222, 'e': 159, 'w': 197}, 222: {'n': 305, 's': 196}, 305: {'n': 365, 's': 222}, 365: {'s': 305}, 197: {'n': 232, 'e': 196, 'w': 276}, 232: {'n': 272, 's': 197, 'w': 235}, 272: {'n': 295, 's': 232}, 295: {'s': 272}, 235: {'n': 330, 'e': 232, 'w': 355}, 330: {'n': 369, 's': 235, 'w': 383}, 369: {'n': 400, 's': 330, 'w': 376}, 400: {'s': 369}, 376: {'e': 369}, 383: {'e': 330, 'w': 495}, 495: {'e': 383}, 355: {'e': 235}, 276: {'e': 197, 'w': 419}, 419: {'e': 276}, 126: {'n': 98, 's': 129}, 129: {'n': 126, 'e': 194, 'w': 170}, 194: {'s': 214, 'w': 129}, 214: {'n': 194, 'e': 173, 'w': 226}, 173: {'e': 133, 'w': 214}, 133: {'e': 117, 'w': 173}, 226: {'s': 300, 'e': 214}, 300: {'n': 226, 's': 377, 'w': 389}, 377: {'n': 300}, 389: {'e': 300}, 170: {'e': 129}, 109: {'s': 185, 'e': 98, 'w': 175}, 185: {'n': 109}, 175: {'s': 183, 'e': 109, 'w': 179}, 183: {'n': 175, 's': 229}, 229: {'n': 183, 's': 250, 'w': 236}, 250: {'n': 229, 's': 294, 'e': 289}, 294: {'n': 250, 's': 334}, 334: {'n': 294, 's': 393, 'e': 341, 'w': 391}, 393: {'n': 334, 's': 482}, 482: {'n': 393}, 341: {'s': 449, 'w': 334}, 449: {'n': 341}, 391: {'s': 396, 'e': 334, 'w': 428}, 396: {'n': 391}, 428: {'e': 391}, 289: {'w': 250}, 236: {'s': 264, 'e': 229}, 264: {'n': 236, 's': 274, 'w': 273}, 274: {'n': 264, 'w': 308}, 308: {'e': 274}, 273: {'n': 343, 'e': 264}, 343: {'s': 273, 'w': 351}, 351: {'s': 491, 'e': 343, 'w': 478}, 491: {'n': 351}, 478: {'e': 351}, 179: {'s': 233, 'e': 175, 'w': 213}, 233: {'n': 179, 'w': 238}, 238: {'e': 233}, 213: {'e': 179, 'w': 420}, 420: {'s': 444, 'e': 213, 'w': 437}, 444: {'n': 420, 'w': 490}, 490: {'e': 444, 'w': 493}, 493: {'e': 490}, 437: {'e': 420, 'w': 497}, 497: {'e': 437}, 49: {'s': 79, 'e': 29, 'w': 136}, 79: {'n': 49}, 136: {'e': 49, 'w': 148}, 148: {'e': 136, 'w': 292}, 292: {'n': 301, 'e': 148}, 301: {'n': 304, 's': 292}, 304: {'s': 301}, 50: {'n': 34, 's': 89}, 89: {'n': 50, 's': 93}, 93: {'n': 89, 'w': 108}, 75: {'e': 85, 'w': 52}, 85: {'e': 154, 'w': 75}, 154: {'e': 193, 'w': 85}, 193: {'e': 251, 'w': 154}, 251: {'e': 315, 'w': 193}, 315: {'w': 251}, 111: {'n': 106, 's': 367, 'e': 158}, 367: {'n': 111}, 158: {'s': 167, 'w': 111}, 167: {'n': 158, 's': 262, 'e': 260}, 262: {'n': 167, 's': 370, 'e': 358}, 370: {'n': 262, 's': 434, 'e': 407}, 434: {'n': 370}, 407: {'s': 496, 'w': 370}, 496: {'n': 407}, 358: {'e': 401, 'w': 262}, 401: {'w': 358}, 260: {'w': 167}, 199: {'s': 230, 'w': 198}, 230: {'n': 199, 's': 307, 'e': '?'}, 307: {'n': 230, 's': 373, 'e': 371, 'w': 321}, 373: {'n': 307, 's': 480}, 480: {'n': 373}, 371: {'s': 475, 'w': 307}, 475: {'n': 371, 's': 484}, 484: {'n': 475}, 25: {'e': '?'}, 11: {'e': '?', 'w': '?'}, 17: {'n': '?', 'e': '?', 'w': '?'}, 24: {'s': '?'}, 42: {'n': '?', 's': '?', 'e': '?', 'w': '?'}, 44: {'s': '?'}, 80: {'n': '?', 's': '?', 'e': '?'}, 81: {'n': '?'}, 86: {'s': '?', 'e': '?', 'w': '?'}, 96: {'n': '?', 'e': '?'}, 97: {'e': '?', 'w': '?'}, 181: {'w': '?'}, 90: {'e': '?', 'w': '?'}, 178: {'n': '?', 'e': '?', 'w': '?'}, 209: {'s': '?'}, 243: {'s': '?', 'e': '?', 'w': '?'}, 293: {'n': '?'}, 256: {'s': '?', 'e': '?', 'w': '?'}, 360: {'n': '?', 'e': '?'}, 398: {'e': '?', 'w': '?'}, 438: {'e': '?', 'w': '?'}, 465: {'e': '?', 'w': '?'}, 498: {'w': '?'}, 327: {'e': '?', 'w': '?'}, 427: {'e': '?', 'w': '?'}, 430: {'n': '?', 'e': '?', 'w': '?'}, 443: {'s': '?', 'e': '?'}, 471: {'w': '?'}, 439: {'w': '?'}, 118: {'e': '?', 'w': '?'}, 137: {'w': '?'}, 5: {'w': '?'}, 4: {'n': 23, 'e': 13, 'w': 0}, 23: {'s': 4, 'e': 26}, 26: {'e': 55, 'w': 23}, 55: {'w': 26}, 13: {'e': 15, 'w': 4}, 15: {'w': 13}, 321: {'s': '?', 'e': 307}}
