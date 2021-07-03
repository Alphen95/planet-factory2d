import socket
import threading
import json
import os
import random
import pygame

inputed_port = input("Enter server port>")
port = int(inputed_port) if inputed_port.isdigit() and int(inputed_port) < 65535 and int(inputed_port) > 0 else 8000
clock = pygame.time.Clock()

serverSocket = socket.socket()
try:
    serverSocket.bind(("", port))
    print("[LOG]", "Successfully installed port for socket")
except Exception as exc:
    print("[ERROR]", "Failed to install port for socket")
    print("[EXCEPTION]", exc)
    input()
    exit()

processing_recepies = {
    "smelter":[
        {
            "name":"Iron ingot",
            "required_text":"Iron ore",
            "output_text":"Iron ingot",
            "required":[[("unprocessed","iron"),1]],
            "output":{"item": ("ingot", "iron"), "amount": 1},
            "time":2
        },
        {
            "name":"Copper ingot",
            "required_text":"Copper ore",
            "output_text":"Copper ingot",
            "required":[[("unprocessed","copper"),1]],
            "output":{"item": ("ingot", "copper"), "amount": 1},
            "time":2
        }, 
    ]
}
clients = []
dirname = os.path.dirname(__file__)
serverSocket.listen(1)
MAX_CLIENTS = 10
new_blocks = []
world = []
starting_blocks = []
world_len = 200
tick = 0
temp_new_blocks = []
chat = []

power_capacity = 0
power_capacity_current = 0
power_max = 0
power_usage = 0
power_down = False


class Client:
    def __init__(self, socket, nickname, ID):
        self.socket = socket
        self.socket.settimeout(5)
        self.nickname = nickname
        self.rot = 0
        self.state = "default"
        self.id = ID
        self.newBlocks = []
        self.pos = [0, 0]
        self.thread = threading.Thread(target=self.thread)
        self.thread.start()
        self.player = "alphen"
        self.updBlocks = []

    def thread(self):
        running = True
        global new_blocks, starting_blocks, clients, temp_new_blocks,chat,world

        while running:
            #try:
            block_updated = False
            received = ""
            while True:
                received += self.socket.recv(8192).decode("utf-8")
                if not received:
                    running = False
                if received[-1] == "=":
                    received = received[:-1]
                    break
            data = json.loads(received)
            for bl in data["new_blocks"]:
                world[bl["id"]] = bl["tile"] 
            for bl in data["upd_blocks"]:
                world[bl["id"]] = bl["tile"] 
            for c in clients:
                for bl in data["new_blocks"]:
                    c.newBlocks.append(bl)
            for c in clients:
                for bl in data["upd_blocks"]:
                    c.newBlocks.append(bl)
            for temp_block in data["temp_new_blocks"]:
                world[temp_block["id"]] = temp_block["tile"]
                temp_new_blocks.append(temp_block)
            if data["msg"] != "":
                chat.append({"user":self.nickname,"text":data["msg"]})
            power_down = data["power_down"]
            self.pos = data["self"][0]
            self.state = data["self"][1]
            self.rot = data["self"][2]
            self.player = data["self"][3]
            reply = {"new_blocks": self.newBlocks, "upd_blocks":self.updBlocks, "temp_new_blocks":temp_new_blocks,"chat":chat,"power":[power_down,power_capacity,power_capacity_current,power_max,power_usage]}
            self.newBlocks = []
            self.updBlocks = []
            reply["users"] = [[c.pos, c.nickname,c.state,c.rot,c.player] for c in clients if c.id != self.id]
            self.socket.send((json.dumps(reply) + "=").encode())
            #except Exception as ex:
                #print("[EXCEPTION]", ex)
                #break

        print("[INFO] {} has disconnected".format(self.nickname))
        chat.append({"user":"Server","text":"{} has disconnected".format(self.nickname)})
        self.socket.close()
        clients.remove(self)


def globalUpdateCycle():
    global clients, running, tick, world, temp_new_blocks,new_blocks,power_capacity,power_capacity_current,power_down,power_max,power_usage
    while running:
        for tile_id,tile in enumerate(world):
            if "tick_timer" in tile and tile["tick_timer"] > -1: 
                tile["tick_timer"] -= 1
                for c in clients:c.newBlocks.append({"id":tile_id,"tile":tile})     
        power_capacity = 0
        if tick == 59:
            print("a")
            tick = 0
            power_capacity = 0
            power_capacity_current = 0
            power_max = 0
            power_usage = 0
            for tile_id, tile in enumerate(world):
                if tile["building"] == "biomass_burner":
                    power_max += 100       
                    if tile["timer"] == 0 and not power_down:
                        if tile["inventory"] != {} and tile["inventory"]["amount"] > 1:
                            tile["timer"] = 30
                            tile["inventory"]["amount"] -= 1
                            tile["tick_timer"] = 30*60
                            power_capacity += 100  
                            power_capacity_current +=100
                            for c in clients:c.updBlocks.append({"id":tile_id,"tile":tile})      
                    elif not power_down:
                        tile["timer"] -= 1
                        power_capacity += 100                      
                elif tile["tile"] == "coal_plant" and tile["part"] == 1:
                    #power_capacity += 250
                    pass                
            for tile_id, tile in enumerate(world):
                if tile["building"] == "drill" and tile["part"] == 1 and (power_capacity >= 10 or not(power_down) and power_capacity >= 10):
                    power_capacity -= 10
                    power_usage += 10
                    tile["inventory"]["amount"] += 1

                    for c in clients:c.updBlocks.append({"id":tile_id,"tile":tile})                    
                elif tile["building"] == "drill" and tile["part"] == 1 and power_capacity < 10:
                    power_down = True
                if tile["building"] == "smelter" and tile["part"] == 1:# and (power_capacity >= 15 or not(power_down) and power_capacity >= 15):
                    print(2)
                    power_capacity -= 15
                    power_usage += 15
                    if tile["timer"] == 0 and tile["recepie"] != -1:
                        print(3)
                        if tile["inventory"][1] != {}:
                            
                            tile["inventory"][1]["amount"] += processing_recepies[tile["building"]][tile["recepie"]]["output"]["amount"]
                            tile["timer"] = -1
                            for c in clients:c.updBlocks.append({"id":tile_id,"tile":tile})                               
                        elif tile["inventory"][1] == {}:
                            tile["inventory"][1] = processing_recepies[tile["building"]][tile["recepie"]]["output"].copy()
                            tile["timer"] = -1
                            for c in clients:c.updBlocks.append({"id":tile_id,"tile":tile})                                    
                    if tile["inventory"][0] != {} and tile["inventory"][0]["amount"] >= processing_recepies[tile["building"]][tile["recepie"]]["required"][0][1] and tile["timer"] == -1:
                        print(5)
                        tile["timer"] = processing_recepies[tile["building"]][tile["recepie"]]["time"]
                        tile["tick_timer"]  = (processing_recepies[tile["building"]][tile["recepie"]]["time"]+1)*60
                        if tile["inventory"][0]["amount"] > processing_recepies[tile["building"]][tile["recepie"]]["required"][0][1]:
                            tile["inventory"][0]["amount"] -= processing_recepies[tile["building"]][tile["recepie"]]["required"][0][1]
                        elif tile["inventory"][0]["amount"] == processing_recepies[tile["building"]][tile["recepie"]]["required"][0][1]:
                            tile["inventory"][0] = {}
                        for c in clients:c.updBlocks.append({"id":tile_id,"tile":tile})                                 
                    elif tile["timer"]  >= 1:
                        print(4)
                        tile["timer"] -=1
                        for c in clients:c.updBlocks.append({"id":tile_id,"tile":tile})                                   
                elif tile["building"] == "smelter" and tile["part"] == 1 and power_capacity < 15:
                    power_down = True
                if tile["tile"] == "grass" and random.randint(0, 1) == 0 and tile["building"] == None:
                    tile["tile"] = "leaves"
                    for c in clients:c.newBlocks.append({"id":tile_id,"tile":tile})
                for tile_id, tile in enumerate(world):

                    if x == world_len:
                        y += 1
                        x = 0
                    if tile["building"] == "drill" and tile["part"] == 1 and "inventory" in tile and tile["inventory"]["amount"] >= 1:
                        if tile["rotation"] == 0 and x + 3 < world_len and world[(x + 2) + (y * world_len)]["building"] == "conveyor_belt" and world[(x + 2) + (y * world_len)]["inventory"] == {}:
                            world[(x + 2) + (y * world_len)]["inventory"] = {"item": tile["inventory"]["item"]}
                            tile["inventory"]["amount"] -= 1
                            world[(x + 2) + (y * world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 90 and y - 2 >= 0 and world[x + ((y - 2) * world_len)]["building"] == "conveyor_belt" and world[x + ((y - 2) * world_len)]["inventory"] == {}:
                            world[x + ((y - 2) * world_len)]["inventory"] = {"item": tile["inventory"]["item"]}
                            tile["inventory"]["amount"] -= 1
                            world[x + ((y - 2) * world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 180 and x - 2 >= 0 and world[(x - 2) + (y * world_len)]["building"] == "conveyor_belt" and world[(x - 2) + (y * world_len)]["inventory"] == {}:
                            world[(x - 2) + (y * world_len)]["inventory"] = {"item": tile["inventory"]["item"]}
                            tile["inventory"]["amount"] -= 1
                            world[(x - 2) + (y * world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 270 and y + 3 < world_len and world[x + ((y + 2) * world_len)]["building"] == "conveyor_belt" and world[x + ((y + 2) * world_len)]["inventory"] == {}:
                            world[x + ((y + 2) * world_len)]["inventory"] = {"item": tile["inventory"]["item"]}
                            tile["inventory"]["amount"] -= 1
                            world[x + ((y + 2) * world_len)]["not_gotta_work"] = True
                    elif tile["building"] in conveyor_acceptable_processors and tile["part"] == conveyor_acceptable_processors[tile["building"]] and "inventory" in tile and tile["inventory"][-1] != {}:
                        if tile["rotation"] == 0 and x + 2 < world_len and world[(x + 1) + (y * world_len)]["building"] == "conveyor_belt" and world[(x + 1) + (y * world_len)]["inventory"] == {}:
                            world[(x + 1) + (y * world_len)]["inventory"] = {"item": tile["inventory"][-1]["item"]}
                            if tile["inventory"][-1]["amount"] != 1:
                                tile["inventory"][-1]["amount"] -= 1
                            else:
                                tile["inventory"][-1] = {}
                            world[(x + 1) + (y * world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 90 and y - 1 >= 0 and world[x + ((y - 1) * world_len)]["building"] == "conveyor_belt" and world[x + ((y - 1) * world_len)]["inventory"] == {}:
                            world[x + ((y - 1) * world_len)]["inventory"] = {"item": tile["inventory"][-1]["item"]}
                            if tile["inventory"][-1]["amount"] != 1:
                                tile["inventory"][-1]["amount"] -= 1
                            else:
                                tile["inventory"][-1] = {}
                            world[x + ((y - 2) * world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 180 and x - 1 >= 0 and world[(x - 1) + (y * world_len)]["building"] == "conveyor_belt" and world[(x - 1) + (y * world_len)]["inventory"] == {}:
                            world[(x - 1) + (y * world_len)]["inventory"] = {"item": tile["inventory"][-1]["item"]}
                            if tile["inventory"][-1]["amount"] != 1:
                                tile["inventory"][-1]["amount"] -= 1
                            else:
                                tile["inventory"][-1] = {}
                            world[(x - 1) + (y * world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 270 and y + 2 < world_len and world[x + ((y + 1) * world_len)]["building"] == "conveyor_belt" and world[x + ((y + 1) * world_len)]["inventory"] == {}:
                            world[x + ((y + 1) * world_len)]["inventory"] = {"item": tile["inventory"][-1]["item"]}
                            if tile["inventory"][-1]["amount"] != 1:
                                tile["inventory"][-1]["amount"] -= 1
                            else:
                                tile["inventory"][-1] = {}
                            world[x + ((y + 1) * world_len)]["not_gotta_work"] = True
                    elif tile["building"] == "storage_container" and tile["part"] == 2:
                        for item_id, item in enumerate(tile["inventory"]):
                            if item != {}:
                                if tile["rotation"] == 0 and x + 2 < world_len and world[(x + 1) + (y * world_len)]["building"] == "conveyor_belt" and world[(x + 1) + (y * world_len)]["inventory"] == {}:
                                    world[(x + 1) + (y * world_len)]["inventory"] = {"item": tile["inventory"][item_id]["item"]}
                                    if tile["inventory"][item_id]["amount"] != 1:
                                        tile["inventory"][item_id]["amount"] -= 1
                                    else:
                                        tile["inventory"][item_id] = {}
                                    world[(x + 1) + (y * world_len)]["not_gotta_work"] = True
                                elif tile["rotation"] == 90 and y - 1 >= 0 and world[x + ((y - 1) * world_len)]["building"] == "conveyor_belt" and world[x + ((y - 1) * world_len)]["inventory"] == {}:
                                    world[x + ((y - 1) * world_len)]["inventory"] = {"item": tile["inventory"][item_id]["item"]}
                                    if tile["inventory"][item_id]["amount"] != 1:
                                        tile["inventory"][item_id]["amount"] -= 1
                                    else:
                                        tile["inventory"][item_id] = {}
                                    world[x + ((y - 2) * world_len)]["not_gotta_work"] = True
                                elif tile["rotation"] == 180 and x - 1 >= 0 and world[(x - 1) + (y * world_len)]["building"] == "conveyor_belt" and world[(x - 1) + (y * world_len)]["inventory"] == {}:
                                    world[(x - 1) + (y * world_len)]["inventory"] = {"item": tile["inventory"][item_id]["item"]}
                                    if tile["inventory"][item_id]["amount"] != 1:
                                        tile["inventory"][item_id]["amount"] -= 1
                                    else:
                                        tile["inventory"][item_id] = {}
                                    world[(x - 1) + (y * world_len)]["not_gotta_work"] = True
                                elif tile["rotation"] == 270 and y + 2 < world_len and world[x + ((y + 1) * world_len)]["building"] == "conveyor_belt" and world[x + ((y + 1) * world_len)]["inventory"] == {}:
                                    world[x + ((y + 1) * world_len)]["inventory"] = {"item": tile["inventory"][item_id]["item"]}
                                    if tile["inventory"][item_id]["amount"] != 1:
                                        tile["inventory"][item_id]["amount"] -= 1
                                    else:
                                        tile["inventory"][item_id] = {}
                                    world[x + ((y + 1) * world_len)]["not_gotta_work"] = True
                                break
                    elif tile["building"] == "conveyor_belt" and "item" in tile["inventory"]:
                        if tile["rotation"] == 0 and y - 1 < world_len and world[(x + 1) + (y * world_len)]["rotation"] == 0 and world[(x + 1) + (y * world_len)]["building"] in processors and processing_recepies[world[(x + 1) + (y * world_len)]["building"]][world[(x + 1) + (y * world_len)]["recepie"]]["required"][world[(x + 1) + (y * world_len)]["part"] - 1][0] == tile["inventory"]["item"]:
                            if world[(x + 1) + (y * world_len)]["inventory"][world[(x + 1) + (y * world_len)]["part"] - 1] == {}:
                                world[(x + 1) + (y * world_len)]["inventory"][world[(x + 1) + (y * world_len)]["part"] - 1] = {"item": tile["inventory"]["item"], "amount": 1}
                            else:
                                world[(x + 1) + (y * world_len)]["inventory"][world[(x + 1) + (y * world_len)]["part"] - 1]["amount"] += 1
                            tile["inventory"] = {}
                        elif tile["rotation"] == 90 and y - 1 < world_len and world[x + ((y - 1) * world_len)]["rotation"] == 90 and world[x + ((y - 1) * world_len)]["building"] in processors and processing_recepies[world[x + ((y - 1) * world_len)]["building"]][world[x + ((y - 1) * world_len)]["recepie"]]["required"][world[x + ((y - 1) * world_len)]["part"] - 1][0] == tile["inventory"]["item"]:
                            if world[x + ((y - 1) * world_len)]["inventory"][world[x + ((y - 1) * world_len)]["part"] - 1] == {}:
                                world[x + ((y - 1) * world_len)]["inventory"][world[x + ((y - 1) * world_len)]["part"] - 1] = {"item": tile["inventory"]["item"], "amount": 1}
                            else:
                                world[x + ((y - 1) * world_len)]["inventory"][world[x + ((y - 1) * world_len)]["part"] - 1]["amount"] += 1
                            tile["inventory"] = {}
                        elif tile["rotation"] == 180 and y - 1 < world_len and world[(x - 1) + (y * world_len)]["rotation"] == 180 and world[(x - 1) + (y * world_len)]["building"] in processors and processing_recepies[world[(x - 1) + (y * world_len)]["building"]][world[(x - 1) + (y * world_len)]["recepie"]]["required"][world[(x - 1) + (y * world_len)]["part"] - 1][0] == tile["inventory"]["item"]:
                            if world[(x - 1) + (y * world_len)]["inventory"][world[(x - 1) + (y * world_len)]["part"] - 1] == {}:
                                world[(x - 1) + (y * world_len)]["inventory"][world[(x - 1) + (y * world_len)]["part"] - 1] = {"item": tile["inventory"]["item"], "amount": 1}
                            else:
                                world[(x - 1) + (y * world_len)]["inventory"][world[(x - 1) + (y * world_len)]["part"] - 1]["amount"] += 1
                            tile["inventory"] = {}
                        elif tile["rotation"] == 270 and y + 1 < world_len and world[x + ((y + 1) * world_len)]["rotation"] == 270 and world[x + ((y + 1) * world_len)]["building"] in processors and processing_recepies[world[x + ((y + 1) * world_len)]["building"]][world[x + ((y + 1) * world_len)]["recepie"]]["required"][world[x + ((y + 1) * world_len)]["part"] - 1][0] == tile["inventory"]["item"]:
                            if world[x + ((y + 1) * world_len)]["inventory"][world[x + ((y + 1) * world_len)]["part"] - 1] == {}:
                                world[x + ((y + 1) * world_len)]["inventory"][world[x + ((y + 1) * world_len)]["part"] - 1] = {"item": tile["inventory"]["item"], "amount": 1}
                            else:
                                world[x + ((y + 1) * world_len)]["inventory"][world[x + ((y + 1) * world_len)]["part"] - 1]["amount"] += 1
                            tile["inventory"] = {}
                        elif tile["rotation"] == 0 and y - 1 < world_len and world[(x + 1) + (y * world_len)]["rotation"] == 0 and world[(x + 1) + (y * world_len)]["building"] == "storage_container":
                            for item_id, item in enumerate(world[(x + 1) + (y * world_len)]["inventory"]):
                                if item == {}:
                                    world[(x + 1) + (y * world_len)]["inventory"][item_id] = {"item": tile["inventory"]["item"], "amount": 1}
                                    tile["inventory"] = {}
                                    break
                                elif item != {} and item["item"] == tile["inventory"]["item"] and item["amount"] < 200:
                                    world[(x + 1) + (y * world_len)]["inventory"][item_id]["amount"] += 1
                                    tile["inventory"] = {}
                                    break
                        elif tile["rotation"] == 90 and y - 1 < world_len and world[x + ((y - 1) * world_len)]["rotation"] == 90 and world[x + ((y - 1) * world_len)]["building"] == "storage_container":
                            for item_id, item in enumerate(world[x + ((y - 1) * world_len)]["inventory"]):
                                if item == {}:
                                    world[x + ((y - 1) * world_len)]["inventory"][item_id] = {"item": tile["inventory"]["item"], "amount": 1}
                                    tile["inventory"] = {}
                                    break
                                elif item != {} and item["item"] == tile["inventory"]["item"] and item["amount"] < 200:
                                    world[x + ((y - 1) * world_len)]["inventory"][item_id]["amount"] += 1
                                    tile["inventory"] = {}
                                    break
                        elif tile["rotation"] == 180 and y - 1 < world_len and world[(x - 1) + (y * world_len)][item_id]["rotation"] == 180 and world[(x - 1) + (y * world_len)]["building"] == "storage_container":
                            for item_id, item in enumerate(world[(x - 1) + (y * world_len)]["inventory"]):
                                if item == {}:
                                    world[(x - 1) + (y * world_len)]["inventory"][item_id] = {"item": tile["inventory"]["item"], "amount": 1}
                                    tile["inventory"] = {}
                                    break
                                elif item != {} and item["item"] == tile["inventory"]["item"] and item["amount"] < 200:
                                    world[(x - 1) + (y * world_len)]["inventory"][item_id]["amount"] += 1
                                    tile["inventory"] = {}
                                    break
                        elif tile["rotation"] == 270 and y + 1 < world_len and world[x + ((y + 1) * world_len)]["rotation"] == 270 and world[x + ((y + 1) * world_len)]["building"] == "storage_container":
                            for item_id, item in enumerate(world[x + ((y + 1) * world_len)]["inventory"]):
                                if item == {}:
                                    world[x + ((y + 1) * world_len)]["inventory"][item_id] = {"item": tile["inventory"]["item"], "amount": 1}
                                    tile["inventory"] = {}
                                    break
                                elif item != {} and item["item"] == tile["inventory"]["item"] and item["amount"] < 200:
                                    world[x + ((y + 1) * world_len)]["inventory"][item_id]["amount"] += 1
                                    tile["inventory"] = {}
                                    break
                        elif tile["rotation"] == 0 and x + 1 < world_len and world[(x + 1) + (y * world_len)]["building"] == "conveyor_belt" and world[(x + 1) + (y * world_len)]["inventory"] == {} and not "not_gotta_work" in tile:
                            world[(x + 1) + (y * world_len)]["inventory"] = {"item": tile["inventory"]["item"]}
                            tile["inventory"] = {}
                            world[(x + 1) + (y * world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 90 and y - 1 >= 0 and world[x + ((y - 1) * world_len)]["building"] == "conveyor_belt" and world[x + ((y - 1) * world_len)]["inventory"] == {} and not "not_gotta_work" in tile:
                            world[x + ((y - 1) * world_len)]["inventory"] = {"item": tile["inventory"]["item"]}
                            tile["inventory"] = {}
                            world[x + ((y - 1) * world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 180 and x - 1 >= 0 and world[(x - 1) + (y * world_len)]["building"] == "conveyor_belt" and world[(x - 1) + (y * world_len)]["inventory"] == {} and not "not_gotta_work" in tile:
                            world[(x - 1) + (y * world_len)]["inventory"] = {"item": tile["inventory"]["item"]}
                            tile["inventory"] = {}
                            world[(x - 1) + (y * world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 270 and y + 1 < world_len and world[x + ((y + 1) * world_len)]["building"] == "conveyor_belt" and world[x + ((y + 1) * world_len)]["inventory"] == {} and not "not_gotta_work" in tile:
                            world[x + ((y + 1) * world_len)]["inventory"] = {"item": tile["inventory"]["item"]}
                            tile["inventory"] = {}
                            world[x + ((y + 1) * world_len)]["not_gotta_work"] = True
    
                    for c in clients:c.updBlocks.append({"id":tile_id,"tile":tile})                    
                    x += 1
                for tile in world:
                    if "not_gotta_work" in tile:
                        tile.pop("not_gotta_work")
                        for c in clients:c.updBlocks.append({"id":tile_id,"tile":tile})
        clock.tick(60)
        tick += 1


for i in range(0, world_len * world_len):
    world.append({"item": None, "building": None, "tile": "stone", "part": 0, "rotation": 0})

for i in range(0, random.randint(15, 40)):
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
    elif i == 5:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "uranium_ore", "part": 0, "rotation": 0}
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
    elif i == 5:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "uranium_ore", "part": 0, "rotation": 0}
        starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
x = random.randint(0, world_len - 3)
y = random.randint(0, world_len - 3)
for i in range(0, 3):
    for i1 in range(0, 3):
        world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "grass", "part": 0, "rotation": 0}
        starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
        if i == 1 and i1 == 1:
            world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "resin_ore", "part": 0, "rotation": 0}
            starting_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
for j in range(0,5):
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
            reply = {"world":world}
            reply = json.dumps(reply)
            connection.send((reply + "=").encode())
        except Exception as exc:
            print("[ERROR]", "An unexpected error occured while client was connecting")
            print("[EXCEPTION]", exc)
            continue
        print("[INFO]", "{} has connected".format(nickname))
        chat.append({"user":"Server","text":"{} has connected".format(nickname)})
        clients.append(Client(connection, nickname, len(clients)))

