import socket
import threading
import json
import os
import random

inputed_port = input("Enter server port>")
port = int(inputed_port) if inputed_port.isdigit() and int(inputed_port) < 65535 and int(inputed_port) > 0 else 8000

serverSocket = socket.socket()
try:
    serverSocket.bind(("", port))
    print("[LOG]", "Successfully installed port for socket")
except Exception as exc:
    print("[ERROR]", "Failed to install port for socket")
    print("[EXCEPTION]", exc)
    input()
    exit()

clients = []
dirname = os.path.dirname(__file__)
serverSocket.listen(1)
MAX_CLIENTS = 10
new_blocks = []
world = []
starting_blocks = []
world_len = 200


class Client:
    def __init__(self, socket, nickname, ID):
        self.socket = socket
        self.socket.settimeout(5)
        self.nickname = nickname
        self.inventory = []
        self.id = ID
        self.pos = [0, 0]
        self.thread = threading.Thread(target=self.thread)
        self.thread.start()

    def thread(self):
        running = True
        global new_blocks, starting_blocks, clients

        while running:
            # try:
            received = ""
            while True:
                received += self.socket.recv(8192).decode("utf-8")
                if not received:
                    running = False
                if received[-1] == "=":
                    received = received[:-1]
                    break
            data = json.loads(received)
            for block in data["new_blocks"]:
                new_blocks.append(block)
            self.pos = data["self"]
            reply = {"new_blocks": new_blocks}
            reply["users"] = [[c.pos, c.nickname] for c in clients if c.id != self.id]
            self.socket.send((json.dumps(reply) + "=").encode())
            # except Exception as ex:
            #    print("[EXCEPTION]", ex)
            #    break

        print("[INFO] {} has disconnected".format(self.nickname))
        self.socket.close()
        clients.remove(self)


def globalUpdateCycle():
    global clients
    while True:
        break


for i in range(0, world_len * world_len):
    world.append({"item": None, "building": None, "tile": "stone", "part": 0, "rotation": 0})

for i in range(0, random.randint(5, 20)):
    size = random.randint(1, 5)
    x = random.randint(0, world_len - (size + 1))
    y = random.randint(0, world_len - (size + 1))
    for xpos in range(0, size):
        for ypos in range(0, size):
            grass_chance = ["grass", "grass", "leaves"]
            world[x + xpos + ((y + ypos) * world_len)]["tile"] = random.choice(grass_chance)
            starting_blocks.append({"id": x + xpos + ((y + ypos) * world_len), "tile": world[x + xpos + ((y + ypos) * world_len)]})


for i in range(0, 4):
    x = random.randint(0, world_len - 1)
    y = random.randint(0, world_len - 1)
    if i == 0 or i == 1:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "coal_ore", "part": 0, "rotation": 0}
        starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
    elif i == 2:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "iron_ore", "part": 0, "rotation": 0}
        starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
    elif i == 3:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "copper_ore", "part": 0, "rotation": 0}
        starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
    elif i == 4:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "tungsten_ore", "part": 0, "rotation": 0}
        starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
for i1 in range(0, int((world_len - 20) / 2)):
    x = random.randint(0, world_len - 1)
    y = random.randint(0, world_len - 1)
    i = random.randint(0, 4)
    if i == 0 or i == 1:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "coal_ore", "part": 0, "rotation": 0}
        starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
    elif i == 2:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "iron_ore", "part": 0, "rotation": 0}
        starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
    elif i == 3:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "copper_ore", "part": 0, "rotation": 0}
        starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
    elif i == 4:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "tungsten_ore", "part": 0, "rotation": 0}
        starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
x = random.randint(0, world_len - 3)
y = random.randint(0, world_len - 3)
for i in range(0, 3):
    for i1 in range(0, 3):
        world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "grass", "part": 0, "rotation": 0}
        starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
        if i == 1 and i1 == 1:
            world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "resin _tree", "part": 0, "rotation": 0}
            starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
if int(world_len / 100) > 0:
    for l in range(0, int(world_len / 100)):
        for i in range(0, 3):
            for i1 in range(0, 3):
                world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "grass", "part": 0, "rotation": 0}
                if i == 1 and i1 == 1:
                    world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "resin_tree", "part": 0, "rotation": 0}


running = True
globalUpdateCycleThread = threading.Thread(target=globalUpdateCycle)
globalUpdateCycleThread.start()
while running:
    if len(clients) < MAX_CLIENTS:
        connection, address = serverSocket.accept()
        try:
            nickname = connection.recv(8192).decode("utf-8")
            reply = {"starting_blocks": starting_blocks}
            reply = json.dumps(reply)
            connection.send((reply + "=").encode())
        except Exception as exc:
            print("[ERROR]", "An unexpected error occured while client was connecting")
            print("[EXCEPTION]", exc)
            continue
        print("[INFO]", "{} has connected".format(nickname))
        clients.append(Client(connection, nickname, len(clients)))

