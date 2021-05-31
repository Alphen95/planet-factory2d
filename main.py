import pygame as pg
import sys
import random
import os
import datetime
import socket
import threading
import json
from pprint import pprint

os.makedirs("logs", exist_ok=True)
log_file = open(os.path.join("logs", "log-{}.txt".format(str(datetime.datetime.now()).replace(":", "_   ")[:-7])), "w+")
log_file.write("[INFO] program started, time: {}\n".format(str(datetime.datetime.now())[:-7]))
SPECIAL_YELLOW = (220, 184, 10)
ppc_power = 253
ppc_batt = 1000
game_mode = "title"
selected = 0
temp_new_blocks = []
new_blocks = []
users = []
ip = "localhost"
port = "8000"
nick = "Player{}".format(random.randint(0,9999))
world_applied = False
category = 0
chat = []
recent_messages = []
current_message = ""
send = False
chat_open = False
recepies = [
    {
        "name":"Iron ingot",
        "required_text":"Iron ore",
        "output_text":"Iron ingot",
        "required":[[("unprocessed","iron"),1]],
        "output":{"item": ("ingot", "iron"), "amount": 1}
    },
    {
        "name":"Copper ingot",
        "required_text":"Copper ore",
        "output_text":"Copper ingot",
        "required":[[("unprocessed","copper"),1]],
        "output":{"item": ("ingot", "copper"), "amount": 1}
    },
    {
        "name":"Tungsten ingot",
        "required_text":"Tungsten ore",
        "output_text":"Tungsten ingot",
        "required":[[("unprocessed","tungsten"),1]],
        "output":{"item": ("ingot", "tungsten"), "amount": 1}
    },
    {
        "name":"Resin sheet",
        "required_text":"Sticky resin x2",
        "output_text":"Resin sheet",
        "required":[[("unprocessed","resin"),2]],
        "output":{"item": ("ingot", "resin"), "amount": 1}
    },
    {
        "name":"Iron plate",
        "required_text":"Iron ingot",
        "output_text":"Iron plate x 3",
        "required":[[("ingot","iron"),1]],
        "output":{"item": ("basic", "plate"), "amount": 3}
    },
    {
        "name":"Iron rod",
        "required_text":"Iron ingot",
        "output_text":"Iron rod x2",
        "required":[[("ingot","iron"),1]],
        "output":{"item": ("basic", "rod"), "amount": 2}
    }, 
    {
        "name":"Screws",
        "required_text":"Iron ingot",
        "output_text":"Screws x10",
        "required":[[("ingot","iron"),1]],
        "output":{"item": ("basic", "screws"), "amount": 10}
    }, 
    {
        "name":"Copper wire",
        "required_text":"Copper ingot",
        "output_text":"Copper wire x5",
        "required":[[("ingot","copper"),1]],
        "output":{"item": ("basic", "wire"), "amount": 5}
    }, 
    {
        "name":"Cable",
        "required_text":"Copper wire, Rubber sheet",
        "output_text":"Copper wire x5",
        "required":[[("basic","wire"),1],[("ingot","resin"),1]],
        "output":{"item": ("basic", "cable"), "amount": 1}
    },     
    {
        "name":"Portable drill",
        "required_text":"Iron plate x2, Iron rod x3",
        "output_text":"Portable drill",
        "required":[[("basic","plate"),2],[("basic","rod"),3]],
        "output":{"item": ("basic", "drill"), "amount": 1}
    }    
]

ui = {
    "tooltip": pg.image.load(os.path.join("res", "ui", "tooltip_box.png")),
    "ppc": pg.image.load(os.path.join("res", "ui", "pocket_comp.png")),
    "bat": {
        "0": pg.image.load(os.path.join("res", "ui", "bat_0.png")),
        "25": pg.image.load(os.path.join("res", "ui", "bat_25.png")),
        "50": pg.image.load(os.path.join("res", "ui", "bat_50.png")),
        "75": pg.image.load(os.path.join("res", "ui", "bat_75.png")),
        "100": pg.image.load(os.path.join("res", "ui", "bat_100.png"))
    },
    "inv_cell": pg.image.load(os.path.join("res", "ui", "inv_cell.png")),
    "cursor": pg.image.load(os.path.join("res", "ui", "cursor.png")),
    "title": pg.image.load(os.path.join("res", "ui", "title.png")),
    "titlename": pg.image.load(os.path.join("res", "ui", "titlename.png"))
}

player = {
    "default": [
        pg.image.load(os.path.join("res", "player", "state0.png")),
        pg.image.load(os.path.join("res", "player", "state1.png"))
    ],
    "dig": [
        pg.image.load(os.path.join("res", "player", "state0_dig0.png")),
        pg.image.load(os.path.join("res", "player", "state1_dig0.png"))
    ],
    "dig_active": [
        pg.image.load(os.path.join("res", "player", "state0_dig1.png")),
        pg.image.load(os.path.join("res", "player", "state1_dig1.png"))
    ]
}

resources = {
    "ingot": {
        "iron": pg.image.load(os.path.join("res", "resources", "ingot", "iron.png")),
        "copper": pg.image.load(os.path.join("res", "resources", "ingot", "copper.png")),
        "resin": pg.image.load(os.path.join("res", "resources", "ingot", "resin.png")),
        "leaves": pg.image.load(os.path.join("res", "resources", "ingot", "leaves.png")),
        "tungsten": pg.image.load(os.path.join("res", "resources", "ingot", "tungsten.png")),
        "coal": pg.image.load(os.path.join("res", "resources", "ingot", "coal.png"))
    },
    "raw_ore": {
        "iron": pg.image.load(os.path.join("res", "ores", "iron.png")),
        "copper": pg.image.load(os.path.join("res", "ores", "copper.png")),
        "resin": pg.image.load(os.path.join("res", "ores", "resin.png")),
        "leaves": pg.image.load(os.path.join("res", "ores", "leaves.png")),
        "tungsten": pg.image.load(os.path.join("res", "ores", "tungsten.png")),
        "uranium": pg.image.load(os.path.join("res", "ores", "uranium.png")),
        "coal": pg.image.load(os.path.join("res", "ores", "coal.png"))
    },
    "unprocessed": {
        "iron": pg.image.load(os.path.join("res", "resources", "unprocessed", "iron.png")),
        "copper": pg.image.load(os.path.join("res", "resources", "unprocessed", "copper.png")),
        "resin": pg.image.load(os.path.join("res", "resources", "unprocessed", "resin.png")),
        "leaves": pg.image.load(os.path.join("res", "resources", "unprocessed", "leaves.png")),
        "tungsten": pg.image.load(os.path.join("res", "resources", "unprocessed", "tungsten.png")),
        "coal": pg.image.load(os.path.join("res", "resources", "unprocessed", "coal.png")),
        "uranium": pg.image.load(os.path.join("res", "resources", "unprocessed", "uranium.png"))
    },
    "electronics": {
        "re_bat_0": pg.image.load(os.path.join("res", "resources", "electronics", "re_bat", "0.png")),
        "re_bat_25": pg.image.load(os.path.join("res", "resources", "electronics", "re_bat", "25.png")),
        "re_bat_50": pg.image.load(os.path.join("res", "resources", "electronics", "re_bat", "50.png")),
        "re_bat_75": pg.image.load(os.path.join("res", "resources", "electronics", "re_bat", "75.png")),
        "re_bat_100": pg.image.load(os.path.join("res", "resources", "electronics", "re_bat", "100.png"))
    },
    "bio": {
        "biofiber": pg.image.load(os.path.join("res", "resources", "bio", "biofiber.png")),
        "leaves": pg.image.load(os.path.join("res", "resources", "bio", "leaves.png"))
    },
    "basic":{
        "plate":pg.image.load(os.path.join("res", "resources", "basic", "iron_plate.png")),
        "rod":pg.image.load(os.path.join("res", "resources", "basic", "iron_rod.png")),
        "screws":pg.image.load(os.path.join("res", "resources", "basic", "screws.png")),
        "wire":pg.image.load(os.path.join("res", "resources", "basic", "wire_copper.png")),
        "cable":pg.image.load(os.path.join("res", "resources", "basic", "cable.png")),
        "drill":pg.image.load(os.path.join("res", "resources", "basic", "drill.png")),
    }
}

buildings = {
    "drill": [
        pg.image.load(os.path.join("res", "buildings", "drill_part1.png")),
        pg.image.load(os.path.join("res", "buildings", "drill_part2.png"))
    ],
    "conveyor": [
        pg.image.load(os.path.join("res", "buildings", "conveyor_belt0.png")),
        pg.image.load(os.path.join("res", "buildings", "conveyor_belt1.png")),
        pg.image.load(os.path.join("res", "buildings", "conveyor_belt2.png")),
        pg.image.load(os.path.join("res", "buildings", "conveyor_belt3.png"))
    ],
    "biomass_burner": [
        pg.image.load(os.path.join("res", "buildings", "biomass_burner.png"))
    ]
}

ground_tiles = [
    pg.image.load(os.path.join("res", "ground_tiles", "stone.png")),
    pg.image.load(os.path.join("res", "ground_tiles", "water.png")),
    pg.image.load(os.path.join("res", "ground_tiles", "grass.png"))
]

tick = 0
tooltip_tick = -1
tooltip_tile = {}
menu = "hidden"
menu_tick = 0
inventory = []
current_item = ["", 0]
mode = "!building"
power_capacity = 0
facing = 0
player_state = "default"
player_state_timer = 0
running_thread = True
starting_blocks = []

cell_size = 40
screen_size = (cell_size * 20, cell_size * 20)
world_len = 200

window = pg.display.set_mode(screen_size)
clock = pg.time.Clock()
pg.init()
pg.mouse.set_visible(False)
font = pg.font.SysFont("Verdana", 12)
dosfont = pg.font.Font(os.path.join("res", "dosfont.ttf"), int(12 * screen_size[1] / (40 * 20)))
dosfontbig = pg.font.Font(os.path.join("res", "dosfont.ttf"), 24)
pos = [int(world_len / 2), int(world_len / 2)]
menubar = []

sounds = {
    "msg":pg.mixer.Sound(os.path.join("res","snd","msg.wav"))
}


# world define
world = []
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


for i in range(0, 5):
    x = random.randint(0, world_len - 1)
    y = random.randint(0, world_len - 1)
    if i == 0 or i == 1:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "coal_ore", "part": 0, "rotation": 0}
        log_file.write("[DEBUG] placed coal ore in x:{0} y:{1}, time:{2}\n".format(x, y, str(datetime.datetime.now())[:-7]))
    elif i == 2:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "iron_ore", "part": 0, "rotation": 0}
        log_file.write("[DEBUG] placed iron ore in x:{0} y:{1}, time:{2}\n".format(x, y, str(datetime.datetime.now())[:-7]))
    elif i == 3:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "copper_ore", "part": 0, "rotation": 0}
        log_file.write("[DEBUG] placed copper ore in x:{0} y:{1}, time:{2}\n".format(x, y, str(datetime.datetime.now())[:-7]))
    elif i == 4:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "tungsten_ore", "part": 0, "rotation": 0}
        log_file.write("[DEBUG] placed tungsten ore in x:{0} y:{1}, time:{2}\n".format(x, y, str(datetime.datetime.now())[:-7]))
    elif i == 5:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "uranium_ore", "part": 0, "rotation": 0}
        log_file.write("[DEBUG] placed uranium ore in x:{0} y:{1}, time:{2}\n".format(x, y, str(datetime.datetime.now())[:-7]))    
for i1 in range(0, int((world_len - 20) / 2)):
    x = random.randint(0, world_len - 1)
    y = random.randint(0, world_len - 1)
    i = random.randint(0, 5)
    if i == 0 or i == 1:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "coal_ore", "part": 0, "rotation": 0}
        log_file.write("[DEBUG] placed coal ore in x:{0} y:{1}, time:{2}\n".format(x, y, str(datetime.datetime.now())[:-7]))
    elif i == 2:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "iron_ore", "part": 0, "rotation": 0}
        log_file.write("[DEBUG] placed iron ore in x:{0} y:{1}, time:{2}\n".format(x, y, str(datetime.datetime.now())[:-7]))
    elif i == 3:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "copper_ore", "part": 0, "rotation": 0}
        log_file.write("[DEBUG] placed copper ore in x:{0} y:{1}, time:{2}\n".format(x, y, str(datetime.datetime.now())[:-7]))
    elif i == 4:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "tungsten_ore", "part": 0, "rotation": 0}
        log_file.write("[DEBUG] placed tungsten ore in x:{0} y:{1}, time:{2}\n".format(x, y, str(datetime.datetime.now())[:-7]))
    elif i == 5:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "uranium_ore", "part": 0, "rotation": 0}
x = random.randint(0, world_len - 3)
y = random.randint(0, world_len - 3)
for i in range(0, 3):
    for i1 in range(0, 3):
        world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "grass", "part": 0, "rotation": 0}
        if i == 1 and i1 == 1:
            world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "resin _tree", "part": 0, "rotation": 0}
for j in range(0,10):
    x = random.randint(0, world_len - 3)
    y = random.randint(0, world_len - 3)    
    for i in range(0, 3):
        for i1 in range(0, 3):
            world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "grass", "part": 0, "rotation": 0}
            if i == 1 and i1 == 1:
                world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "resin_tree", "part": 0, "rotation": 0}

world[0] = {"item": None, "building": "drill", "tile": "coal_ore", "part": 1, "rotation": 0}
world[1] = {"item": None, "building": "drill", "tile": "stone", "part": 2, "rotation": 0}
world[2] = {"item": None, "building": "conveyor_belt", "tile": "stone", "part": 0, "rotation": 0}


def draw_world(world, winobj, tick, pos, tooltip_props, menu_props, edit_mode, player_props):
    winobj.fill((25, 25, 25))
    x = 0
    x1 = 0
    y = 0
    y1 = 0
    x_borders = [pos[0] - 10, pos[0] + 10]
    y_borders = [pos[1] - 10, pos[1] + 10]
    for tile_id, tile in enumerate(world):
        if x == world_len:
            x = 0
            y += 1
        if y >= y_borders[0] and y <= y_borders[1] and x >= x_borders[0] and x <= x_borders[1]:
            block = tile["tile"]
            block_rotation = tile["rotation"]
            block_part = tile["part"]
            block_building = tile["building"]
            x1 = x
            y1 = y
            if x_borders[0] < 0:
                x1 += abs(x_borders[0])
            else:
                x1 -= x_borders[0]
            if y_borders[0] < 0:
                y1 += abs(y_borders[0])
            else:
                y1 -= y_borders[0]
            if block == "stone":
                winobj.blit(pg.transform.scale(ground_tiles[0], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block == "coal_ore":
                winobj.blit(pg.transform.scale(resources["raw_ore"]["coal"], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block == "iron_ore":
                winobj.blit(pg.transform.scale(resources["raw_ore"]["iron"], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block == "copper_ore":
                winobj.blit(pg.transform.scale(resources["raw_ore"]["copper"], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block == "tungsten_ore":
                winobj.blit(pg.transform.scale(resources["raw_ore"]["tungsten"], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block == "uranium_ore":
                winobj.blit(pg.transform.scale(resources["raw_ore"]["uranium"], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))            
            elif block == "resin_tree":
                winobj.blit(pg.transform.scale(ground_tiles[2], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                winobj.blit(pg.transform.scale(resources["raw_ore"]["resin"], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block == "water":
                winobj.blit(pg.transform.scale(ground_tiles[1], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block == "grass":
                winobj.blit(pg.transform.scale(ground_tiles[2], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block == "leaves":
                winobj.blit(pg.transform.scale(ground_tiles[2], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                winobj.blit(pg.transform.scale(resources["raw_ore"]["leaves"], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            if block_building == "drill":
                if block_part == 1:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                elif block_part == 2:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block_building == "conveyor_belt":
                if tick <= 11:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                elif tick <= 22:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                elif tick <= 33:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                elif tick <= 44:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][3], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
        x += 1
    x1 = pos[0]
    y1 = pos[1]
    if x_borders[0] < 0:
        x1 += abs(x_borders[0])
    else:
        x1 -= x_borders[0]
    if y_borders[0] < 0:
        y1 += abs(y_borders[0])
    else:
        y1 -= y_borders[0]
    if tick > 21:
        winobj.blit(pg.transform.scale(pg.transform.flip(player[player_props[1]][1], player_props[0], False), (cell_size * 2, cell_size * 2)), ((x1 - 1) * cell_size, (y1 - 1) * cell_size))
    elif tick <= 21:
        winobj.blit(pg.transform.scale(pg.transform.flip(player[player_props[1]][0], player_props[0], False), (cell_size * 2, cell_size * 2)), ((x1 - 1) * cell_size, (y1 - 1) * cell_size))
    for user in users:
        x1 = user[0][0]
        y1 = user[0][1]
        if x_borders[0] < 0:
            x1 += abs(x_borders[0])
        else:
            x1 -= x_borders[0]
        if y_borders[0] < 0:
            y1 += abs(y_borders[0])
        else:
            y1 -= y_borders[0]
        if tick > 21:
            winobj.blit(pg.transform.scale(pg.transform.flip(player[user[2]][1], user[3], False), (cell_size * 2, cell_size * 2)), ((x1 - 1) * cell_size, (y1 - 1) * cell_size))
        elif tick <= 21:
            winobj.blit(pg.transform.scale(pg.transform.flip(player[user[2]][0], user[3], False), (cell_size * 2, cell_size * 2)), ((x1 - 1) * cell_size, (y1 - 1) * cell_size))
        text_name = dosfont.render(user[1], True, (0, 0, 0))
        winobj.blit(text_name, ((x1 - 1) * cell_size, (y1 - 1) * cell_size))
    if tooltip_props[0] != -1 and tooltip_props[1] != {}:
        block = tooltip_props[1]["tile"]
        block_rotation = tooltip_props[1]["rotation"]
        block_part = tooltip_props[1]["part"]
        block_building = tooltip_props[1]["building"]
        block_item = tooltip_props[1]["item"]
        ypos = 0
        xpos = 6 * cell_size
        if tooltip_props[0] >= 104:
            ypos = 3 * (104 - tooltip_props[0])
        if tooltip_props[0] <= 20:
            ypos = -60 + tooltip_props[0] * 3
        winobj.blit(pg.transform.scale(pg.transform.rotate(ui["tooltip"], 0), (190, 60)), (xpos + 10, ypos))
        text_tile = font.render("Tile:{}".format(block), True, (0, 0, 0))
        text_build = font.render("Building:{}".format(block_building), True, (0, 0, 0))
        text_item = font.render("Item:{}".format(block_item), True, (0, 0, 0))
        winobj.blit(text_tile, (xpos + 25 + cell_size, ypos + 5))
        winobj.blit(text_build, (xpos + 25 + cell_size, ypos + 17))
        winobj.blit(text_item, (xpos + 25 + cell_size, ypos + 30))
        if block == "stone":
            winobj.blit(pg.transform.scale(ground_tiles[0], (cell_size, cell_size)), (xpos + 20, ypos + 10))
        elif block == "coal_ore":
            winobj.blit(pg.transform.scale(resources["raw_ore"]["coal"], (cell_size, cell_size)), (xpos + 20, ypos + 10))
        elif block == "iron_ore":
            winobj.blit(pg.transform.scale(resources["raw_ore"]["iron"], (cell_size, cell_size)), (xpos + 20, ypos + 10))
        elif block == "copper_ore":
            winobj.blit(pg.transform.scale(resources["raw_ore"]["copper"], (cell_size, cell_size)), (xpos + 20, ypos + 10))
        elif block == "tungsten_ore":
            winobj.blit(pg.transform.scale(resources["raw_ore"]["tungsten"], (cell_size, cell_size)), (xpos + 20, ypos + 10))
        elif block == "uranium_ore":
            winobj.blit(pg.transform.scale(resources["raw_ore"]["uranium"], (cell_size, cell_size)), (xpos + 20, ypos + 10))        
        elif block == "resin_tree":
            winobj.blit(pg.transform.scale(ground_tiles[2], (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            winobj.blit(pg.transform.scale(resources["raw_ore"]["resin"], (cell_size, cell_size)), (xpos + 20, ypos + 10))
        elif block == "water":
            winobj.blit(pg.transform.scale(ground_tiles[1], (cell_size, cell_size)), (xpos + 20, ypos + 10))
        elif block == "grass":
            winobj.blit(pg.transform.scale(ground_tiles[2], (cell_size, cell_size)), (xpos + 20, ypos + 10))
        elif block == "leaves":
            winobj.blit(pg.transform.scale(ground_tiles[2], (cell_size, cell_size)), (xpos + 20, ypos + 10))
            winobj.blit(pg.transform.scale(resources["raw_ore"]["leaves"], (cell_size, cell_size)), (xpos + 20, ypos + 10))
        if block_building == "drill":
            if block_part == 1:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][0], block_rotation), (cell_size, cell_size)), (xpos + 20, ypos + 10))
            elif block_part == 2:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][1], block_rotation), (cell_size, cell_size)), (xpos + 20, ypos + 10))
        elif block_building == "conveyor_belt":
            if tick <= 11:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0], block_rotation), (cell_size, cell_size)), (xpos + 20, ypos + 10))
            elif tick <= 22:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1], block_rotation), (cell_size, cell_size)), (xpos + 20, ypos + 10))
            elif tick <= 33:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2], block_rotation), (cell_size, cell_size)), (xpos + 20, ypos + 10))
            elif tick <= 44:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][3], block_rotation), (cell_size, cell_size)), (xpos + 20, ypos + 10))

    if edit_mode:
        winobj.blit(pg.transform.scale(pg.transform.rotate(ui["ppc"], 0), (cell_size * 6, cell_size * 12)), (5, screen_size[1] + 10 - cell_size * 8))
        if current_item[0] != "":
            if tick <= 22:
                text_tile = dosfont.render(">ROTATE: [R]", True, (0, 0, 0))
                text_tile2 = dosfont.render(">CURRENT_ROT", True, (0, 0, 0))
                text_rot = dosfont.render(str(current_item[1]), True, (0, 0, 0))
                text_tile3 = dosfont.render(">CURRENT_ITM", True, (0, 0, 0))
                text_item = dosfont.render(str(current_item[0]), True, (0, 0, 0))
                text_cancel = dosfont.render(str("5>CANCEL"), True, (0, 0, 0))
                winobj.blit(text_tile, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20 * 5) - cell_size * 4) * 1.25))))
                winobj.blit(text_tile2, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20) - cell_size * 4) * 1.25))))
                winobj.blit(text_rot, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 2) - cell_size * 4) * 1.25)))
                winobj.blit(text_tile3, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 3) - cell_size * 4) * 1.25)))
                winobj.blit(text_item, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 4) - cell_size * 4) * 1.25))))
                winobj.blit(text_cancel, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 5) - cell_size * 4) * 1.25))))
            else:
                text_tile = dosfont.render(">REQUIRED", True, (0, 0, 0))
                text_tile2 = dosfont.render(">"+current_item[2][0], True, (0, 0, 0))
                text_rot = dosfont.render(">"+current_item[2][1], True, (0, 0, 0))
                text_tile3 = dosfont.render(">"+current_item[2][2], True, (0, 0, 0))
                text_item = dosfont.render(">"+current_item[2][3], True, (0, 0, 0))
                text_cancel = dosfont.render(str("5>CANCEL"), True, (0, 0, 0))
                winobj.blit(text_tile, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20 * 5) - cell_size * 4) * 1.25))))
                winobj.blit(text_tile2, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20) - cell_size * 4) * 1.25))))
                winobj.blit(text_rot, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 2) - cell_size * 4) * 1.25)))
                winobj.blit(text_tile3, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 3) - cell_size * 4) * 1.25)))
                winobj.blit(text_item, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 4) - cell_size * 4) * 1.25))))
                winobj.blit(text_cancel, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 5) - cell_size * 4) * 1.25))))                
        else:
            if category == 0:
                text_line1 = dosfont.render("CATEGORY: MAIN", True, (0, 0, 0))
                text_line2 = dosfont.render("1>MINING", True, (0, 0, 0))
                text_line3 = dosfont.render("2>LOGIC", True, (0, 0, 0))
                text_line4 = dosfont.render("3>LOGISITC", True, (0, 0, 0))
                text_line5 = dosfont.render("4>PROCESSING", True, (0, 0, 0))
                text_line6 = dosfont.render("5>DISASSEMBLE", True, (0, 0, 0))
                winobj.blit(text_line1, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20 * 5) - cell_size * 4) * 1.25))))
                winobj.blit(text_line2, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20) - cell_size * 4) * 1.25))))
                winobj.blit(text_line3, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 2) - cell_size * 4) * 1.25)))
                winobj.blit(text_line4, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 3) - cell_size * 4) * 1.25)))
                winobj.blit(text_line5, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 4) - cell_size * 4) * 1.25))))
                winobj.blit(text_line6, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 5) - cell_size * 4) * 1.25))))   
            elif category == 1:
                text_line1 = dosfont.render("CATEGORY: MINING", True, (0, 0, 0))
                text_line2 = dosfont.render("1>DRILL_MK1", True, (0, 0, 0))
                text_line3 = dosfont.render("2>", True, (0, 0, 0))
                text_line4 = dosfont.render("3>", True, (0, 0, 0))
                text_line5 = dosfont.render("4>", True, (0, 0, 0))
                text_line6 = dosfont.render("5>BACK", True, (0, 0, 0))
                winobj.blit(text_line1, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20 * 5) - cell_size * 4) * 1.25))))
                winobj.blit(text_line2, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20) - cell_size * 4) * 1.25))))
                winobj.blit(text_line3, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 2) - cell_size * 4) * 1.25)))
                winobj.blit(text_line4, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 3) - cell_size * 4) * 1.25)))
                winobj.blit(text_line5, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 4) - cell_size * 4) * 1.25))))
                winobj.blit(text_line6, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 5) - cell_size * 4) * 1.25))))     
            elif category == 1:
                text_line1 = dosfont.render("CATEGORY: LOGIC", True, (0, 0, 0))
                text_line2 = dosfont.render("1>", True, (0, 0, 0))
                text_line3 = dosfont.render("2>", True, (0, 0, 0))
                text_line4 = dosfont.render("3>", True, (0, 0, 0))
                text_line5 = dosfont.render("4>", True, (0, 0, 0))
                text_line6 = dosfont.render("5>BACK", True, (0, 0, 0))
                winobj.blit(text_line1, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20 * 5) - cell_size * 4) * 1.25))))
                winobj.blit(text_line2, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20) - cell_size * 4) * 1.25))))
                winobj.blit(text_line3, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 2) - cell_size * 4) * 1.25)))
                winobj.blit(text_line4, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 3) - cell_size * 4) * 1.25)))
                winobj.blit(text_line5, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 4) - cell_size * 4) * 1.25))))
                winobj.blit(text_line6, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 5) - cell_size * 4) * 1.25))))     
            elif category == 1:
                text_line1 = dosfont.render("CATEGORY: MINING", True, (0, 0, 0))
                text_line2 = dosfont.render("1>CONV_BELT_MK1", True, (0, 0, 0))
                text_line3 = dosfont.render("2>", True, (0, 0, 0))
                text_line4 = dosfont.render("3>", True, (0, 0, 0))
                text_line5 = dosfont.render("4>", True, (0, 0, 0))
                text_line6 = dosfont.render("5>BACK", True, (0, 0, 0))
                winobj.blit(text_line1, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20 * 5) - cell_size * 4) * 1.25))))
                winobj.blit(text_line2, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20) - cell_size * 4) * 1.25))))
                winobj.blit(text_line3, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 2) - cell_size * 4) * 1.25)))
                winobj.blit(text_line4, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 3) - cell_size * 4) * 1.25)))
                winobj.blit(text_line5, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 4) - cell_size * 4) * 1.25))))
                winobj.blit(text_line6, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 5) - cell_size * 4) * 1.25))))                 
    if menu_props[1] != "hidden":
        ypos = 0
        xpos = 0
        if menu_props[1] == "opening" or menu_props[1] == "open":
            xpos = 0 * (cell_size / 2)
        elif menu_props[1] == "closing" or menu_props[1] == "hidden":
            xpos = screen_size[0] - 0 * (cell_size / 2)
        pg.draw.polygon(winobj, (0, 0, 0), [[xpos, ypos], [xpos + screen_size[0] + 10, ypos], [xpos + screen_size[0] + 10, ypos + screen_size[1] - 70], [xpos, ypos + screen_size[1] - 70]])
        pg.draw.polygon(winobj, SPECIAL_YELLOW, [[xpos + 5, ypos + 5], [xpos + screen_size[0] + 10, ypos + 5], [xpos + screen_size[0] + 10, ypos + screen_size[1] - 75], [xpos + 5, ypos + screen_size[1] - 75]])
        for y in range(0, 3):
            for x in range(0, 9):
                try:
                    winobj.blit(pg.transform.scale(ui["inv_cell"], (cell_size * 2, cell_size * 2)), (xpos + 5 + 10 * x + (cell_size * 2) * x, ypos + 5 + 10 * y + (cell_size * 2) * y))
                    item = inventory[x + y * 9]["item"]
                    item_amount = inventory[x + y * 9]["amount"]
                    winobj.blit(pg.transform.scale(resources[item[0]][item[1]], (cell_size * 2, cell_size * 2)), (xpos + 10 * x + (cell_size * 2) * x, ypos + 10 * y + (cell_size * 2) * y))
                    text_amount = dosfont.render(str(item_amount), True, (255, 255, 255))
                    winobj.blit(text_amount, (xpos + 10 * x + (cell_size * 2) * x + (cell_size * 2) - 11, ypos + 10 * y + (cell_size * 2) * y + (cell_size * 2) - 11))
                except:
                    pass
        x = 0
        y = 0
        for recepie in recepies:
            if x >6:
                x = 0
                y +=1
            pg.draw.rect(winobj,(0,0,0),(xpos+10+y*153,ypos+310+x*60,150,50))
            pg.draw.rect(winobj,(200,200,200),(xpos+10+y*157,ypos+310+x*60,148,48))
            text_name = dosfont.render(recepie["name"], True, (0,0,0))
            winobj.blit(text_name, (xpos+10+y*160,ypos+310+x*60))
            text_required = dosfont.render("Need:"+recepie["required_text"], True, (0,0,0))
            winobj.blit(text_required, (xpos+10+y*160,ypos+325+x*60))
            text_result = dosfont.render("Will give: "+recepie["output_text"], True, (0,0,0))
            winobj.blit(text_result, (xpos+10+y*160,ypos+340+x*60))            
            x+=1
    if chat_open:
        pg.draw.rect(winobj,(100,100,100),(0,0,screen_size[1],300))
        if len(chat) <=14:
            for message_id, message in enumerate(chat):
                text_message= dosfontbig.render(message["user"]+" : "+message["text"], True, (0, 255, 0))
                winobj.blit(text_message, (0,20*message_id)) 
        elif len(chat) >14:
            for message_id, message in enumerate(chat[-14:]):
                text_message= dosfontbig.render(message["user"]+" : "+message["text"], True, (0, 255, 0))
                winobj.blit(text_message, (0,20*message_id))             
        text_message= dosfontbig.render(">"+current_message, True, (0, 255, 0))
        winobj.blit(text_message, (0,20*14)) 
    else:
        if len(recent_messages) <= 14:
            for message_id, message in enumerate(recent_messages):
                text_message= dosfontbig.render(message["user"]+" : "+message["text"], True, (0, 255, 0))
                winobj.blit(text_message, (0,20*message_id))    
        elif len(recent_messages) > 14:
            for message_id, message in enumerate(recent_messages[-14:]):
                text_message= dosfontbig.render(message["user"]+" : "+message["text"], True, (0, 255, 0))
                winobj.blit(text_message, (0,20*message_id))    



def draw_title(winobj):
    for i in range(0, 64):
        for i1 in range(0, 64):
            winobj.blit(pg.transform.scale(ui["title"], (cell_size * 2, cell_size * 2)), (i1 * (cell_size * 2), i * (cell_size * 2)))
    winobj.blit(pg.transform.scale(ui["titlename"], (cell_size * 10, cell_size * 5)), (5 * cell_size, 3 * cell_size))
    pg.draw.rect(winobj, (100, 100, 100), (cell_size * 4, cell_size * 12, cell_size * 4, cell_size * 0.5))
    pg.draw.rect(winobj, (100, 100, 100), (cell_size * 4, cell_size * 14, cell_size * 4, cell_size * 0.5))
    text_singleplayer = dosfontbig.render(">Singleplayer", True, (0, 255, 0))
    text_multiplayer = dosfontbig.render(">Multiplayer", True, (0, 255, 0))
    winobj.blit(text_singleplayer, (cell_size * 4, cell_size * 12))
    winobj.blit(text_multiplayer, (cell_size * 4, cell_size * 14))

def draw_splash(winobj,splash):
    for i in range(0, 64):
        for i1 in range(0, 64):
            winobj.blit(pg.transform.scale(ui["title"], (cell_size * 2, cell_size * 2)), (i1 * (cell_size * 2), i * (cell_size * 2)))
    text_splash1 = dosfontbig.render(splash[0], True, (0, 255, 0))
    text_splash2 = dosfontbig.render(splash[1], True, (0, 255, 0))
    winobj.blit(text_splash1,(cell_size*5,cell_size*5))
    winobj.blit(text_splash2,(cell_size*4,cell_size*6))

def draw_multiplayer(winobj, port, ip, nick):
    for i in range(0, 64):
        for i1 in range(0, 64):
            winobj.blit(pg.transform.scale(ui["title"], (cell_size * 2, cell_size * 2)), (i1 * (cell_size * 2), i * (cell_size * 2)))
    winobj.blit(pg.transform.scale(ui["titlename"], (cell_size * 10, cell_size * 5)), (5 * cell_size, 3 * cell_size))
    pg.draw.rect(winobj, (100, 100, 100), (cell_size * 4, cell_size * 12, cell_size * 8, cell_size * 0.5))
    pg.draw.rect(winobj, (100, 100, 100), (cell_size * 4, cell_size * 14, cell_size * 8, cell_size * 0.5))
    pg.draw.rect(winobj, (100, 100, 100), (cell_size * 4, cell_size * 10, cell_size * 8, cell_size * 0.5))
    text_port = dosfontbig.render("Port>" + str(port), True, (0, 255, 0))
    text_ip = dosfontbig.render("IP>" + str(ip), True, (0, 255, 0))
    text_nickname = dosfontbig.render("Nick>" + nick, True, (0, 255, 0))
    winobj.blit(text_port, (cell_size * 4, cell_size * 12))
    winobj.blit(text_ip, (cell_size * 4, cell_size * 14))
    winobj.blit(text_nickname, (cell_size * 4, cell_size * 10))


# main cycle
while 1:
    if game_mode == "singleplayer" or game_mode == "multiplayer":
        '''
        for item in inventory:
            if item["item"] ==("unprocessed","iron"):
                item["info"] = ("Iron ore","Basic metal.","Used almost every-","where.","","")
            elif item["item"] ==("unprocessed","copper"):
                item["info"] = ("Copper ore","Electroconductive","and heat-conductive","metal.","","")
            elif item["item"] ==("unprocessed","tungsten"):
                item["info"] = ("Tungsten ore","Advanced metal. Used","to make complicated","circutry","","")
            elif item["item"] ==("unprocessed","coal"):
                item["info"] = ("Coal","Natural resource.","Good for making steel","","","")
            elif item["item"] ==("unprocessed","resin"):
                item["info"] = ("Sticky resin","Perfect material to","isolate something.","","","")
            elif item["item"] ==("unprocessed","uranium"):
                item["info"] = ("Uranium ore","Radioactive metal.","Power source for this","whole planet.","","")
            elif item["item"] ==("ingot","iron"):
                item["info"] = ("Iron ingot","A heavy ingot that","can be used in many","ways.","","")
            elif item["item"] ==("ingot","copper"):
                item["info"] = ("Copper ingot","One step from being a","copper wire or a","heat conduction pipe","","")
            elif item["item"] ==("ingot","tungsten"):
                item["info"] = ("Tungsten ingot","Does it have any","purpose in this form?","","","")
            elif item["item"] ==("ingot","resin"):
                item["info"] = ("Resin sheet","Used to make cables,","fix-tape and some other","electronics","","")
            elif item["item"] ==("basic","plate"):
                item["info"] = ("Iron plate","Basic sheet of metal.","Good for some basic buildings.","","","")
            elif item["item"] ==("basic","rod"):
                item["info"] = ("Iron rod","Supporting element in","basic buildings","","","")
            elif item["item"] ==("basic","screws"):
                item["info"] = ("Screws","Very useful part.","Can repair and be used","in almost everything","","")
            elif item["item"] ==("basic","wire_copper"):
                item["info"] = ("Copper wire","Higly electroconductive","wire. Used in basic electronics.","","","")
            elif item["item"] ==("basic","cable"):
                item["info"] = ("Cable","Isoalted wire. Used to","transmit energy.","","","")
            elif item["item"] ==():
                item["info"] = ("","","","","","")
            elif item["item"] ==():
                item["info"] = ("","","","","","")
            '''
        temp_new_blocks = []
        if tick == 44:
            if mode == "building" and ppc_power != 0:
                ppc_power -= 1
            tick = 0
            power_capacity = 0
            for tile_id, tile in enumerate(world):
                if tile["tile"] == "biomass_burner":
                    power_capacity += 100
                elif tile["tile"] == "coal_plant" and tile["part"] == 1:
                    power_capacity += 250
                elif tile["tile"] == "drill" and tile["part"] == 1:
                    power_capacity -= 25
                if tile["tile"] == "grass" and random.randint(0, 25) == 0 and tile["building"] == None and game_mode == "singleplayer":
                    world[tile_id]["tile"] = "leaves"
        if recent_messages != []:
            for msg_id,msg in reversed(list(enumerate(recent_messages))):
                if msg["timer"] <= 0:
                    recent_messages.pop(msg_id)
                elif msg["timer"] > 0:
                    msg["timer"] -= 1            
        if tooltip_tick != -1:
            tooltip_tick -= 1
        if menu_tick != 0:
            menu_tick -= 1
        if tooltip_tick == -1:
            tooltip_tile = {}
        if player_state_timer == 0 and player_state == "dig_active":
            player_state = "dig"
            player_state_timer = 15
        elif player_state_timer == 0 and player_state != "ppc":
            player_state = "default"
        if player_state_timer > 0:
            player_state_timer -= 1
        if menu_tick == 0 and menu == "closing":
            menu = "hidden"
        if menu_tick == 0 and menu == "opening":
            menu = "open"
        draw_world(world, window, tick, pos, [tooltip_tick, tooltip_tile], [menu_tick, menu], mode == "building", [facing != 0, player_state])
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                running_thread = False
                pg.quit()
                sys.exit()
            elif evt.type == pg.KEYDOWN:

                keys = pg.key.get_pressed()
                if keys[pg.K_m]:
                    if mode == "building":
                        mode = "!building"
                    elif mode == "!building":
                        mode = "building"
                elif keys[pg.K_TAB] and menu == "hidden" and game_mode == "multiplayer":
                    if not(chat_open): recent_messages = []
                    chat_open = not(chat_open)
                elif keys[pg.K_r]  and not(chat_open):
                    if current_item[1] != 270:
                        current_item[1] += 90
                    else:
                        current_item[1] = 0
                elif keys[pg.K_5] and category != 0 or keys[pg.K_5] and current_item[0] != "" and not(chat_open):
                    category = 0
                    current_item = ["",0]
                elif keys[pg.K_5] and category == 0 and not(chat_open):
                    current_item = ["disassemble",0]                
                elif keys[pg.K_1] and category == 0 and not(chat_open):
                    category = 1            
                elif keys[pg.K_1] and category == 1 and not(chat_open):
                    current_item = ["drill",0,("Basic drill","Iron plate x3","Copper wire x5",""),((("basic","drill"),1),(("basic","plate"),3),(("basic","wire"),5))]   
                elif chat_open:
                    if evt.key == pg.K_BACKSPACE:
                        current_message = current_message[:-1]
                    elif evt.key ==pg.K_RETURN:
                        send = True
                    else:
                        current_message += evt.unicode
            elif evt.type == pg.MOUSEBUTTONDOWN:
                coords = evt.pos
                # tooltip on middle-click
                # build on left-click
                x = int(coords[1] / cell_size)
                y = int(coords[0] / cell_size)
                x2 = 0
                y2 = 0
                x_borders = [pos[0] - 10, pos[0] + 10]
                y_borders = [pos[1] - 10, pos[1] + 10]
                visible_part = {}
                for x1 in range(x_borders[0], x_borders[1]):
                    for y1 in range(y_borders[0], y_borders[1]):
                        visible_part[str(x1) + "_" + str(y1)] = {}
                for i in range(0, len(world)):
                    if x2 == world_len:
                        x2 = 0
                        y2 += 1
                    if x2 >= x_borders[0] and x2 <= x_borders[1] and y2 >= y_borders[0] and y2 <= y_borders[1]:
                        visible_part[str(x2) + "_" + str(y2)] = world[i]
                    x2 += 1
                true_visible_part = []
                for x1 in range(x_borders[0], x_borders[1]):
                    for y1 in range(y_borders[0], y_borders[1]):
                        true_visible_part.append(visible_part[str(x1) + "_" + str(y1)])
                if evt.button == 1:
                    if menu == "open":
                        x = 0
                        y = 0
                        for recepie in recepies: #(xpos+10+y*155,ypos+310+x*60,150,50)
                            if x > 6:
                                x = 0
                                y += 1
                            can_craft = False
                            added = False
                            item_ids = []
                            ids_to_pop = []
                            if coords[0] >= 10+y*155 and coords[0] <= 10+y*155+150 and coords[1] >=310+x*60 and coords[1] < 310+x*60+50 and len(inventory) < 30:
                                for item in recepie["required"]:
                                    for inv_item_id, inv_item in enumerate(inventory):
                                        if item[0] == inv_item["item"] and item[1] <= inv_item["amount"]:
                                            can_craft = True
                                            item_ids.append([inv_item_id,item[1]])
                                            pprint(recepie)
                                            break
                                    if can_craft == False:  
                                        break
                                if can_craft:

                                    a = recepie["output"].copy()                                  
                                    for item_id in item_ids:
                                        item = inventory[item_id[0]]
                                        if item["amount"] > item_id[1]:
                                            inventory[item_id[0]]["amount"] -= item_id[1]
                                        else:
                                            ids_to_pop.append(item_id[0])
                                    for id_to_pop in ids_to_pop:
                                        inventory.pop(id_to_pop)
                                    for item_id, item in enumerate(inventory):
                                        if item["item"] == recepie["output"]["item"]  and item["amount"] < 200:
                                            for i in range(0,recepie["output"]["amount"]):
                                                inventory[item_id]["amount"] = inventory[item_id]["amount"] + 1
                                            added = True
                                    if not(added):
                                        inventory.append(recepie["output"])
                                    
                                    pprint(recepie)
                                    print("=======")
                                    recepie["output"]   = a
                            x+=1
                    x = int(coords[0] / cell_size)
                    y = int(coords[1] / cell_size)
                    if x_borders[0] < 0:
                        x -= abs(x_borders[0])
                    else:
                        x += x_borders[0]
                    if y_borders[0] < 0:
                        y -= abs(y_borders[0])
                    else:
                        y += y_borders[0]
                    if mode == "building" and not(chat_open) and menu == "hidden":
                        can_craft = False
                        added = False
                        item_ids = []
                        ids_to_pop = []
                        for item in current_item[3]:
                            for inv_item_id, inv_item in enumerate(current_item[3]):
                                if item[0] == inv_item["item"] and item[1] <= inv_item["amount"]:
                                    can_craft = True
                                    item_ids.append((inv_item_id,item[1]))
                                    break
                            if can_craft == False:  
                                break
                        if can_craft:
                            for item_id in item_ids:
                                item = current_item[3][item_id[0]]
                                if item["amount"] > item_id[1]:
                                    item["amount"] -= item_id[1]
                                else:
                                    ids_to_pop.append(item_id[0])
                            for id_to_pop in ids_to_pop:
                                current_item[3].pop(id_to_pop)
                            added = True                         
                        if current_item[0] == "drill" and added:
                            if current_item[1] == 0:
                                if x >= 0 and x < world_len - 1 and y >= 0 and y <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[(x + 1) + (y * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[(x + 1) + (y * world_len)]["tile"] == "leaves":
                                        world[(x + 1) + (y * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "drill"
                                    world[(x + 1) + (y * world_len)]["building"] = "drill"
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[(x + 1) + (y * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 1
                                    world[(x + 1) + (y * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                            elif current_item[1] == 90:
                                if y > 0 and y <= world_len - 1 and x >= 0 and x <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[x + ((y - 1) * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[x + ((y - 1) * world_len)]["tile"] == "leaves":
                                        world[x + ((y - 1) * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "drill"
                                    world[x + ((y - 1) * world_len)]["building"] = "drill"
                                    world[x + (y * world_len)]["rotation"] = 90
                                    world[x + ((y - 1) * world_len)]["rotation"] = 90
                                    world[x + (y * world_len)]["part"] = 1
                                    world[x + ((y - 1) * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                    print("a", new_blocks)
                            elif current_item[1] == 180:
                                if x > 0 and x <= world_len - 1 and y >= 0 and y <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[(x - 1) + (y * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[(x - 1) + (y * world_len)]["tile"] == "leaves":
                                        world[(x - 1) + (y * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "drill"
                                    world[(x - 1) + (y * world_len)]["building"] = "drill"
                                    world[x + (y * world_len)]["rotation"] = 180
                                    world[(x - 1) + (y * world_len)]["rotation"] = 180
                                    world[x + (y * world_len)]["part"] = 1
                                    world[(x - 1) + (y * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x - 1) + (y * world_len)]})
                            elif current_item[1] == 270:
                                if y >= 0 and y < world_len - 1 and x >= 0 and x <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[x + ((y + 1) * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[x + ((y + 1) * world_len)]["tile"] == "leaves":
                                        world[x + ((y + 1) * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "drill"
                                    world[x + ((y + 1) * world_len)]["building"] = "drill"
                                    world[x + (y * world_len)]["rotation"] = 270
                                    world[x + ((y + 1) * world_len)]["rotation"] = 270
                                    world[x + (y * world_len)]["part"] = 1
                                    world[x + ((y + 1) * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y + 1) * world_len)]})
                        elif current_item[0] == "disassemble":
                            if world[x + (y * world_len)]["building"] == "drill" and world[x + (y * world_len)]["rotation"] == 0:
                                if world[x + (y * world_len)]["part"] == 1:
                                    world[x + (y * world_len)]["building"] = None
                                    world[(x + 1) + (y * world_len)]["building"] = None
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[(x + 1) + (y * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 0
                                    world[(x + 1) + (y * world_len)]["part"] = 0
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                                else:
                                    world[x + (y * world_len)]["building"] = None
                                    world[(x - 1) + (y * world_len)]["building"] = None
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[(x - 1) + (y * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 0
                                    world[(x - 1) + (y * world_len)]["part"] = 0
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})                                    
                            if world[x + (y * world_len)]["building"] == "drill" and world[x + (y * world_len)]["rotation"] == 90:
                                if world[x + (y * world_len)]["part"] == 1:
                                    world[x + (y * world_len)]["building"] = None
                                    world[x + ((y - 1) * world_len)]["building"] = None
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[x + ((y - 1) * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 0
                                    world[x + ((y - 1) * world_len)]["part"] = 0
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                else:
                                    world[x + (y * world_len)]["building"] = None
                                    world[x + ((y + 1) * world_len)]["building"] = None
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[x + ((y + 1) * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 0
                                    world[x + ((y + 1) * world_len)]["part"] = 0
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})                                    
                            if world[x + (y * world_len)]["building"] == "drill" and world[x + (y * world_len)]["rotation"] == 180:
                                if world[x + (y * world_len)]["part"] == 2:
                                    world[x + (y * world_len)]["building"] = None
                                    world[(x + 1) + (y * world_len)]["building"] = None
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[(x + 1) + (y * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 0
                                    world[(x + 1) + (y * world_len)]["part"] = 0
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                                else:
                                    world[x + (y * world_len)]["building"] = None
                                    world[(x - 1) + (y * world_len)]["building"] = None
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[(x - 1) + (y * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 0
                                    world[(x - 1) + (y * world_len)]["part"] = 0
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})         
                            if world[x + (y * world_len)]["building"] == "drill" and world[x + (y * world_len)]["rotation"] == 270:
                                if world[x + (y * world_len)]["part"] == 2:
                                    world[x + (y * world_len)]["building"] = None
                                    world[x + ((y - 1) * world_len)]["building"] = None
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[x + ((y - 1) * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 0
                                    world[x + ((y - 1) * world_len)]["part"] = 0
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                else:
                                    world[x + (y * world_len)]["building"] = None
                                    world[x + ((y + 1) * world_len)]["building"] = None
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[x + ((y + 1) * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 0
                                    world[x + ((y + 1) * world_len)]["part"] = 0
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})  
                            
                elif evt.button == 2 and not(chat_open):
                    tooltip_tile = true_visible_part[x + y * 20]
                    tooltip_tick = 125

        keys = pg.key.get_pressed()
        if tick % 2 == 0 and not(chat_open):
            keys = pg.key.get_pressed()
            if keys[pg.K_LALT]:
                speed = 4
            else:
                speed = 1
            if keys[pg.K_UP] and pos[1] != 0 or keys[pg.K_w] and pos[1] != 0:
                pos[1] -= speed
            if keys[pg.K_DOWN] and pos[1] != world_len or keys[pg.K_s] and pos[1] != world_len:
                pos[1] += speed
            if keys[pg.K_LEFT] and pos[0] != 0 or keys[pg.K_a] and pos[0] != 0:
                pos[0] -= speed
                facing = 0
            if keys[pg.K_RIGHT] and pos[0] != world_len or keys[pg.K_d] and pos[0] != world_len:
                pos[0] += speed
                facing = 1
        if tick % 3 == 0 and menu_tick == 0 and not(chat_open):
            if keys[pg.K_e] and menu == "hidden":
                menu = "opening"
                menu_tick = 10
            elif keys[pg.K_e] and menu == "open":
                menu = "closing"
                menu_tick = 10

        if player_state_timer == 0 and not(chat_open):
            coords = pg.mouse.get_pos()
            # tooltip on middle-click
            # build on left-click
            x = int(coords[1] / cell_size)
            y = int(coords[0] / cell_size)
            x2 = 0
            y2 = 0
            x_borders = [pos[0] - 10, pos[0] + 10]
            y_borders = [pos[1] - 10, pos[1] + 10]
            visible_part = {}
            for x1 in range(x_borders[0], x_borders[1]):
                for y1 in range(y_borders[0], y_borders[1]):
                    visible_part[str(x1) + "_" + str(y1)] = {}
            for i in range(0, len(world)):
                if x2 == world_len:
                    x2 = 0
                    y2 += 1
                if x2 >= x_borders[0] and x2 <= x_borders[1] and y2 >= y_borders[0] and y2 <= y_borders[1]:
                    visible_part[str(x2) + "_" + str(y2)] = world[i]
                x2 += 1
            true_visible_part = []
            for x1 in range(x_borders[0], x_borders[1]):
                for y1 in range(y_borders[0], y_borders[1]):
                    true_visible_part.append(visible_part[str(x1) + "_" + str(y1)])
            if pg.mouse.get_pressed()[0]:
                x = int(coords[0] / cell_size)
                y = int(coords[1] / cell_size)
                if x_borders[0] < 0:
                    x -= abs(x_borders[0])
                else:
                    x += x_borders[0]
                if y_borders[0] < 0:
                    y -= abs(y_borders[0])
                else:
                    y += y_borders[0]
                if mode == "!building":
                    added = False
                    if world[x + y * world_len]["tile"] == "iron_ore":
                        for item_id, item in enumerate(inventory):
                            if item["item"] == ("unprocessed", "iron") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 15
                                player_state = "dig_active"
                        if not(added) and len(inventory) < 30:
                            inventory.append({"item": ("unprocessed", "iron"), "amount": 1, "info": ("Iron ore", "Iron, waiting to be", "melted. Can be transf-", "ormed to iron ingot.", "")})
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "copper_ore":
                        for item_id, item in enumerate(inventory):
                            if item["item"] == ("unprocessed", "copper") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 5
                                player_state = "dig_active"
                        if not(added) and len(inventory) < 30:
                            inventory.append({"item": ("unprocessed", "copper"), "amount": 1, "info": ("Copper ore", "Copper, waiting to be", "melted. Can be transf-", "ormed to copper ingot.", "")})
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "tungsten_ore":
                        for item_id, item in enumerate(inventory):
                            if item["item"] == ("unprocessed", "tungsten") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 5
                                player_state = "dig_active"
                        if not(added) and len(inventory) < 30:
                            inventory.append({"item": ("unprocessed", "tungsten"), "amount": 1, "info": ("Raw tungsten", "Raw metal that can glow.", "", "", "")})
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "coal_ore":
                        for item_id, item in enumerate(inventory):
                            if item["item"] == ("unprocessed", "coal") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 5
                                player_state = "dig_active"
                        if not(added) and len(inventory) < 30:
                            inventory.append({"item": ("unprocessed", "coal"), "amount": 1, "info": ("Coal", "Natural material.", "Good for making steel.", "", "")})
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "resin_tree":
                        for item_id, item in enumerate(inventory):
                            if item["item"] == ("unprocessed", "resin") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 5
                                player_state = "dig_active"
                        if not(added) and len(inventory) < 30:
                            inventory.append({"item": ("unprocessed", "resin"), "amount": 1, "info": ("Raw resin", "Natural material.", "Good for isolatin","wires.", "")})
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "uranium_ore":
                        for item_id, item in enumerate(inventory):
                            if item["item"] == ("unprocessed", "uranium") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 5
                                player_state = "dig_active"
                        if not(added) and len(inventory) < 30:
                            inventory.append({"item": ("unprocessed", "uranium"), "amount": 1})
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "leaves":
                        for item_id, item in enumerate(inventory):
                            if item["item"] == ("bio", "leaves") and item["amount"] < 500:
                                inventory[item_id]["amount"] += 1
                                added = True
                                world[x + y * world_len]["tile"] = "grass"
                                temp_new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})                                
                                player_state_timer = 5
                                player_state = "dig_active" 
                        if not(added) and len(inventory) < 30:
                            inventory.append({"item": ("bio", "leaves"), "amount": 1, "info": ("Leaves", "Natural material, but", "has a little radiation in", "it. Can be transformed", "to Biofiber")})
                            world[x + y * world_len]["tile"] = "grass"
                            temp_new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                            player_state_timer = 5
                            player_state = "dig_active" 

        if pos[0] >= world_len:
            pos[0] = world_len - 1
        elif pos[0] < 0:
            pos[0] = 0
        if pos[1] >= world_len:
            pos[1] = world_len - 1
        elif pos[1] < 0:
            pos[1] = 0
        cursor_pos = pg.mouse.get_pos()
        window.blit(pg.transform.scale(ui["cursor"], (cell_size * 2, cell_size * 2)), cursor_pos)
        if menu == "open":
            cursor_pos = pg.mouse.get_pos()
            for y in range(0, 3):
                for x in range(0, 9):
                    if cursor_pos[0] >= 10 * x + (cell_size * 2) * x and cursor_pos[0] <= 10 * x + (cell_size * 2) * (x + 1) and cursor_pos[1] >= 10 * y + (cell_size * 2) * y and cursor_pos[1] <= 10 * y + (cell_size * 2) * (y + 1):
                        try:
                            item = inventory[x + y * 9]
                            window.blit(pg.transform.scale(ui["tooltip"], (cell_size * 4, cell_size * 2)), (cursor_pos[0] + cell_size, cursor_pos[1] + cell_size))
                            text_tooltip1 = dosfont.render(item["info"][0], True, (0, 0, 0))
                            window.blit(text_tooltip1, (cursor_pos[0] + cell_size * 1.2, cursor_pos[1] + cell_size * 1.1))
                            text_tooltip2 = dosfont.render(item["info"][1], True, (0, 0, 0))
                            window.blit(text_tooltip2, (cursor_pos[0] + cell_size * 1.2, cursor_pos[1] + cell_size * 1.4))
                            text_tooltip2 = dosfont.render(item["info"][2], True, (0, 0, 0))
                            window.blit(text_tooltip2, (cursor_pos[0] + cell_size * 1.2, cursor_pos[1] + cell_size * 1.7))
                            text_tooltip2 = dosfont.render(item["info"][3], True, (0, 0, 0))
                            window.blit(text_tooltip2, (cursor_pos[0] + cell_size * 1.2, cursor_pos[1] + cell_size * 2))
                            text_tooltip2 = dosfont.render(item["info"][4], True, (0, 0, 0))
                            window.blit(text_tooltip2, (cursor_pos[0] + cell_size * 1.2, cursor_pos[1] + cell_size * 2.3))
                        except:
                            pass
        pg.display.update()
        clock.tick(45)
        tick += 1
    elif game_mode == "title":
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif evt.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] >= cell_size * 4 and mouse_pos[0] <= cell_size * 8:
                    if mouse_pos[1] >= cell_size * 12 and mouse_pos[1] <= cell_size * 12.5:
                        game_mode = "singleplayer"
                        tick = -1
                    if mouse_pos[1] >= cell_size * 14 and mouse_pos[1] <= cell_size * 14.5:
                        game_mode = "multiplayer_setup"
                        tick = -1
        draw_title(window)
        cursor_pos = pg.mouse.get_pos()
        window.blit(pg.transform.scale(ui["cursor"], (cell_size * 2, cell_size * 2)), cursor_pos)
        pg.display.update()
        clock.tick(45)
        tick += 1
    elif game_mode == "multiplayer_setup":
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif evt.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] >= cell_size * 4 and mouse_pos[0] <= cell_size * 12:
                    if mouse_pos[1] >= cell_size * 12 and mouse_pos[1] <= cell_size * 12.5:
                        selected = 0
                    elif mouse_pos[1] >= cell_size * 14 and mouse_pos[1] <= cell_size * 14.5:
                        selected = 1
                    elif mouse_pos[1] >= cell_size * 10 and mouse_pos[1] <= cell_size * 14.5:
                        selected = 2
            elif evt.type == pg.KEYDOWN:
                if evt.key == pg.K_RETURN:
                    port = int(port) if port.isdigit() and int(port) < 65535 and int(port) > 0 else 8000
                    clientSocket = socket.socket()

                    try:
                        clientSocket.connect((ip, int(port)))
                        clientSocket.settimeout(5)
                        clientSocket.send(nick.encode())
                        received = ""
                        while True:
                            # print("cycling")
                            received += clientSocket.recv(8192).decode("utf-8")
                            if not received:
                                running_thread = False
                            # print(received[-1])
                            if received[-1] == "=":
                                received = received[:-1]
                                break
                        # print("debug")
                        # print(received)
                        received = json.loads(received)
                        starting_blocks = received["starting_blocks"]
                        world = []
                        for i in range(0, world_len * world_len):
                            world.append({"item": None, "building": None, "tile": "stone", "part": 0, "rotation": 0})
                        for block in starting_blocks:
                            world[block["id"]] = block["tile"]
                        for new_block in new_blocks:
                            world[new_block["id"]] = new_block["tile"]
                    except:
                        game_mode = "error"
                        splash = ["Error","Failed to connect, check IP and port"]
                        break
                    chat = []
                    def socketThread():
                        global clientSocket, running_thread, users, pos, world, new_blocks, starting_blocks, temp_new_blocks,chat, recent_messages, send, current_message,game_mode,splash

                        while running_thread:
                            try:
                                if send:
                                    data = {"nickname": nick, "self": [pos,player_state,facing], "new_blocks": new_blocks, "temp_new_blocks":temp_new_blocks,"msg":current_message}
                                    send = False
                                    current_message = ""
                                else:
                                    data = {"nickname": nick, "self": [pos,player_state,facing], "new_blocks": new_blocks, "temp_new_blocks":temp_new_blocks,"msg":""}
                                clientSocket.send((json.dumps(data) + "=").encode())
                                received = ""
                                while True:
                                    received += clientSocket.recv(8192).decode("utf-8")
                                    if not received:
                                        running_thread = False
                                    if received[-1] == "=":
                                        received = received[:-1]
                                        break
                                received = json.loads(received)
                                users = received["users"]
                                received_new_blocks = received["new_blocks"]
                                received_temp_new_blocks = received["temp_new_blocks"]
                                if chat != received["chat"]:
                                    sounds["msg"].play()
                                    recent_messages = [{"user":x["user"],"text":x["text"],"timer":90} for x in received["chat"] if x not in chat]
                                    chat = received["chat"]
                                for block in received_new_blocks:
                                    world[block["id"]] = block["tile"]
                                for block in received_temp_new_blocks:
                                    world[block["id"]] = block["tile"]
                            except:
                                print("a")
                                running_thread = False
                        print("b")
                        game_mode = "error"
                        splash = ["Error","Server closed or connection closed"]

                    socketTh = threading.Thread(target=socketThread)
                    socketTh.start()
                    game_mode = "multiplayer"
                elif evt.key == pg.K_BACKSPACE:
                    if selected == 0:
                        port = port[:-1]
                    elif selected == 1:
                        ip = ip[:-1]
                    elif selected == 2:
                        nick = nick[:-1]
                else:
                    if selected == 0 and len(port) < 5:
                        port += evt.unicode
                    elif selected == 1 and len(ip) < 14:
                        ip += evt.unicode
                    elif selected == 2 and len(nick) < 15:
                        nick += evt.unicode
        draw_multiplayer(window, port, ip, nick)
        cursor_pos = pg.mouse.get_pos()
        window.blit(pg.transform.scale(ui["cursor"], (cell_size * 2, cell_size * 2)), cursor_pos)
        pg.display.update()
        clock.tick(45)
        tick += 1
    elif game_mode == "error":
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                pg.quit()
                sys.exit()        
        draw_splash(window,splash)
        cursor_pos = pg.mouse.get_pos()
        window.blit(pg.transform.scale(ui["cursor"], (cell_size * 2, cell_size * 2)), cursor_pos)
        pg.display.update()
        clock.tick(45)
        tick += 1        
