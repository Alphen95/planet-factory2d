#hint for Hardcore652 : go fix multiplayer

import pygame as pg
import sys
import random
import os
import datetime
import socket
import threading
import json
from pprint import pprint

VERSION = 0.6
RUNNING_TEXT = "PRE-RELEASE"
effects = [(9,9)]
os.makedirs("logs", exist_ok=True)
log_file = open(os.path.join("logs", "log-{}.txt".format(str(datetime.datetime.now()).replace(":", "_")[:-7])), "w+")
log_file.write("[INFO] program started, time: {}\n".format(str(datetime.datetime.now())[:-7]))
SPECIAL_YELLOW = (220, 184, 10)
ppc_power = 253
ppc_batt = 1000
game_mode = "title"
selected = 0
temp_new_blocks = []
new_blocks = []
users = []
action = ""
ip = "localhost"
port = "8000"
nick = "Player{}".format(random.randint(0,9999))
world_applied = False
category = 0
coins = 500
chat = []
recent_messages = []
current_message = ""
send = False
chat_open = False
player_type = "alphen"
inventory_tile = ""
cursor_tile_id = -1
dialogue = [[],0]
power_capacity = 0
power_capacity_current = 0
power_max = 0
power_usage = 0
power_down = False
release_notes = [
    "PreRelease 0.6",
    "Automation Update",
    "Now smelting can be automated.",
    "Added conveyors, automatic",
    "smelters and storage",
    "containers.",
    
]

processors = ["smelter"]
conveyor_acceptable = ["conveyor_belt","smelter","storage_container"]
conveyor_acceptable_processors = {"smelter":2}
"""
("",""):0, 
    ("",""):0, 
    ("",""):0, 
    ("",""):0, 
    ("",""):0, 
    ("",""):0, 
    ("",""):0, 
"""
item_costs = {
    ("basic","drill"):30, 
    ("basic","plate"):3, 
    ("basic","screws"):12, 
    ("basic","wire"):7, 
    ("basic","cable"):10, 
    ("basic","rod"):5, 
    ("uranium","bio"):35
    
}
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
        "name":"Iron plate x3",
        "required_text":"Iron ingot",
        "output_text":"Iron plate x 3",
        "required":[[("ingot","iron"),1]],
        "output":{"item": ("basic", "plate"), "amount": 3}
    },
    {
        "name":"Iron rod x2",
        "required_text":"Iron ingot",
        "output_text":"Iron rod x2",
        "required":[[("ingot","iron"),1]],
        "output":{"item": ("basic", "rod"), "amount": 2}
    }, 
    {
        "name":"Screws x10",
        "required_text":"Iron ingot",
        "output_text":"Screws x10",
        "required":[[("ingot","iron"),1]],
        "output":{"item": ("basic", "screws"), "amount": 10}
    }, 
    {
        "name":"Copper wire x5",
        "required_text":"Copper ingot",
        "output_text":"Copper wire x5",
        "required":[[("ingot","copper"),1]],
        "output":{"item": ("basic", "wire"), "amount": 5}
    }, 
    {
        "name":"Cable",
        "required_text":("Copper wire","Rubber sheet"),
        "output_text":"Copper wire x5",
        "required":[[("basic","wire"),1],[("ingot","resin"),1]],
        "output":{"item": ("basic", "cable"), "amount": 1}
    },     
    {
        "name":"Portable drill",
        "required_text":("Iron plate x2","Iron rod x3"),
        "output_text":"Portable drill",
        "required":[[("basic","plate"),2],[("basic","rod"),3]],
        "output":{"item": ("basic", "drill"), "amount": 1}
    },
    {
        "name":"Biofiber x2",
        "required_text":"Leaves x3",
        "output_text":"",
        "required":[[("bio","leaves"),3]],
        "output":{"item": ("bio", "fiber"), "amount": 2}
    }, 
    {
        "name":"BioUranium fuel rod x6",
        "required_text":("Biofiber x3","Iron plate x5"),
        "output_text":"",
        "required":[[("bio","fiber"),3],[("basic","plate"),5]],
        "output":{"item": ("uranium", "bio"), "amount": 6}
    }, 
    {
        "name":"Hi-tech glasses",
        "required_text":("Iron plate x3","Cable x2"),
        "output_text":"",
        "required":[[("basic","cable"),2],[("basic","plate"),3]],
        "output":{"item": ("wearables", "varu_glasses"), "amount": 1}
    },     
]

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
        {
            "name":"Resin sheet",
            "required_text":"Sticky resin",
            "required":[[("unprocessed","resin"),1]],
            "output":{"item": ("ingot", "resin"), "amount": 1},
            "time":2
        },         
    ]
}

npc = {
    "weles":{
        "overworld":pg.image.load(os.path.join("res", "npc","weles_delivery", "overworld.png")),
        "dialog":pg.image.load(os.path.join("res", "npc","weles_delivery", "dialog.png"))
    }
}

ui = {
    "tooltip": pg.image.load(os.path.join("res", "ui", "tooltip_box.png")),
    "ppc": pg.image.load(os.path.join("res", "ui", "pocket_comp.png")),
    "inv_cell": pg.image.load(os.path.join("res", "ui", "inv_cell.png")),
    "inv_cell_armor": pg.image.load(os.path.join("res", "ui", "inv_cell_armor.png")),
    "cursor": pg.image.load(os.path.join("res", "ui", "cursor.png")),
    "title": pg.image.load(os.path.join("res", "ui", "title.png")),
    "titlename": pg.image.load(os.path.join("res", "ui", "titlename.png")),
    "fuse_normal":pg.image.load(os.path.join("res", "ui", "fuse_normal.png")),
    "fuse_broken":pg.image.load(os.path.join("res", "ui", "fuse_broken.png")),
}

filters = {
    "varu_glasses":[
        pg.image.load(os.path.join("res", "filters","varu_glasses.png")),
        pg.image.load(os.path.join("res", "filters","varu_glasses_2.png"))
    ]
}

player = {
    "alphen":{
        "default": [
            pg.image.load(os.path.join("res", "player","alphen", "state0.png")),
            pg.image.load(os.path.join("res", "player","alphen", "state1.png"))
        ],
        "building": [
            pg.image.load(os.path.join("res", "player","alphen", "state0_build.png")),
            pg.image.load(os.path.join("res", "player","alphen", "state1_build.png"))
        ],        
        "dig": [
            pg.image.load(os.path.join("res", "player","alphen", "state0_dig0.png")),
            pg.image.load(os.path.join("res", "player","alphen", "state1_dig0.png"))
        ],
        "dig_active": [
            pg.image.load(os.path.join("res", "player","alphen", "state0_dig1.png")),
            pg.image.load(os.path.join("res", "player","alphen", "state1_dig1.png"))
        ]       ,
        "dialog":pg.image.load(os.path.join("res", "player","alphen", "dialog_avatar.png")) 
    },
    "fury":{
        "default": [
            pg.image.load(os.path.join("res", "player","fury", "state0.png")),
            pg.image.load(os.path.join("res", "player","fury", "state1.png"))
        ],
        "building": [
            pg.image.load(os.path.join("res", "player","fury", "state0_build.png")),
            pg.image.load(os.path.join("res", "player","fury", "state1_build.png"))
        ],        
        "dig": [
            pg.image.load(os.path.join("res", "player","fury", "state0_dig0.png")),
            pg.image.load(os.path.join("res", "player","fury", "state1_dig0.png"))
        ],
        "dig_active": [
            pg.image.load(os.path.join("res", "player","fury", "state0_dig1.png")),
            pg.image.load(os.path.join("res", "player","fury", "state1_dig1.png"))
        ],
        "dialog":pg.image.load(os.path.join("res", "player","fury", "dialog_avatar.png"))
    },
    "a":{
        "default": [
            pg.image.load(os.path.join("res", "player","alphen", "state0.png")),
            pg.image.load(os.path.join("res", "player","alphen", "state1.png"))
        ],
        "building": [
            pg.image.load(os.path.join("res", "player","alphen", "state0_build.png")),
            pg.image.load(os.path.join("res", "player","alphen", "state1_build.png"))
        ],        
        "dig": [
            pg.image.load(os.path.join("res", "player","alphen", "state0_dig0.png")),
            pg.image.load(os.path.join("res", "player","alphen", "state1_dig0.png"))
        ],
        "dig_active": [
            pg.image.load(os.path.join("res", "player","alphen", "state0_dig1.png")),
            pg.image.load(os.path.join("res", "player","alphen", "state1_dig1.png"))
        ],
        "dialog":pg.image.load(os.path.join("res", "player","alphen", "dialog_avatar.png"))        
    },
    "f":{
        "default": [
            pg.image.load(os.path.join("res", "player","fury", "state0.png")),
            pg.image.load(os.path.join("res", "player","fury", "state1.png"))
        ],
        "building": [
            pg.image.load(os.path.join("res", "player","fury", "state0_build.png")),
            pg.image.load(os.path.join("res", "player","fury", "state1_build.png"))
        ],        
        "dig": [
            pg.image.load(os.path.join("res", "player","fury", "state0_dig0.png")),
            pg.image.load(os.path.join("res", "player","fury", "state1_dig0.png"))
        ],
        "dig_active": [
            pg.image.load(os.path.join("res", "player","fury", "state0_dig1.png")),
            pg.image.load(os.path.join("res", "player","fury", "state1_dig1.png"))
        ],
        "dialog":pg.image.load(os.path.join("res", "player","fury", "dialog_avatar.png"))        
    }      
}

deal_translations = {
    ("basic","plate"):"Iron plate",
    ("basic","rod"):"Iron rod",
    ("basic","wire"):"Copper wire",
    ("basic","drill"):"Basic drill",
    ("basic","screws"):"Screws",
    ("basic","cable"):"Cable",
    ("uranium","bio"):"BioUranium fuel rod",
                
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
        "fiber": pg.image.load(os.path.join("res", "resources", "bio", "biofiber.png")),
        "leaves": pg.image.load(os.path.join("res", "resources", "bio", "leaves.png"))
    },
    "basic":{
        "plate":pg.image.load(os.path.join("res", "resources", "basic", "iron_plate.png")),
        "rod":pg.image.load(os.path.join("res", "resources", "basic", "iron_rod.png")),
        "screws":pg.image.load(os.path.join("res", "resources", "basic", "screws.png")),
        "wire":pg.image.load(os.path.join("res", "resources", "basic", "wire_copper.png")),
        "cable":pg.image.load(os.path.join("res", "resources", "basic", "cable.png")),
        "drill":pg.image.load(os.path.join("res", "resources", "basic", "drill.png")),
        "reinforced_plate":pg.image.load(os.path.join("res","resources","basic","reinforced_plate.png")),
        #"":pg.image.load(os.path.join("res","resources",".png")),
    },
    "uranium":{
        "bio":pg.image.load(os.path.join("res","resources","uranium","bio_fuel_rod.png"))
    },
    "wearables":{
        "varu_glasses":pg.image.load(os.path.join("res","wearables","varu_glasses.png"))
    }
}

buildings = {
    "drill": [
        pg.image.load(os.path.join("res", "buildings", "drill_part1.png")),
        pg.image.load(os.path.join("res", "buildings", "drill_part2.png"))
    ],
    "conveyor": {
        0:[
            pg.image.load(os.path.join("res", "buildings", "conveyor_belt0.png")),
            pg.image.load(os.path.join("res", "buildings", "conveyor_belt1.png")),
            pg.image.load(os.path.join("res", "buildings", "conveyor_belt2.png")),
            pg.image.load(os.path.join("res", "buildings", "conveyor_belt3.png"))
        ],
        1:[
            pg.image.load(os.path.join("res", "buildings", "conveyor_belt0_turn.png")),
            pg.image.load(os.path.join("res", "buildings", "conveyor_belt1_turn.png")),
            pg.image.load(os.path.join("res", "buildings", "conveyor_belt2_turn.png")),
            pg.image.load(os.path.join("res", "buildings", "conveyor_belt3_turn.png")) 
        ],
        2:[
            pg.transform.flip(pg.image.load(os.path.join("res", "buildings", "conveyor_belt0_turn.png")),False,True),
            pg.transform.flip(pg.image.load(os.path.join("res", "buildings", "conveyor_belt1_turn.png")),False,True),
            pg.transform.flip(pg.image.load(os.path.join("res", "buildings", "conveyor_belt2_turn.png")),False,True),
            pg.transform.flip(pg.image.load(os.path.join("res", "buildings", "conveyor_belt3_turn.png")),False,True) 
        ],        
    },
    "biomass_burner": [
        pg.image.load(os.path.join("res", "buildings", "biomass_burner.png"))
    ],
    "smelter":[
        pg.image.load(os.path.join("res","buildings","smelter_part1.png")),
        pg.image.load(os.path.join("res","buildings","smelter_part2.png"))
    ],
    "storage_container":[
        pg.image.load(os.path.join("res","buildings","storage_container.png")),
        pg.transform.flip(pg.image.load(os.path.join("res","buildings","storage_container.png")),True,False)
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
for i in range(0,27): inventory.append({})
current_item = ["", 0]
mode = "!building"
power_capacity = 0
facing = 0
action = ""
player_state = "default"
player_state_timer = 0
running_thread = True
starting_blocks = []

cell_size = 40
screen_size = (cell_size * 20, cell_size * 20)
world_len = 200

window = pg.display.set_mode(screen_size)
clock = pg.time.Clock()
clockA = pg.time.Clock()
pg.init()
pg.mouse.set_visible(False)
font = pg.font.SysFont("Verdana", 12)
dosfont = pg.font.Font(os.path.join("res", "dosfont.ttf"), 12)
dosfontbig = pg.font.Font(os.path.join("res", "dosfont.ttf"), 24)
dosfont125 = pg.font.Font(os.path.join("res", "dosfont.ttf"), 18)
pos = [int(world_len / 2), int(world_len / 2)]
menubar = []
pg.display.set_icon(pg.image.load(os.path.join("res","icon.png")))

sounds = {
    "msg":pg.mixer.Sound(os.path.join("res","snd","msg.wav"))
}


# world define
world = []
for i in range(0, world_len * world_len):
    world.append({"item": None, "building": None, "tile": "stone", "part": 0, "rotation": 0})

for i in range(0, random.randint(10, 40)):
    size = random.randint(1, 10)
    x = random.randint(0, world_len - (size + 1))
    y = random.randint(0, world_len - (size + 1))
    for xpos in range(0, size):
        for ypos in range(0, size):
            grass_chance = ["grass", "grass", "leaves"]
            world[x + xpos + ((y + ypos) * world_len)]["tile"] = random.choice(grass_chance)


for i in range(0, 5):
    x = random.randint(0, world_len - 1)
    y = random.randint(0, world_len - 1)
    if i == 0:
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
    elif i == 5 or i == 1:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "uranium_ore", "part": 0, "rotation": 0}
        log_file.write("[DEBUG] placed uranium ore in x:{0} y:{1}, time:{2}\n".format(x, y, str(datetime.datetime.now())[:-7]))    
for i1 in range(0, int((world_len - 20) / 2)):
    x = random.randint(0, world_len - 1)
    y = random.randint(0, world_len - 1)
    i = random.randint(0, 5)
    if i == 0:
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
    elif i == 5 or i == 1:
        world[x + (y * world_len)] = {"item": None, "building": None, "tile": "uranium_ore", "part": 0, "rotation": 0}
        log_file.write("[DEBUG] placed uranium ore in x:{0} y:{1}, time:{2}\n".format(x, y, str(datetime.datetime.now())[:-7])) 
x = random.randint(0, world_len - 3)
y = random.randint(0, world_len - 3)
for i in range(0, 3):
    for i1 in range(0, 3):
        world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "grass", "part": 0, "rotation": 0}
        if i == 1 and i1 == 1:
            world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "resin_ore", "part": 0, "rotation": 0}
for j in range(0,10):
    x = random.randint(0, world_len - 3)
    y = random.randint(0, world_len - 3)    
    for i in range(0, 3):
        for i1 in range(0, 3):
            world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "grass", "part": 0, "rotation": 0}
            if i == 1 and i1 == 1:
                world[(x + i) + ((y + i1) * world_len)] = {"item": None, "building": None, "tile": "resin_ore", "part": 0, "rotation": 0}
                
def create_deal():
    possible_items = list(item_costs.items())  
    deal = random.choice(possible_items)
    item_amount = random.randint(1,30)
    cost_modifier = random.randint(8,12)/10
    return {"item":deal[0],"amount":item_amount,"cost":int(deal[1]*item_amount*cost_modifier)}
    

def draw_world(world, winobj, tick, pos, tooltip_props, menu_props, edit_mode, player_props,action,effects):
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
            elif block == "resin_ore":
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
                    if inventory[-1] != {} and inventory[-1]["item"] == ("wearables","varu_glasses"):
                        try:
                            winobj.blit(pg.transform.scale(pg.transform.rotate(resources[tile["inventory"]["item"][0]][tile["inventory"]["item"][1]], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        except:pass                    
                elif block_part == 2:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][1], 0), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block_building == "smelter":
                if block_part == 1:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["smelter"][0], block_rotation+270), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    if inventory[-1] != {} and inventory[-1]["item"] == ("wearables","varu_glasses"):
                        if tile["recepie"] != -1:
                            item = processing_recepies[tile["building"]][tile["recepie"]]["output"]["item"]
                            winobj.blit(pg.transform.scale(pg.transform.rotate(resources[item[0]][item[1]], 0), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                elif block_part == 2:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["smelter"][1], block_rotation+270), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block_building == "storage_container":
                if block_part == 1:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["storage_container"][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                elif block_part == 2:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["storage_container"][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
            elif block_building == "conveyor_belt":
                combo = 4
                conv_side = 0
                if block_rotation == 0:
                    if world[x+(y-1)*world_len]["building"] in conveyor_acceptable and world[x+(y-1)*world_len]["rotation"] == 270 and world[x+(y+1)*world_len]["building"] in conveyor_acceptable and world[x+(y+1)*world_len]["rotation"] == 90 and world[(x-1)+y*world_len]["building"] in conveyor_acceptable and world[(x-1)+y*world_len]["rotation"] == 0: combo = 0
                    elif world[x+(y-1)*world_len]["building"] in conveyor_acceptable and world[x+(y-1)*world_len]["rotation"] == 270 and world[x+(y+1)*world_len]["building"] in conveyor_acceptable and world[x+(y+1)*world_len]["rotation"] == 90 : combo = 1
                    elif world[x+(y-1)*world_len]["building"] in conveyor_acceptable and world[x+(y-1)*world_len]["rotation"] == 270 and world[(x-1)+y*world_len]["building"] in conveyor_acceptable and world[(x-1)+y*world_len]["rotation"] == 0: combo = 2
                    elif world[x+(y+1)*world_len]["building"] in conveyor_acceptable and world[x+(y+1)*world_len]["rotation"] == 90 and world[(x-1)+y*world_len]["building"] in conveyor_acceptable and world[(x-1)+y*world_len]["rotation"] == 0: combo = 3
                    elif world[x+(y-1)*world_len]["building"] in conveyor_acceptable and world[x+(y-1)*world_len]["rotation"] == 270: conv_side = 1
                    elif world[x+(y+1)*world_len]["building"] in conveyor_acceptable and world[x+(y+1)*world_len]["rotation"] == 90: conv_side = 2
                elif block_rotation == 180:
                    if world[x+(y+1)*world_len]["building"] in conveyor_acceptable and world[x+(y+1)*world_len]["rotation"] == 90 and world[x+(y-1)*world_len]["building"] in conveyor_acceptable and world[x+(y-1)*world_len]["rotation"] == 270 and world[(x+1)+y*world_len]["building"] in conveyor_acceptable and world[(x+1)+y*world_len]["rotation"] == 180: combo=0
                    elif world[x+(y+1)*world_len]["building"] in conveyor_acceptable and world[x+(y+1)*world_len]["rotation"] == 90 and world[x+(y-1)*world_len]["building"] in conveyor_acceptable and world[x+(y-1)*world_len]["rotation"] == 270: combo=1
                    elif world[x+(y+1)*world_len]["building"] in conveyor_acceptable and world[x+(y+1)*world_len]["rotation"] == 90 and world[(x+1)+y*world_len]["building"] in conveyor_acceptable and world[(x+1)+y*world_len]["rotation"] == 180: combo=2
                    elif world[x+(y-1)*world_len]["building"] in conveyor_acceptable and world[x+(y-1)*world_len]["rotation"] == 270 and world[(x+1)+y*world_len]["building"] in conveyor_acceptable and world[(x+1)+y*world_len]["rotation"] == 180: combo=3
                    elif world[x+(y+1)*world_len]["building"] in conveyor_acceptable and world[x+(y+1)*world_len]["rotation"] == 90: conv_side = 1
                    elif world[x+(y-1)*world_len]["building"] in conveyor_acceptable and world[x+(y-1)*world_len]["rotation"] == 270: conv_side = 2
                elif block_rotation == 90:
                    if world[(x-1)+y*world_len]["building"] in conveyor_acceptable and world[(x-1)+y*world_len]["rotation"] == 0 and world[(x+1)+y*world_len]["building"] in conveyor_acceptable and world[(x+1)+y*world_len]["rotation"] == 180 and world[x+(y+1)*world_len]["building"] in conveyor_acceptable and world[x+(y+1)*world_len]["rotation"] == 90: combo=0
                    elif world[(x-1)+y*world_len]["building"] in conveyor_acceptable and world[(x-1)+y*world_len]["rotation"] == 0 and world[(x+1)+y*world_len]["building"] in conveyor_acceptable and world[(x+1)+y*world_len]["rotation"] == 180: combo=1
                    elif world[(x-1)+y*world_len]["building"] in conveyor_acceptable and world[(x-1)+y*world_len]["rotation"] == 0 and world[x+(y+1)*world_len]["building"] in conveyor_acceptable and world[x+(y+1)*world_len]["rotation"] == 90: combo=2
                    elif world[(x+1)+y*world_len]["building"] in conveyor_acceptable and world[(x+1)+y*world_len]["rotation"] == 180 and world[x+(y+1)*world_len]["building"] in conveyor_acceptable and world[x+(y+1)*world_len]["rotation"] == 90: combo=3
                    elif world[(x-1)+y*world_len]["building"] in conveyor_acceptable and world[(x-1)+y*world_len]["rotation"] == 0: conv_side = 1
                    elif world[(x+1)+y*world_len]["building"] in conveyor_acceptable and world[(x+1)+y*world_len]["rotation"] == 180: conv_side = 2
                elif block_rotation == 270:
                    if world[(x+1)+y*world_len]["building"] in conveyor_acceptable and world[(x+1)+y*world_len]["rotation"] == 180 and world[(x-1)+y*world_len]["building"] in conveyor_acceptable and world[(x-1)+y*world_len]["rotation"] == 0 and world[x+(y-1)*world_len]["building"] in conveyor_acceptable and world[x+(y-1)*world_len]["rotation"] == 270: combo=0
                    elif world[(x+1)+y*world_len]["building"] in conveyor_acceptable and world[(x+1)+y*world_len]["rotation"] == 180 and world[(x-1)+y*world_len]["building"] in conveyor_acceptable and world[(x-1)+y*world_len]["rotation"] == 0: combo=1
                    elif world[(x+1)+y*world_len]["building"] in conveyor_acceptable and world[(x+1)+y*world_len]["rotation"] == 180 and world[x+(y-1)*world_len]["building"] in conveyor_acceptable and world[x+(y-1)*world_len]["rotation"] == 270: combo=2
                    elif world[(x-1)+y*world_len]["building"] in conveyor_acceptable and world[(x-1)+y*world_len]["rotation"] == 0 and world[x+(y-1)*world_len]["building"] in conveyor_acceptable and world[x+(y-1)*world_len]["rotation"] == 270: combo=3
                    elif world[(x+1)+y*world_len]["building"] in conveyor_acceptable and world[(x+1)+y*world_len]["rotation"] == 180: conv_side = 1
                    elif world[(x-1)+y*world_len]["building"] in conveyor_acceptable and world[(x-1)+y*world_len]["rotation"] == 0: conv_side = 2
                if combo == 0:
                    if tick <= 14:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 29:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 44:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][2], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][2], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][2], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 59:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][3], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][3], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][3], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size)) 
                elif combo == 4:                
                    if tick <= 14:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][conv_side][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 29:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][conv_side][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 44:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][conv_side][2], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 59:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][conv_side][3], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                elif combo == 1:
                    if tick <= 14:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 29:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 44:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][2], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][2], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 59:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][3], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][3], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))   
                elif combo == 2:
                    if tick <= 14:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 29:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 44:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][2], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][2], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 59:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1][3], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][3], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))   
                elif combo == 3:
                    if tick <= 14:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 29:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][1], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 44:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][2], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][2], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    elif tick <= 59:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2][3], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                        winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0][3], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size)) 
                if tile["inventory"] != {}: 
                    item = tile["inventory"]["item"]
                    winobj.blit(pg.transform.scale(resources[item[0]][item[1]], (int(cell_size*0.5), int(cell_size*0.5))), (x1 * cell_size+cell_size*0.25, y1 * cell_size+cell_size*0.25))     
            elif block_building == "biomass_burner":
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["biomass_burner"][0], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                if inventory[-1] != {} and inventory[-1]["item"] == ("wearables","varu_glasses"):
                    try:
                        winobj.blit(pg.transform.scale(pg.transform.rotate(resources[tile["inventory"]["item"][0]][tile["inventory"]["item"][1]], block_rotation), (cell_size, cell_size)), (x1 * cell_size, y1 * cell_size))
                    except:pass
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
        winobj.blit(pg.transform.scale(pg.transform.flip(player[player_type][player_props[1]][1], player_props[0], False), (cell_size * 2, cell_size * 2)), ((x1 - 1) * cell_size, (y1 - 1) * cell_size))
    elif tick <= 21:
        winobj.blit(pg.transform.scale(pg.transform.flip(player[player_type][player_props[1]][0], player_props[0], False), (cell_size * 2, cell_size * 2)), ((x1 - 1) * cell_size, (y1 - 1) * cell_size))
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
            winobj.blit(pg.transform.scale(pg.transform.flip(player[user[4]][user[2]][1], user[3], False), (cell_size * 2, cell_size * 2)), ((x1 - 1) * cell_size, (y1 - 1) * cell_size))
        elif tick <= 21:
            winobj.blit(pg.transform.scale(pg.transform.flip(player[user[4]][user[2]][0], user[3], False), (cell_size * 2, cell_size * 2)), ((x1 - 1) * cell_size, (y1 - 1) * cell_size))
        text_name = dosfont.render(user[1], True, (0, 0, 0))
        winobj.blit(text_name, ((x1 - 1) * cell_size, (y1 - 1) * cell_size)) 
    if edit_mode:
        winobj.blit(pg.transform.scale(pg.transform.rotate(ui["ppc"], 0), (cell_size * 6, cell_size * 12)), (5, screen_size[1] + 10 - cell_size * 8))
        if current_item!=[] and current_item[0] != "":
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
                text_line3 = dosfont.render("2>ELECTRICITY", True, (0, 0, 0))
                text_line4 = dosfont.render("3>LOGISITC", True, (0, 0, 0))
                text_line5 = dosfont.render("4>PROCESSING", True, (0, 0, 0))
                text_line6 = dosfont.render("5>DISASSEMBLE", True, (0, 0, 0))
                text_line7 = dosfont.render("6>WELES_DELIVERY", True, (0, 0, 0))
                winobj.blit(text_line1, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20 * 5) - cell_size * 4) * 1.25))))
                winobj.blit(text_line2, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20) - cell_size * 4) * 1.25))))
                winobj.blit(text_line3, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 2) - cell_size * 4) * 1.25)))
                winobj.blit(text_line4, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 3) - cell_size * 4) * 1.25)))
                winobj.blit(text_line5, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 4) - cell_size * 4) * 1.25))))
                winobj.blit(text_line6, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 5) - cell_size * 4) * 1.25))))   
                winobj.blit(text_line7, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 6) - cell_size * 4) * 1.25))))   
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
            elif category == 2:
                text_line1 = dosfont.render("CATEGORY: ELECTRC.", True, (0, 0, 0))
                text_line2 = dosfont.render("1>BIO_BURNER", True, (0, 0, 0))
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
            elif category == 3:
                text_line1 = dosfont.render("CATEGORY: LOGIST.", True, (0, 0, 0))
                text_line2 = dosfont.render("1>CONV_BELT_MK1", True, (0, 0, 0))
                text_line3 = dosfont.render("2>", True, (0, 0, 0))
                text_line4 = dosfont.render("3>", True, (0, 0, 0))
                text_line5 = dosfont.render("4>STORAGE_CONT", True, (0, 0, 0))
                text_line6 = dosfont.render("5>BACK", True, (0, 0, 0))
                winobj.blit(text_line1, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20 * 5) - cell_size * 4) * 1.25))))
                winobj.blit(text_line2, (int(cell_size * 1.5), (screen_size[1] + 15 + int((12 * screen_size[1] / (40 * 20) - cell_size * 4) * 1.25))))
                winobj.blit(text_line3, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 2) - cell_size * 4) * 1.25)))
                winobj.blit(text_line4, (int(cell_size * 1.5), (screen_size[1] + 15 + (int((12 * screen_size[1] / (40 * 20)) * 3) - cell_size * 4) * 1.25)))
                winobj.blit(text_line5, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 4) - cell_size * 4) * 1.25))))
                winobj.blit(text_line6, (int(cell_size * 1.5), (screen_size[1] + 15 + (int(((12 * screen_size[1] / (40 * 20)) * 5) - cell_size * 4) * 1.25))))     
            elif category == 4:
                text_line1 = dosfont.render("CATEGORY: PROCESSING", True, (0, 0, 0))
                text_line2 = dosfont.render("1>SMELTER", True, (0, 0, 0))
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
    if menu_props[1] != "hidden" and inventory_tile == "" and action == "":
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
        if menu_props[1] != "hidden" and inventory_tile == "":
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
                if x+y*9 != 26:
                    try:
                        winobj.blit(pg.transform.scale(ui["inv_cell"], (cell_size * 2, cell_size * 2)), (xpos + 5 + 10 * x + (cell_size * 2) * x, ypos + 5 + 10 * y + (cell_size * 2) * y))
                        item = inventory[x + y * 9]["item"]
                        item_amount = inventory[x + y * 9]["amount"]
                        winobj.blit(pg.transform.scale(resources[item[0]][item[1]], (cell_size * 2, cell_size * 2)), (xpos + 10 * x + (cell_size * 2) * x, ypos + 10 * y + (cell_size * 2) * y))
                        text_amount = dosfont.render(str(item_amount), True, (255, 255, 255))
                        winobj.blit(text_amount, (xpos + 10 * x + (cell_size * 2) * x + (cell_size * 2) - 11, ypos + 10 * y + (cell_size * 2) * y + (cell_size * 2) - 11))
                    except:
                        pass
                else:
                    try:
                        winobj.blit(pg.transform.scale(ui["inv_cell_armor"], (cell_size * 2, cell_size * 2)), (xpos + 5 + 10 * x + (cell_size * 2) * x, ypos + 5 + 10 * y + (cell_size * 2) * y))
                        item = inventory[x+y*9]["item"]
                        winobj.blit(pg.transform.scale(resources[item[0]][item[1]], (cell_size * 2, cell_size * 2)), (xpos + 10 * x + (cell_size * 2) * x, ypos + 10 * y + (cell_size * 2) * y))
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
            if isinstance(recepie["required_text"],str):
                text_required = dosfont.render("Need:"+recepie["required_text"], True, (0,0,0))
                winobj.blit(text_required, (xpos+10+y*160,ypos+325+x*60))
            else:
                i = -1
                for text in recepie["required_text"]:
                    text_required = dosfont.render(text, True, (0,0,0))
                    winobj.blit(text_required, (xpos+10+y*160,ypos+325+x*60+i*9+2))              
                    i+=1
            x+=1
    if menu_props[1] != "hidden" and action != "":
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
        if menu_props[1] != "hidden" and inventory_tile == "":
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
        if action == "sell":
            text_line1 = dosfontbig.render("Left click: sell 1", True, (255, 255, 255))
            text_line3 = dosfontbig.render("Coins: {}".format(coins), True, (255, 255, 255))
            text_line2 = dosfontbig.render("Enter: exit", True, (255, 255, 255))
            winobj.blit(text_line1, (cell_size*0.25, cell_size*8 ))  
            winobj.blit(text_line2, (cell_size*0.25, cell_size*8.5 ))
            winobj.blit(text_line3, (cell_size*0.25, cell_size*9 ))
            
    if menu_props[1] != "hidden" and inventory_tile != "" and action == "":
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
        if menu_props[1] != "hidden" and inventory_tile != "":
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
        if world[inventory_tile]["building"] == "biomass_burner":
            text_line1 = dosfontbig.render("Max power production:{}".format(power_max), True, (0, 0, 0))
            text_line2 = dosfontbig.render("Power production:{}".format(power_capacity_current), True, (0, 0, 0))
            text_line3 = dosfontbig.render("Power consumption:{}".format(power_usage), True, (0, 0, 0))
            text_line4 = dosfontbig.render("Power left:{}".format(power_capacity), True, (0, 0, 0))
            winobj.blit(text_line1, (cell_size*1,cell_size*7))
            winobj.blit(text_line2, (cell_size*1,cell_size*7.5))
            winobj.blit(text_line3, (cell_size*1,cell_size*8))
            winobj.blit(text_line4, (cell_size*1,cell_size*8.5))  
            if power_down:
                winobj.blit(pg.transform.scale(ui["fuse_broken"], (cell_size * 2, cell_size*4)), (cell_size*1,cell_size*9))
            else:
                winobj.blit(pg.transform.scale(ui["fuse_normal"], (cell_size * 2, cell_size*4)), (cell_size*1,cell_size*9))
        if type(world[inventory_tile]["inventory"]) != list:
            x = 5
            y = 4
            try:
                winobj.blit(pg.transform.scale(ui["inv_cell"], (cell_size * 2, cell_size * 2)), (xpos + 5 + 10 * x + (cell_size * 2) * x, ypos + 5 + 10 * y + (cell_size * 2) * y))
                item = world[inventory_tile]["inventory"]["item"]
                item_amount = world[inventory_tile]["inventory"]["amount"]
                winobj.blit(pg.transform.scale(resources[item[0]][item[1]], (cell_size * 2, cell_size * 2)), (xpos + 10 * x + (cell_size * 2) * x, ypos + 10 * y + (cell_size * 2) * y))
                text_amount = dosfont.render(str(item_amount), True, (255, 255, 255))
                winobj.blit(text_amount, (xpos + 10 * x + (cell_size * 2) * x + (cell_size * 2) - 11, ypos + 10 * y + (cell_size * 2) * y + (cell_size * 2) - 11))
            except:pass
        elif "recepie" in world[inventory_tile] and world[inventory_tile]["recepie"] != -1 or not "recepie" in world[inventory_tile]:
            y = 4
            x = 0
            for x_1 in range(len(world[inventory_tile]["inventory"])):
                if x == 10:
                    y+= 1
                    x = 0
                draw_x =x
                if x+1 == len(world[inventory_tile]["inventory"]) and len(world[inventory_tile]["inventory"]) <= 5:
                    percent_done = world[inventory_tile]["tick_timer"]/((processing_recepies[world[inventory_tile]["building"]][world[inventory_tile]["recepie"]]["time"]+1)*60)
                    pg.draw.rect(winobj,(150,150,150),(xpos + 10 * draw_x + (cell_size * 2) * draw_x,ypos + 5 + 10 * y + (cell_size * 2) * y+cell_size*0.65,cell_size*2,cell_size*0.9))
                    pg.draw.rect(winobj,SPECIAL_YELLOW,(xpos + 10 * draw_x + (cell_size * 2) * draw_x,ypos + 5 + 10 * y + (cell_size * 2) *y+ cell_size*0.65,cell_size*2-int(percent_done*(cell_size*2)),cell_size*0.9))
                    draw_x+= 1                 
                winobj.blit(pg.transform.scale(ui["inv_cell"], (cell_size * 2, cell_size * 2)), (xpos + 5 + 10 * draw_x + (cell_size * 2) * draw_x, ypos + 5 + 10 * y + (cell_size * 2) * y))
                if world[inventory_tile]["inventory"][x] != {}:
                    item = world[inventory_tile]["inventory"][x]["item"]
                    item_amount = world[inventory_tile]["inventory"][x]["amount"]
                    winobj.blit(pg.transform.scale(resources[item[0]][item[1]], (cell_size * 2, cell_size * 2)), (xpos + 10 * draw_x + (cell_size * 2) * draw_x, ypos + 10 * y + (cell_size * 2) * y))
                    text_amount = dosfont.render(str(item_amount), True, (255, 255, 255))
                    winobj.blit(text_amount, (xpos + 10 * draw_x + (cell_size * 2) * draw_x + (cell_size * 2) - 11, ypos + 10 * y + (cell_size * 2) * y + (cell_size * 2) - 11))
                x += 1
            x = 0
            y = 0
            if "recepie" in world[inventory_tile]:
                recepie = processing_recepies[world[inventory_tile]["building"]][world[inventory_tile]["recepie"]]
                pg.draw.rect(winobj,(0,0,0),(xpos+10+y*153,ypos+310+x*60,150,50))
                pg.draw.rect(winobj,(200,200,200),(xpos+10+y*157,ypos+310+x*60,148,48))
                text_name = dosfont.render(recepie["name"], True, (0,0,0))
                winobj.blit(text_name, (xpos+10+y*160,ypos+310+x*60))
                if isinstance(recepie["required_text"],str):
                    text_required = dosfont.render("Need:"+recepie["required_text"], True, (0,0,0))
                    winobj.blit(text_required, (xpos+10+y*160,ypos+325+x*60))
                else:
                    i = -1
                    for text in recepie["required_text"]:
                        text_required = dosfont.render(text, True, (0,0,0))
                        winobj.blit(text_required, (xpos+10+y*160,ypos+325+x*60+i*9+2))              
                        i+=1            
        elif world[inventory_tile]["recepie"] == -1:
            x = 0
            y = 0
            for recepie in processing_recepies[world[inventory_tile]["building"]]:
                if x >6:
                    x = 0
                    y +=1
                pg.draw.rect(winobj,(0,0,0),(xpos+10+y*153,ypos+310+x*60,150,50))
                pg.draw.rect(winobj,(200,200,200),(xpos+10+y*157,ypos+310+x*60,148,48))
                text_name = dosfont.render(recepie["name"], True, (0,0,0))
                winobj.blit(text_name, (xpos+10+y*160,ypos+310+x*60))
                if isinstance(recepie["required_text"],str):
                    text_required = dosfont.render("Need:"+recepie["required_text"], True, (0,0,0))
                    winobj.blit(text_required, (xpos+10+y*160,ypos+325+x*60))
                else:
                    i = -1
                    for text in recepie["required_text"]:
                        text_required = dosfont.render(text, True, (0,0,0))
                        winobj.blit(text_required, (xpos+10+y*160,ypos+325+x*60+i*9+2))              
                        i+=1
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
    if dialogue[0] != []:
        dialogue_strip = dialogue[0][dialogue[1]]
        if dialogue_strip["character"] != "action":
            if dialogue_strip["character"] == "alphen":
                winobj.blit(pg.transform.scale(player["a"]["dialog"], (cell_size * 3, cell_size * 6)), (cell_size*17, cell_size*14))
            elif dialogue_strip["character"] == "fury":
                winobj.blit(pg.transform.scale(player["f"]["dialog"], (cell_size * 3, cell_size * 6)), (cell_size*17, cell_size*14))
            elif dialogue_strip["character"] == "weles":
                winobj.blit(pg.transform.scale(npc["weles"]["dialog"], (cell_size * 3, cell_size * 6)), (0, cell_size*14))
            
            pg.draw.rect(winobj, (0, 0, 0), (cell_size *3, cell_size * 18, cell_size * 14, cell_size * 2))  
            pg.draw.rect(winobj, (255, 255, 255), (cell_size *3.15, cell_size * 18.15, cell_size * 13.7, cell_size * 1.7))  
            pg.draw.rect(winobj, (0, 0, 0), (cell_size *3.2, cell_size * 18.2, cell_size * 13.6, cell_size * 1.6)) 
            pg.draw.rect(winobj, (0, 0, 0), (cell_size *3.10, cell_size * 18.05, cell_size * 4, cell_size * 0.2))
            
            text_line1 = dosfontbig.render(dialogue_strip["name"], True, (255, 255, 255))
            text_line2 = dosfont.render(dialogue_strip["text"][0], True, (255, 255, 255))
            text_line3 = dosfont.render(dialogue_strip["text"][1], True, (255, 255, 255))
            text_line4 = dosfont.render(dialogue_strip["text"][2], True, (255, 255, 255))
            text_line5 = dosfont.render(dialogue_strip["text"][3], True, (255, 255, 255))
            winobj.blit(text_line1, (cell_size*3.25, cell_size*18.05))
            winobj.blit(text_line2, (cell_size*3.25, cell_size*18.60))
            winobj.blit(text_line3, (cell_size*3.25, cell_size*18.80))
            winobj.blit(text_line4, (cell_size*3.25, cell_size*19 ))
            winobj.blit(text_line5, (cell_size*3.25, cell_size*19.20))
    if inventory[-1] != {} and inventory[-1]["item"] == ("wearables","varu_glasses"):
        winobj.blit(pg.transform.scale(filters["varu_glasses"][0], (cell_size * 20, cell_size * 20)), (0,0))
        for effect_pos in effects:
            winobj.blit(pg.transform.scale(filters["varu_glasses"][1], (cell_size, cell_size)), (cell_size*effect_pos[0],cell_size*effect_pos[1]))
            
        
            



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
    for i,text in enumerate(release_notes):
        pg.draw.rect(winobj,(100,100,100),(int(cell_size*13),int(cell_size * 12+(cell_size*0.5)*i),int(cell_size*7),int(cell_size*0.5)))
        text_info = dosfont125.render(text, True, (0, 255, 0))
        winobj.blit(text_info, (cell_size * 13, cell_size * 12+(cell_size*0.5)*i))        
        
    

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
    pg.draw.rect(winobj, (100, 100, 100), (cell_size * 4, cell_size * 16, cell_size * 8, cell_size * 0.5))
    text_port = dosfontbig.render("Port>" + str(port), True, (0, 255, 0))
    text_ip = dosfontbig.render("IP>" + str(ip), True, (0, 255, 0))
    text_nickname = dosfontbig.render("Nick>" + nick, True, (0, 255, 0))
    text_play_as = dosfontbig.render("Character (A/F)>" + player_type, True, (0, 255, 0))
    winobj.blit(text_port, (cell_size * 4, cell_size * 12))
    winobj.blit(text_ip, (cell_size * 4, cell_size * 14))
    winobj.blit(text_nickname, (cell_size * 4, cell_size * 10))
    winobj.blit(text_play_as, (cell_size * 4, cell_size * 16))

def draw_singleplayer(winobj):
    for i in range(0, 64):
        for i1 in range(0, 64):
            winobj.blit(pg.transform.scale(ui["title"], (cell_size * 2, cell_size * 2)), (i1 * (cell_size * 2), i * (cell_size * 2)))
    winobj.blit(pg.transform.scale(ui["titlename"], (cell_size * 10, cell_size * 5)), (5 * cell_size, 3 * cell_size))
    pg.draw.rect(winobj, (100, 100, 100), (cell_size * 4, cell_size * 10, cell_size * 8, cell_size * 0.5))
    text_play_as = dosfontbig.render("Character (A/F)>" + player_type, True, (0, 255, 0))
    winobj.blit(text_play_as, (cell_size * 4, cell_size * 10))
    


# main cycle
text_cycle = 0
while 1:
    if dialogue[0] != []:
        dialogue_strip = dialogue[0][dialogue[1]]
        if dialogue_strip["character"] == "action":
            if dialogue_strip["text"] == "sell":
                menu = "open"
                menu_tick = 0
                action = "sell" 
            elif dialogue_strip["text"] == "exit":
                menu = "hidden"
                menu_tick = 0
                action = "" 
                if dialogue[1]+1 != len(dialogue[0]):dialogue[1] += 1
                else:dialogue = [[],0]
    else:
        action = ""
    if game_mode == "singleplayer" or game_mode == "multiplayer":
        if tick % 10 == 0 or tick == 59:
            effects = []
            for i in range(0,random.randint(10,20)):
                effects.append((random.randint(0,19),(random.randint(0,19))))        
        for item in inventory:
            if item == {}: break
            else:
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
                    item["info"] = ("Tungsten ingot","Shiny electroconductive","metal.","","","")
                elif item["item"] ==("ingot","resin"):
                    item["info"] = ("Resin sheet","Used to make cables,","fix-tape and some other","electronics","","")
                elif item["item"] ==("basic","plate"):
                    item["info"] = ("Iron plate","Basic sheet of metal.","Good for some basic","buildings.","","")
                elif item["item"] ==("basic","rod"):
                    item["info"] = ("Iron rod","Supporting element in","basic buildings","","","")
                elif item["item"] ==("basic","screws"):
                    item["info"] = ("Screws","Very useful part.","Can repair and be used","in almost everything","","")
                elif item["item"] ==("basic","wire"):
                    item["info"] = ("Copper wire","Highly electroconductive","wire. Used in basic electr-","onics.","","")
                elif item["item"] ==("basic","cable"):
                    item["info"] = ("Cable","Isoalted wire. Used to","transmit energy.","","","")
                elif item["item"] ==("bio","fiber"):
                    item["info"] = ("Biofiber","Biological fiber, made out ","of grass. Used to make","textolite and BioUranium.","","")
                elif item["item"] ==("basic","drill"):
                    item["info"] = ("Basic drill","Can be used to build","Electric drills mk.1-3","","","")
                elif item["item"] ==("uranium","bio"):
                    item["info"] = ("BioUranium fuel rod","Not really radioactive,","but produces a lot of","energy.","","")
                elif item["item"] ==("basic","reinforced_plate"):
                    item["info"] = ("Reinforced metal plate","A better material to","build higher tier","buildings.","","")
                elif item["item"] ==("wearables","varu_glasses"):
                    item["info"] = ("Hi-tech glasses","Glasses, that let you","see settings of things.","Side effects: strong","desire to paint every-.","thing green")                    
                elif item["item"] ==():
                    item["info"] = ("","","","","","")                 
                elif item["item"] ==():
                    item["info"] = ("","","","","","")
        temp_new_blocks = []
        if game_mode == "singleplayer":
            for tile_id,tile in enumerate(world):
                if "tick_timer" in tile: 
                    tile["tick_timer"] -= 1            
        if tick == 59 and game_mode == "singleplayer":
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
                elif tile["building"] == "drill" and tile["part"] == 1 and power_capacity < 10:
                    power_down = True
                if tile["building"] == "smelter" and tile["part"] == 1 and (power_capacity >= 15 or not(power_down) and power_capacity >= 15):
                    power_capacity -= 15
                    power_usage += 15
                    if tile["timer"] == 0 and tile["recepie"] != -1:
                        if tile["inventory"][1] != {}:
                            
                            tile["inventory"][1]["amount"] += processing_recepies[tile["building"]][tile["recepie"]]["output"]["amount"]
                            tile["timer"] = -1
                        elif tile["inventory"][1] == {}:
                            tile["inventory"][1] = processing_recepies[tile["building"]][tile["recepie"]]["output"].copy()
                            tile["timer"] = -1
                    if tile["inventory"][0] != {} and tile["inventory"][0]["amount"] >= processing_recepies[tile["building"]][tile["recepie"]]["required"][0][1] and tile["timer"] == -1:
                        tile["timer"] = processing_recepies[tile["building"]][tile["recepie"]]["time"]
                        tile["tick_timer"]  = (processing_recepies[tile["building"]][tile["recepie"]]["time"]+1)*60
                        if tile["inventory"][0]["amount"] > processing_recepies[tile["building"]][tile["recepie"]]["required"][0][1]:
                            tile["inventory"][0]["amount"] -= processing_recepies[tile["building"]][tile["recepie"]]["required"][0][1]
                        elif tile["inventory"][0]["amount"] == processing_recepies[tile["building"]][tile["recepie"]]["required"][0][1]:
                            tile["inventory"][0] = {}
                    elif tile["timer"]  >= 1:
                        tile["timer"] -=1
                elif tile["building"] == "smelter" and tile["part"] == 1 and power_capacity < 15:
                    power_down = True
                if tile["tile"] == "grass" and random.randint(0, 25) == 0 and tile["building"] == None and game_mode == "singleplayer":
                    tile["tile"] = "leaves"
            x = 0
            y = 0
            if tick == 59 and game_mode == "singleplayer":
                for tile_id, tile in enumerate(world):
                    
                    if x== world_len:
                        y+=1 
                        x = 0  
                    if tile["building"] == "drill" and tile["part"] == 1 and "inventory" in tile and tile["inventory"]["amount"] >= 1:
                        if tile["rotation"] == 0 and x+3 < world_len and world[(x+2)+(y*world_len)]["building"] == "conveyor_belt" and world[(x+2)+(y*world_len)]["inventory"] == {}:
                            world[(x+2)+(y*world_len)]["inventory"] = {"item":tile["inventory"]["item"]}
                            tile["inventory"]["amount"] -= 1
                            world[(x+2)+(y*world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 90 and y-2 >= 0 and world[x+((y-2)*world_len)]["building"] == "conveyor_belt" and world[x+((y-2)*world_len)]["inventory"] == {}:
                            world[x+((y-2)*world_len)]["inventory"] = {"item":tile["inventory"]["item"]}
                            tile["inventory"]["amount"] -= 1
                            world[x+((y-2)*world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 180 and x-2 >= 0 and world[(x-2)+(y*world_len)]["building"] == "conveyor_belt" and world[(x-2)+(y*world_len)]["inventory"] == {}:
                            world[(x-2)+(y*world_len)]["inventory"] = {"item":tile["inventory"]["item"]}
                            tile["inventory"]["amount"] -= 1
                            world[(x-2)+(y*world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 270 and y+3 < world_len and world[x+((y+2)*world_len)]["building"] == "conveyor_belt" and world[x+((y+2)*world_len)]["inventory"] == {}:
                            world[x+((y+2)*world_len)]["inventory"] = {"item":tile["inventory"]["item"]}
                            tile["inventory"]["amount"] -= 1 
                            world[x+((y+2)*world_len)]["not_gotta_work"] = True
                    elif tile["building"] in conveyor_acceptable_processors and tile["part"] == conveyor_acceptable_processors[tile["building"]] and "inventory" in tile and tile["inventory"][-1] != {}:
                        if tile["rotation"] == 0 and x+2 < world_len and world[(x+1)+(y*world_len)]["building"] == "conveyor_belt" and world[(x+1)+(y*world_len)]["inventory"] == {}:
                            world[(x+1)+(y*world_len)]["inventory"] = {"item":tile["inventory"][-1]["item"]}
                            if tile["inventory"][-1]["amount"] != 1:
                                tile["inventory"][-1]["amount"] -= 1
                            else:
                                tile["inventory"][-1] = {}
                            world[(x+1)+(y*world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 90 and y-1 >= 0 and world[x+((y-1)*world_len)]["building"] == "conveyor_belt" and world[x+((y-1)*world_len)]["inventory"] == {}:
                            world[x+((y-1)*world_len)]["inventory"] = {"item":tile["inventory"][-1]["item"]}
                            if tile["inventory"][-1]["amount"] != 1:
                                tile["inventory"][-1]["amount"] -= 1
                            else:
                                tile["inventory"][-1] = {}
                            world[x+((y-2)*world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 180 and x-1 >= 0 and world[(x-1)+(y*world_len)]["building"] == "conveyor_belt" and world[(x-1)+(y*world_len)]["inventory"] == {}:
                            world[(x-1)+(y*world_len)]["inventory"] = {"item":tile["inventory"][-1]["item"]}
                            if tile["inventory"][-1]["amount"] != 1:
                                tile["inventory"][-1]["amount"] -= 1
                            else:
                                tile["inventory"][-1] = {}
                            world[(x-1)+(y*world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 270 and y+2 < world_len and world[x+((y+1)*world_len)]["building"] == "conveyor_belt" and world[x+((y+1)*world_len)]["inventory"] == {}:
                            world[x+((y+1)*world_len)]["inventory"] = {"item":tile["inventory"][-1]["item"]}
                            if tile["inventory"][-1]["amount"] != 1:
                                tile["inventory"][-1]["amount"] -= 1
                            else:
                                tile["inventory"][-1] = {}
                            world[x+((y+1)*world_len)]["not_gotta_work"] = True
                    elif tile["building"] == "storage_container" and tile["part"] == 2:
                        for item_id,item in enumerate(tile["inventory"]):
                            if item != {}:
                                if tile["rotation"] == 0 and x+2 < world_len and world[(x+1)+(y*world_len)]["building"] == "conveyor_belt" and world[(x+1)+(y*world_len)]["inventory"] == {}:
                                    world[(x+1)+(y*world_len)]["inventory"] = {"item":tile["inventory"][item_id]["item"]}
                                    if tile["inventory"][item_id]["amount"] != 1:
                                        tile["inventory"][item_id]["amount"] -= 1
                                    else:
                                        tile["inventory"][item_id] = {}
                                    world[(x+1)+(y*world_len)]["not_gotta_work"] = True
                                elif tile["rotation"] == 90 and y-1 >= 0 and world[x+((y-1)*world_len)]["building"] == "conveyor_belt" and world[x+((y-1)*world_len)]["inventory"] == {}:
                                    world[x+((y-1)*world_len)]["inventory"] = {"item":tile["inventory"][item_id]["item"]}
                                    if tile["inventory"][item_id]["amount"] != 1:
                                        tile["inventory"][item_id]["amount"] -= 1
                                    else:
                                        tile["inventory"][item_id] = {}
                                    world[x+((y-2)*world_len)]["not_gotta_work"] = True
                                elif tile["rotation"] == 180 and x-1 >= 0 and world[(x-1)+(y*world_len)]["building"] == "conveyor_belt" and world[(x-1)+(y*world_len)]["inventory"] == {}:
                                    world[(x-1)+(y*world_len)]["inventory"] = {"item":tile["inventory"][item_id]["item"]}
                                    if tile["inventory"][item_id]["amount"] != 1:
                                        tile["inventory"][item_id]["amount"] -= 1
                                    else:
                                        tile["inventory"][item_id] = {}
                                    world[(x-1)+(y*world_len)]["not_gotta_work"] = True
                                elif tile["rotation"] == 270 and y+2 < world_len and world[x+((y+1)*world_len)]["building"] == "conveyor_belt" and world[x+((y+1)*world_len)]["inventory"] == {}:
                                    world[x+((y+1)*world_len)]["inventory"] = {"item":tile["inventory"][item_id]["item"]}
                                    if tile["inventory"][item_id]["amount"] != 1:
                                        tile["inventory"][item_id]["amount"] -= 1
                                    else:
                                        tile["inventory"][item_id] = {}
                                    world[x+((y+1)*world_len)]["not_gotta_work"] = True                                
                                break
                    elif tile["building"] == "conveyor_belt" and "item" in tile["inventory"]:
                        if tile["rotation"] == 0 and y-1 < world_len and world[(x+1)+(y*world_len)]["rotation"] == 0 and world[(x+1)+(y*world_len)]["building"] in processors and processing_recepies[world[(x+1)+(y*world_len)]["building"]][world[(x+1)+(y*world_len)]["recepie"]]["required"][world[(x+1)+(y*world_len)]["part"]-1][0] == tile["inventory"]["item"]:
                            if world[(x+1)+(y*world_len)]["inventory"][world[(x+1)+(y*world_len)]["part"]-1] == {}:
                                world[(x+1)+(y*world_len)]["inventory"][world[(x+1)+(y*world_len)]["part"]-1] = {"item":tile["inventory"]["item"], "amount":1}
                            else:
                                world[(x+1)+(y*world_len)]["inventory"][world[(x+1)+(y*world_len)]["part"]-1]["amount"] += 1
                            tile["inventory"] = {}
                        elif tile["rotation"] == 90 and y-1 < world_len and world[x+((y-1)*world_len)]["rotation"] == 90 and world[x+((y-1)*world_len)]["building"] in processors and processing_recepies[world[x+((y-1)*world_len)]["building"]][world[x+((y-1)*world_len)]["recepie"]]["required"][world[x+((y-1)*world_len)]["part"]-1][0] == tile["inventory"]["item"]:
                            if world[x+((y-1)*world_len)]["inventory"][world[x+((y-1)*world_len)]["part"]-1] == {}:
                                world[x+((y-1)*world_len)]["inventory"][world[x+((y-1)*world_len)]["part"]-1] = {"item":tile["inventory"]["item"], "amount":1}
                            else:
                                world[x+((y-1)*world_len)]["inventory"][world[x+((y-1)*world_len)]["part"]-1]["amount"] += 1
                            tile["inventory"] = {}
                        elif tile["rotation"] == 180 and y-1 < world_len and world[(x-1)+(y*world_len)]["rotation"] == 180 and world[(x-1)+(y*world_len)]["building"] in processors and processing_recepies[world[(x-1)+(y*world_len)]["building"]][world[(x-1)+(y*world_len)]["recepie"]]["required"][world[(x-1)+(y*world_len)]["part"]-1][0] == tile["inventory"]["item"]:
                            if world[(x-1)+(y*world_len)]["inventory"][world[(x-1)+(y*world_len)]["part"]-1] == {}:
                                world[(x-1)+(y*world_len)]["inventory"][world[(x-1)+(y*world_len)]["part"]-1] = {"item":tile["inventory"]["item"], "amount":1}
                            else:
                                world[(x-1)+(y*world_len)]["inventory"][world[(x-1)+(y*world_len)]["part"]-1]["amount"] += 1
                            tile["inventory"] = {}
                        elif tile["rotation"] == 270 and y+1 < world_len and world[x+((y+1)*world_len)]["rotation"] == 270 and world[x+((y+1)*world_len)]["building"] in processors and processing_recepies[world[x+((y+1)*world_len)]["building"]][world[x+((y+1)*world_len)]["recepie"]]["required"][world[x+((y+1)*world_len)]["part"]-1][0] == tile["inventory"]["item"]:
                            if world[x+((y+1)*world_len)]["inventory"][world[x+((y+1)*world_len)]["part"]-1] == {}:
                                world[x+((y+1)*world_len)]["inventory"][world[x+((y+1)*world_len)]["part"]-1] = {"item":tile["inventory"]["item"], "amount":1}
                            else:
                                world[x+((y+1)*world_len)]["inventory"][world[x+((y+1)*world_len)]["part"]-1]["amount"] += 1
                            tile["inventory"] = {}
                        elif tile["rotation"] == 0 and y-1 < world_len and world[(x+1)+(y*world_len)]["rotation"] == 0 and world[(x+1)+(y*world_len)]["building"] == "storage_container":
                            for item_id, item in enumerate(world[(x+1)+(y*world_len)]["inventory"]):
                                if item == {}:
                                    world[(x+1)+(y*world_len)]["inventory"][item_id] = {"item":tile["inventory"]["item"], "amount":1}
                                    tile["inventory"] = {}
                                    break
                                elif item != {} and item["item"] == tile["inventory"]["item"] and item["amount"] < 200: 
                                    world[(x+1)+(y*world_len)]["inventory"][item_id]["amount"] += 1
                                    tile["inventory"] = {}  
                                    break
                        elif tile["rotation"] == 90 and y-1 < world_len and world[x+((y-1)*world_len)]["rotation"] == 90 and world[x+((y-1)*world_len)]["building"] == "storage_container":
                            for item_id, item in enumerate(world[x+((y-1)*world_len)]["inventory"]):
                                if item == {}:
                                    world[x+((y-1)*world_len)]["inventory"][item_id] = {"item":tile["inventory"]["item"], "amount":1}
                                    tile["inventory"] = {}
                                    break
                                elif item != {} and item["item"] == tile["inventory"]["item"] and item["amount"] < 200: 
                                    world[x+((y-1)*world_len)]["inventory"][item_id]["amount"] += 1
                                    tile["inventory"] = {}  
                                    break
                        elif tile["rotation"] == 180 and y-1 < world_len and world[(x-1)+(y*world_len)][item_id]["rotation"] == 180 and world[(x-1)+(y*world_len)]["building"] == "storage_container":
                            for item_id, item in enumerate(world[(x-1)+(y*world_len)]["inventory"]):
                                if item == {}:
                                    world[(x-1)+(y*world_len)]["inventory"][item_id] = {"item":tile["inventory"]["item"], "amount":1}
                                    tile["inventory"] = {}
                                    break
                                elif item != {} and item["item"] == tile["inventory"]["item"] and item["amount"] < 200: 
                                    world[(x-1)+(y*world_len)]["inventory"][item_id]["amount"] += 1
                                    tile["inventory"] = {}
                                    break    
                        elif tile["rotation"] == 270 and y+1 < world_len and world[x+((y+1)*world_len)]["rotation"] == 270 and world[x+((y+1)*world_len)]["building"] == "storage_container":
                            for item_id, item in enumerate(world[x+((y+1)*world_len)]["inventory"]):
                                if item == {}:
                                    world[x+((y+1)*world_len)]["inventory"][item_id] = {"item":tile["inventory"]["item"], "amount":1}
                                    tile["inventory"] = {}
                                    break
                                elif item != {} and item["item"] == tile["inventory"]["item"] and item["amount"] < 200: 
                                    world[x+((y+1)*world_len)]["inventory"][item_id]["amount"] += 1
                                    tile["inventory"] = {}  
                                    break                                  
                        elif tile["rotation"] == 0 and x+1 < world_len and world[(x+1)+(y*world_len)]["building"] == "conveyor_belt" and world[(x+1)+(y*world_len)]["inventory"] == {} and not "not_gotta_work" in tile:
                            world[(x+1)+(y*world_len)]["inventory"] = {"item":tile["inventory"]["item"]}
                            tile["inventory"] = {}
                            world[(x+1)+(y*world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 90 and y-1 >= 0 and world[x+((y-1)*world_len)]["building"] == "conveyor_belt" and world[x+((y-1)*world_len)]["inventory"] == {} and not "not_gotta_work" in tile:
                            world[x+((y-1)*world_len)]["inventory"] = {"item":tile["inventory"]["item"]}
                            tile["inventory"] = {}
                            world[x+((y-1)*world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 180 and x-1>= 0 and world[(x-1)+(y*world_len)]["building"] == "conveyor_belt" and world[(x-1)+(y*world_len)]["inventory"] == {} and not "not_gotta_work" in tile:
                            world[(x-1)+(y*world_len)]["inventory"] = {"item":tile["inventory"]["item"]}
                            tile["inventory"] = {}
                            world[(x-1)+(y*world_len)]["not_gotta_work"] = True
                        elif tile["rotation"] == 270 and y+1 < world_len and world[x+((y+1)*world_len)]["building"] == "conveyor_belt" and world[x+((y+1)*world_len)]["inventory"] == {} and not "not_gotta_work" in tile:
                            world[x+((y+1)*world_len)]["inventory"] = {"item":tile["inventory"]["item"]}
                            tile["inventory"] = {}
                            world[x+((y+1)*world_len)]["not_gotta_work"] = True
                            
                    x+=1
                for tile in world:
                    if "not_gotta_work" in tile: 
                        tile.pop("not_gotta_work")
                  
                tick = 0            
                
        if tick == 59: tick = 0
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
        elif player_state_timer == 0 and player_state != "building":
            player_state = "default"
        if player_state_timer > 0:
            player_state_timer -= 1
        if menu_tick == 0 and menu == "closing":
            menu = "hidden"
        if menu_tick == 0 and menu == "opening":
            menu = "open"
        draw_world(world, window, tick, pos, [tooltip_tick, tooltip_tile], [menu_tick, menu], mode == "building", [facing != 0, player_state],action,effects)
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                running_thread = False
                pg.quit()
                sys.exit()
            elif evt.type == pg.KEYDOWN:

                keys = pg.key.get_pressed()
                if keys[pg.K_m] and dialogue[0] == []:
                    if mode == "building":
                        player_state = "default"
                        mode = "!building"
                        current_item = []
                        category = 0
                    elif mode == "!building":
                        mode = "building"
                        player_state = "building"
                elif keys[pg.K_TAB] and menu == "hidden" and game_mode == "multiplayer":
                    if not(chat_open): recent_messages = []
                    chat_open = not(chat_open)
                elif mode == "building" and keys[pg.K_r]  and not(chat_open):
                    if current_item[1] != 270:
                        current_item[1] += 90
                    else:
                        current_item[1] = 0
                elif mode == "building" and keys[pg.K_5] and category != 0:
                    category = 0
                elif mode == "building" and keys[pg.K_5] and current_item != [] and not(chat_open):
                    current_item = []
                elif keys[pg.K_1] and dialogue[0] != [] and "choice" in dialogue[0][dialogue[1]]:
                    action = dialogue[0][dialogue[1]]["choice"][1]
                    if action == "continue":
                        if len(dialogue[0]) != dialogue[1]+1: 
                            dialogue[1] += 1
                        else: 
                            dialogue[0] = []
                            dialogue[1] = 0  
                    elif action == "deal_accept":
                        deal = dialogue[0][dialogue[1]]["deal"]
                        if coins >= deal["cost"]:
                            added = False
                            for item_id, item in enumerate(inventory):
                                if "item" in item and item["item"] == deal["item"]  and item["amount"] < 200:
                                    inventory[item_id]["amount"] = inventory[item_id]["amount"] + deal["amount"]
                                    added = True
                            if not(added):
                                for item_id, item in enumerate(inventory):
                                    if item == {}:
                                        inventory[item_id] = {"item":deal["item"],"amount":deal["amount"]}
                                        added = True
                                        break     
                            if added:
                                coins -= deal["cost"]
                        if len(dialogue[0]) != dialogue[1]+1: 
                            dialogue[1] += 1
                        else: 
                            dialogue[0] = []
                            dialogue[1] = 0  
                            
                elif keys[pg.K_2] and dialogue[0] != [] and "choice" in dialogue[0][dialogue[1]]:
                    action = dialogue[0][dialogue[1]]["choice"][2]
                    if action == "continue":
                        if len(dialogue[0]) != dialogue[1]+1: 
                            dialogue[1] += 1
                        else: 
                            dialogue[0] = []
                            dialogue[1] = 0
                    elif action == "deal_accept":
                        deal = dialogue[0][dialogue[1]]["deal"]
                        if coins >= deal["cost"]:
                            added = False
                            for item_id, item in enumerate(inventory):
                                if "item" in item and item["item"] == deal["item"]  and item["amount"] < 200:
                                    inventory[item_id]["amount"] = inventory[item_id]["amount"] + deal["amount"]
                                    added = True
                            if not(added):
                                for item_id, item in enumerate(inventory):
                                    if item == {}:
                                        inventory[item_id] = {"item":deal["item"],"amount":deal["amount"]}
                                        added = True
                                        break     
                            if added:
                                coins -= deal["cost"]
                        if len(dialogue[0]) != dialogue[1]+1: 
                            dialogue[1] += 1
                        else: 
                            dialogue[0] = []
                            dialogue[1] = 0  
                elif keys[pg.K_6] and category == 0 and not(chat_open) and mode == "building" and mode == "!building":
                    mode = "!building"
                    if player_type == "undefined":
                        deal1 = create_deal()
                        deal2 =create_deal()
                        deal3 =create_deal()
                        dialogue[0] = [
                            {
                                "character":"weles",
                                "name":"Weles",
                                "text":["шаблон диалога пиши на английском - твой персонаж","","",""]
                            },
                            {
                                "character":"alphen",
                                "name":"Alphen",
                                "text":["шаблон диалога - мой персонаж (потом сам отредачу)","","",""]
                            },
                            {
                                "character":"action",
                                "text":"sell"
                            },
                            {
                                "character":"action",
                                "text":"exit"
                            },
                            {
                                "character":"weles",
                                "name":"Weles",
                                "deal":deal1,
                                "choice":{1:"deal_accept",2:"continue"},
                                "text":["шаблон сделки {0} это предмет {1} это стоимость {2} это количество порядок любой".format(deal_translations[deal1["item"]],deal1["cost"],deal1["amount"]),"1> принять","2> отказаться","Coins: {}".format(coins)]                                
                            }
                        ]
                elif keys[pg.K_5] and mode == "building" and category == 0 and not(chat_open):
                    current_item = ["disassemble",0,("","","",""),()]                
                elif keys[pg.K_1] and category == 0 and not(chat_open) and mode == "building":
                    category = 1 
                elif keys[pg.K_2] and category == 0 and not(chat_open) and mode == "building":
                    category = 2                
                elif keys[pg.K_3] and category == 0 and not(chat_open) and mode == "building":
                    category = 3   
                elif keys[pg.K_4] and category == 0 and not(chat_open) and mode == "building":
                    category = 4                       
                elif keys[pg.K_1] and category == 1 and not(chat_open) and mode == "building":
                    current_item = ["drill",0,("Basic drill","Iron plate x3","Copper wire x5",""),((("basic","drill"),1),(("basic","plate"),3),(("basic","wire"),5))] 
                elif keys[pg.K_1] and category == 2 and not(chat_open) and mode == "building":
                    current_item = ["biomass_burner",0,("Copper wire x10","Iron plate x5","",""),((("basic","plate"),5),(("basic","wire"),10))]                 
                elif keys[pg.K_1] and category == 3 and not(chat_open) and mode == "building":
                    current_item = ["conveyor_belt_mk1",0,("Iron plate x1","","",""),((("basic","plate"),1))]                
                elif keys[pg.K_1] and category == 4 and not(chat_open) and mode == "building":
                    current_item = ["smelter",0,("Iron plate x2","Copper wire x10","Iron rod x5",""),((("basic","plate"),2),(("basic","wire"),10),(("basic","rod"),5))] 
                elif keys[pg.K_4] and category == 3 and not(chat_open) and mode == "building":
                    current_item = ["storage_container",0,("Iron plate x5","Iron rod x2","",""),((("basic","plate"),5),(("basic","rod"),1))]                      
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
                    if menu == "open" and inventory_tile == "" and action == "":
                        x = 0
                        y = 0
                        for y in range(0,3):
                            for x in range(0,9):
                                if 5 + 10 * x+ (cell_size * 2) * x <= coords[0] and 5 + 10 * x + (cell_size * 2) * x+ (cell_size * 2) >= coords[0] and 5 + 10 * y+ (cell_size * 2) * y <= coords[1] and 5 + 10 * y + (cell_size * 2) * y+ (cell_size * 2)>= coords[1]:
                                    if cursor_tile_id != -1 and x+y*9 <=26 and inventory[x+y*9] == {} and inventory[cursor_tile_id] != {} and cursor_tile_id != x+y*9:
                                        temp_var = inventory[cursor_tile_id].copy()
                                        inventory[cursor_tile_id] = {}
                                        inventory[x+y*9]= temp_var
                                        cursor_tile_id = -1
                                    elif cursor_tile_id != -1 and x+y*9 <=26 and inventory[x+y*9] != {} and inventory[cursor_tile_id] != {} and inventory[x+y*9]["item"] == inventory[cursor_tile_id]["item"] and cursor_tile_id != x+y*9:
                                        temp_var = inventory[cursor_tile_id]["amount"]
                                        inventory[cursor_tile_id] = {}
                                        inventory[x+y*9]["amount"] += temp_var
                                        cursor_tile_id = -1                                            
                                    else:
                                        cursor_tile_id = x+y*9
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
                            if coords[0] >= 20+y*155 and coords[0] <= 10+y*155+150 and coords[1] >=310+x*60 and coords[1] < 310+x*60+50 and {} in inventory:
                                for item in recepie["required"]:
                                    can_craft =False
                                    for inv_item_id, inv_item in enumerate(inventory):
                                        if inv_item != {} and item[0] == inv_item["item"] and item[1] <= inv_item["amount"]:
                                            can_craft = True
                                            item_ids.append([inv_item_id,item[1]])
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
                                        inventory[id_to_pop] = {}
                                    for item_id, item in enumerate(inventory):
                                        if "item" in item and item["item"] == recepie["output"]["item"]  and item["amount"] < 200:
                                            inventory[item_id]["amount"] = inventory[item_id]["amount"] + recepie["output"]["amount"]
                                            added = True
                                    if not(added):
                                        for item_id, item in enumerate(inventory):
                                            if item == {}:
                                                inventory[item_id] = recepie["output"]
                                                break
                                    recepie["output"]   = a
                            x+=1
                    if menu == "open" and inventory_tile == "" and action == "sell":
                        x = 0
                        y = 0
                        for y in range(0,3):
                            for x in range(0,9):
                                if 5 + 10 * x+ (cell_size * 2) * x <= coords[0] and 5 + 10 * x + (cell_size * 2) * x+ (cell_size * 2) >= coords[0] and 5 + 10 * y+ (cell_size * 2) * y <= coords[1] and 5 + 10 * y + (cell_size * 2) * y+ (cell_size * 2)>= coords[1]:
                                    if inventory[x+y*9] != {}:
                                        if inventory[x+y*9]["item"] in item_costs:
                                            coins +=item_costs[inventory[x+y*9]["item"]] 
                                            if inventory[x+y*9]["amount"] > 1:
                                                inventory[x+y*9]["amount"] -= 1
                                            else:
                                                inventory[x+y*9] = {}
                                    else:
                                        cursor_tile_id = x+y*9
                    if menu == "open" and inventory_tile != "" and action == "":
                        x = 0
                        y = 0
                        for y in range(0,3):
                            for x in range(0,9):
                                if 5 + 10 * x+ (cell_size * 2) * x <= coords[0] and 5 + 10 * x + (cell_size * 2) * x+ (cell_size * 2) >= coords[0] and 5 + 10 * y+ (cell_size * 2) * y <= coords[1] and 5 + 10 * y + (cell_size * 2) * y+ (cell_size * 2)>= coords[1]:
                                    if cursor_tile_id == -2 and inventory[x+y*9] == {}:
                                        temp_var = world[inventory_tile]["inventory"].copy()
                                        if world[inventory_tile]["building"] == "drill":
                                            world[inventory_tile]["inventory"]["amount"] = 0
                                        else:
                                            world[inventory_tile]["inventory"] = {}
                                        inventory[x+y*9] = temp_var
                                        cursor_tile_id = -1
                                        temp_new_blocks.append({"id": inventory_tile, "tile": world[inventory_tile]}) 
                                    elif cursor_tile_id == -2 and inventory[x+y*9]["item"] == world[inventory_tile]["inventory"]["item"] and world[inventory_tile]["inventory"]["amount"] != 0:
                                        temp_var = world[inventory_tile]["inventory"]["amount"]
                                        if world[inventory_tile]["building"] == "drill":
                                            world[inventory_tile]["inventory"]["amount"] = 0
                                        else:
                                            world[inventory_tile]["inventory"] = {}                                        
                                        inventory[x+y*9]["amount"] += temp_var
                                        cursor_tile_id = -1
                                        temp_new_blocks.append({"id": inventory_tile, "tile": world[inventory_tile]})
                                    elif cursor_tile_id < -2 and inventory[x+y*9] == {} and world[inventory_tile]["inventory"][abs(cursor_tile_id)-3] != {}:
                                        temp_var = world[inventory_tile]["inventory"][abs(cursor_tile_id)-3].copy()
                                        world[inventory_tile]["inventory"][abs(cursor_tile_id)-3] = {}
                                        inventory[x+y*9] = temp_var
                                        cursor_tile_id = -1            
                                        temp_new_blocks.append({"id": inventory_tile, "tile": world[inventory_tile]})
                                    elif cursor_tile_id < -2 and inventory[x+y*9] != {} and inventory[x+y*9]["item"] == world[inventory_tile]["inventory"][abs(cursor_tile_id)-3]["item"] and world[inventory_tile]["inventory"][abs(cursor_tile_id)-3]["amount"] != 0 and world[inventory_tile]["inventory"][abs(cursor_tile_id)-3] != {}:
                                        temp_var = world[inventory_tile]["inventory"][abs(cursor_tile_id)-3]["amount"]
                                        world[inventory_tile]["inventory"][abs(cursor_tile_id)-3] = {}
                                        inventory[x+y*9]["amount"] += temp_var
                                        cursor_tile_id = -1
                                        temp_new_blocks.append({"id": inventory_tile, "tile": world[inventory_tile]})                                        
                                    elif cursor_tile_id > -1 and inventory[x+y*9] == {} and inventory[cursor_tile_id] != {} and cursor_tile_id != x+y*9:
                                        temp_var = inventory[cursor_tile_id].copy()
                                        inventory[cursor_tile_id] = {}
                                        inventory[x+y*9] = temp_var
                                        cursor_tile_id = -1
                                    elif cursor_tile_id > -1 and inventory[cursor_tile_id] != {} and inventory[x+y*9]["item"] == inventory[cursor_tile_id]["item"] and inventory[x+y*9] == {} and inventory[cursor_tile_id] == {} and cursor_tile_id != x+y*9:
                                        temp_var = inventory[cursor_tile_id]["amount"]
                                        inventory[cursor_tile_id] = {}
                                        inventory[x+y*9]["amount"] += temp_var
                                        cursor_tile_id = -1                                            
                                    else:
                                        cursor_tile_id = x+y*9 
                        if power_down and coords[0] >= cell_size and coords[0] <= cell_size*3 and coords[1] <= cell_size*13 and coords[1] >= cell_size*9: # 
                            power_down = False
                        if type(world[inventory_tile]["inventory"]) != list:
                            x = 5
                            y = 4
                            if 5 + 10 * x+ (cell_size * 2) * x <= coords[0] and 5 + 10 * x + (cell_size * 2) * x+ (cell_size * 2) >= coords[0] and 5 + 10 * y+ (cell_size * 2) * y <= coords[1] and 5 + 10 * y + (cell_size * 2) * y+ (cell_size * 2)>= coords[1]:
                                if cursor_tile_id > -1:
                                    if world[inventory_tile]["building"] != "drill":
                                        if cursor_tile_id != -1 and world[inventory_tile]["inventory"] == {}:
                                            if world[inventory_tile]["building"] != "biomass_burner":
                                                temp_var = inventory[cursor_tile_id].copy()
                                                inventory[cursor_tile_id] = {}
                                                world[inventory_tile]["inventory"] = temp_var
                                                cursor_tile_id = -1    
                                                temp_new_blocks.append({"id": inventory_tile, "tile": world[inventory_tile]})                                                
                                            else:
                                                if inventory[cursor_tile_id]["item"] == ("uranium","bio"):
                                                    temp_var = inventory[cursor_tile_id].copy()
                                                    inventory[cursor_tile_id] = {}
                                                    world[inventory_tile]["inventory"] = temp_var
                                                    cursor_tile_id = -1
                                                    temp_new_blocks.append({"id": inventory_tile, "tile": world[inventory_tile]})                                                    
                                        elif cursor_tile_id >= 0 and world[inventory_tile]["inventory"]["item"] == inventory[cursor_tile_id]["item"] and world[inventory_tile]["inventory"]["amount"] != 0:
                                            if world[inventory_tile]["building"] != "biomass_burner":
                                                temp_var = inventory[cursor_tile_id]["amount"]
                                                inventory[cursor_tile_id] = {}
                                                world[inventory_tile]["inventory"][abs(cursor_tile_id)-2] += temp_var
                                                cursor_tile_id = -1
                                                temp_new_blocks.append({"id": inventory_tile, "tile": world[inventory_tile]})                       
                                            else:
                                                if inventory[cursor_tile_id]["item"] == ("uranium","bio"):    
                                                    temp_var = inventory[cursor_tile_id]["amount"]
                                                    inventory[cursor_tile_id] = {}
                                                    world[inventory_tile]["inventory"][abs(cursor_tile_id)-2] += temp_var
                                                    cursor_tile_id = -1
                                                    temp_new_blocks.append({"id": inventory_tile, "tile": world[inventory_tile]})                       
                                                    
                                else:
                                    if world[inventory_tile]["inventory"] != {}:
                                        cursor_tile_id = -2  
                        elif "recepie" in world[inventory_tile] and world[inventory_tile]["recepie"] != -1 or not("recepie" in world[inventory_tile]):
                            y = 4
                            x = 0
                            for x_1 in range(len(world[inventory_tile]["inventory"])):
                                if x == 9:
                                    x = 0
                                    y += 1
                                check_x = x
                                if x+1 == len(world[inventory_tile]["inventory"]) and len(world[inventory_tile]["inventory"]) <= 5:
                                    check_x+= 1                                 
                                if 5 + 10 * check_x+ (cell_size * 2 * check_x) <= coords[0] and 5 + 10 * check_x + (cell_size * 2 * check_x)+ (cell_size * 2) >= coords[0] and 5 + 10 * y+ (cell_size * 2) * y <= coords[1] and 5 + 10 * y + (cell_size * 2) * y+ (cell_size * 2)>= coords[1]:
                                    if cursor_tile_id > -1:
                                        if x+1 == len(world[inventory_tile]["inventory"]) and len(world[inventory_tile]["inventory"]) <= 5:
                                            x+= 1 
                                        if world[inventory_tile]["building"] != "drill":
                                            if cursor_tile_id >= 0 and world[inventory_tile]["inventory"][x+(y-4)*9] == {}:
                                                if len(world[inventory_tile]["inventory"]) == 2 and inventory[cursor_tile_id]["item"] == processing_recepies[world[inventory_tile]["building"]][world[inventory_tile]["recepie"]]["required"][0][0] or len(world[inventory_tile]["inventory"]) > 2:
                                                    temp_var = inventory[cursor_tile_id].copy()
                                                    inventory[cursor_tile_id] = {}
                                                    world[inventory_tile]["inventory"][x+(y-4)*9] = temp_var
                                                    cursor_tile_id = -1         
                                                    new_blocks.append({"id": inventory_tile, "tile": world[inventory_tile]})
                                                    
                                            elif cursor_tile_id >= 0 and world[inventory_tile]["inventory"][x+(y-4)*9]["item"] == inventory[cursor_tile_id]["item"] and world[inventory_tile]["inventory"][x]["amount"] != 0 or len(world[inventory_tile]["inventory"]) > 2:
                                                if len(world[inventory_tile]["inventory"]) == 2 and inventory[cursor_tile_id]["item"] == processing_recepies[world[inventory_tile]["building"]][world[inventory_tile]["recepie"]]["required"][0][0] or len(world[inventory_tile]["inventory"]) > 2:
                                                    temp_var = inventory[cursor_tile_id]["amount"]
                                                    inventory[cursor_tile_id] = {}
                                                    world[inventory_tile]["inventory"][x+(y-4)*9] += temp_var
                                                    cursor_tile_id = -1 
                                                    new_blocks.append({"id": inventory_tile, "tile": world[inventory_tile]})                                                    
                                    else:
                                        cursor_tile_id= -1*(x+3)
                                x += 1
                        elif world[inventory_tile]["recepie"] == -1:
                            x = 0
                            y = 0
                            for recepie in processing_recepies[world[inventory_tile]["building"]]: #(xpos+10+y*155,ypos+310+x*60,150,50)
                                if x > 6:
                                    x = 0
                                    y += 1
                                can_craft = False
                                added = False
                                item_ids = []
                                ids_to_pop = []
                                if coords[0] >= 20+y*155 and coords[0] <= 10+y*155+150 and coords[1] >=310+x*60 and coords[1] < 310+x*60+50:
                                    world[inventory_tile]["recepie"] = x+y*6
                                    new_blocks.append({"id": inventory_tile, "tile": world[inventory_tile]}) 
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
                    if mode == "building" and current_item != [] and not(chat_open) and menu == "hidden" and current_item[0] != "" and dialogue[0] == []:    
                        built = False
                        can_craft = False
                        added = False
                        item_ids = []
                        ids_to_pop = []
                        for item in current_item[3]:
                            for inv_item_id, inv_item in enumerate(inventory):
                                can_craft = False
                                if inv_item != {} and item[0] == inv_item["item"] and item[1] <= inv_item["amount"]:
                                    can_craft = True
                                    item_ids.append((inv_item_id,item[1]))
                                    break
                            if can_craft == False:  
                                break                         
                        if current_item[0] == "drill" and "ore" in world[x + (y * world_len)]["tile"] and can_craft:
                            if current_item[1] == 0:
                                if x >= 0 and x < world_len - 1 and y >= 0 and y <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[(x + 1) + (y * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[(x + 1) + (y * world_len)]["tile"] == "leaves":
                                        world[(x + 1) + (y * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "drill"
                                    world[(x + 1) + (y * world_len)]["building"] = "drill"
                                    world[x + (y * world_len)]["inventory"] = {"amount":1,"item":("unprocessed",world[x + (y * world_len)]["tile"][:-4])}
                                    world[(x+1) + (y * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[(x + 1) + (y * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 1
                                    world[(x + 1) + (y * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                                    built = True
                            elif current_item[1] == 90:
                                if y > 0 and y <= world_len - 1 and x >= 0 and x <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[x + ((y - 1) * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[x + ((y - 1) * world_len)]["tile"] == "leaves":
                                        world[x + ((y - 1) * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "drill"
                                    world[x + ((y - 1) * world_len)]["building"] = "drill"
                                    world[x + (y * world_len)]["inventory"] = {"amount":1,"item":("unprocessed",world[x + (y * world_len)]["tile"][:-4])}
                                    world[x + ((y-1) * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["rotation"] = 90
                                    world[x + ((y - 1) * world_len)]["rotation"] = 90
                                    world[x + (y * world_len)]["part"] = 1
                                    world[x + ((y - 1) * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                    built = True
                            elif current_item[1] == 180:
                                if x > 0 and x <= world_len - 1 and y >= 0 and y <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[(x - 1) + (y * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[(x - 1) + (y * world_len)]["tile"] == "leaves":
                                        world[(x - 1) + (y * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "drill"
                                    world[(x - 1) + (y * world_len)]["building"] = "drill"
                                    world[x + (y * world_len)]["inventory"] = {"amount":1,"item":("unprocessed",world[x + (y * world_len)]["tile"][:-4])}
                                    world[(x-1) + (y * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["rotation"] = 180
                                    world[(x - 1) + (y * world_len)]["rotation"] = 180
                                    world[x + (y * world_len)]["part"] = 1
                                    world[(x - 1) + (y * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x - 1) + (y * world_len)]})
                                    built = True
                            elif current_item[1] == 270:
                                if y >= 0 and y < world_len - 1 and x >= 0 and x <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[x + ((y + 1) * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[x + ((y + 1) * world_len)]["tile"] == "leaves":
                                        world[x + ((y + 1) * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "drill"
                                    world[x + ((y + 1) * world_len)]["building"] = "drill"
                                    world[x + (y * world_len)]["inventory"] = {"amount":1,"item":("unprocessed",world[x + (y * world_len)]["tile"][:-4])}
                                    world[x + ((y+1) * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["rotation"] = 270
                                    world[x + ((y + 1) * world_len)]["rotation"] = 270
                                    world[x + (y * world_len)]["part"] = 1
                                    world[x + ((y + 1) * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y + 1) * world_len)]})
                                    built = True       
                        elif current_item[0] == "storage_container" and can_craft:
                            if current_item[1] == 0:
                                if x >= 0 and x < world_len - 1 and y >= 0 and y <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[(x + 1) + (y * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[(x + 1) + (y * world_len)]["tile"] == "leaves":
                                        world[(x + 1) + (y * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "storage_container"
                                    world[(x + 1) + (y * world_len)]["building"] = "storage_container"
                                    world[x + (y * world_len)]["inventory"] = []
                                    for i in range(0,10): world[x + (y * world_len)]["inventory"].append({})
                                    world[(x+1) + (y * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[(x + 1) + (y * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 1
                                    world[(x + 1) + (y * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                                    built = True
                            elif current_item[1] == 90:
                                if y > 0 and y <= world_len - 1 and x >= 0 and x <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[x + ((y - 1) * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[x + ((y - 1) * world_len)]["tile"] == "leaves":
                                        world[x + ((y - 1) * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "storage_container"
                                    world[x + ((y - 1) * world_len)]["building"] = "storage_container"
                                    world[x + (y * world_len)]["inventory"] = []
                                    for i in range(0,10): world[x + (y * world_len)]["inventory"].append({})
                                    world[x + ((y-1) * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["rotation"] = 90
                                    world[x + ((y - 1) * world_len)]["rotation"] = 90
                                    world[x + (y * world_len)]["part"] = 1
                                    world[x + ((y - 1) * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                    built = True
                            elif current_item[1] == 180:
                                if x > 0 and x <= world_len - 1 and y >= 0 and y <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[(x - 1) + (y * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[(x - 1) + (y * world_len)]["tile"] == "leaves":
                                        world[(x - 1) + (y * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "storage_container"
                                    world[(x - 1) + (y * world_len)]["building"] = "storage_container"
                                    world[x + (y * world_len)]["inventory"] = []
                                    for i in range(0,10): world[x + (y * world_len)]["inventory"].append({})
                                    world[(x-1) + (y * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["rotation"] = 180
                                    world[(x - 1) + (y * world_len)]["rotation"] = 180
                                    world[x + (y * world_len)]["part"] = 1
                                    world[(x - 1) + (y * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x - 1) + (y * world_len)]})
                                    built = True
                            elif current_item[1] == 270:
                                if y >= 0 and y < world_len - 1 and x >= 0 and x <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[x + ((y + 1) * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[x + ((y + 1) * world_len)]["tile"] == "leaves":
                                        world[x + ((y + 1) * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "storage_container"
                                    world[x + ((y + 1) * world_len)]["building"] = "storage_container"
                                    world[x + (y * world_len)]["inventory"] = []
                                    for i in range(0,10): world[x + (y * world_len)]["inventory"].append({})
                                    world[x + ((y+1) * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["rotation"] = 270
                                    world[x + ((y + 1) * world_len)]["rotation"] = 270
                                    world[x + (y * world_len)]["part"] = 1
                                    world[x + ((y + 1) * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y + 1) * world_len)]})
                                    built = True       
                        elif current_item[0] == "smelter" and can_craft:
                            if current_item[1] == 0:
                                if x >= 0 and x < world_len - 1 and y >= 0 and y <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[(x + 1) + (y * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[(x + 1) + (y * world_len)]["tile"] == "leaves":
                                        world[(x + 1) + (y * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "smelter"
                                    world[(x + 1) + (y * world_len)]["building"] = "smelter"
                                    world[x + (y * world_len)]["inventory"] = [{},{}]
                                    world[(x + 1)+ (y * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["recepie"] = -1
                                    world[x + (y * world_len)]["timer"] = -1
                                    world[x + (y * world_len)]["tick_timer"] = -1
                                    world[x + (y * world_len)]["rotation"] = 0
                                    world[(x + 1) + (y * world_len)]["rotation"] = 0
                                    world[x + (y * world_len)]["part"] = 1
                                    world[(x + 1) + (y * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                                    built = True
                            elif current_item[1] == 90:
                                if y > 0 and y <= world_len - 1 and x >= 0 and x <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[x + ((y - 1) * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[x + ((y - 1) * world_len)]["tile"] == "leaves":
                                        world[x + ((y - 1) * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "smelter"
                                    world[x + ((y - 1) * world_len)]["building"] = "smelter"
                                    world[x + (y * world_len)]["inventory"] = [{},{}]
                                    world[x+ ((y-1) * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["recepie"] = -1
                                    world[x + (y * world_len)]["timer"] = -1
                                    world[x + (y * world_len)]["tick_timer"] = -1
                                    world[x + (y * world_len)]["rotation"] = 90
                                    world[x + ((y - 1) * world_len)]["rotation"] = 90
                                    world[x + (y * world_len)]["part"] = 1
                                    world[x + ((y - 1) * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                    built = True
                            elif current_item[1] == 180:
                                if x > 0 and x <= world_len - 1 and y >= 0 and y <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[(x - 1) + (y * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[(x - 1) + (y * world_len)]["tile"] == "leaves":
                                        world[(x - 1) + (y * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "smelter"
                                    world[(x - 1) + (y * world_len)]["building"] = "smelter"
                                    world[x + (y * world_len)]["inventory"] = [{},{}]
                                    world[(x - 1)+ (y * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["recepie"] = -1
                                    world[x + (y * world_len)]["timer"] = -1
                                    world[x + (y * world_len)]["tick_timer"] = 0
                                    world[x + (y * world_len)]["rotation"] = 180
                                    world[(x - 1) + (y * world_len)]["rotation"] = 180
                                    world[x + (y * world_len)]["part"] = 1
                                    world[(x - 1) + (y * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x - 1) + (y * world_len)]})
                                    built = True
                            elif current_item[1] == 270:
                                if y >= 0 and y < world_len - 1 and x >= 0 and x <= world_len - 1 and world[x + (y * world_len)]["building"] == None and world[x + ((y + 1) * world_len)]["building"] == None:
                                    if world[x + (y * world_len)]["tile"] == "leaves":
                                        world[x + (y * world_len)]["tile"] = "grass"
                                    if world[x + ((y + 1) * world_len)]["tile"] == "leaves":
                                        world[x + ((y + 1) * world_len)]["tile"] = "grass"
                                    world[x + (y * world_len)]["building"] = "smelter"
                                    world[x + ((y + 1) * world_len)]["building"] = "smelter"
                                    world[x + (y * world_len)]["inventory"] = [{},{}]
                                    world[x + ((y+1) * world_len)]["inventory"] = world[x + (y * world_len)]["inventory"]
                                    world[x + (y * world_len)]["recepie"] = -1
                                    world[x + (y * world_len)]["timer"] = -1
                                    world[x + (y * world_len)]["tick_timer"] = 0
                                    world[x + (y * world_len)]["rotation"] = 270
                                    world[x + ((y + 1) * world_len)]["rotation"] = 270
                                    world[x + (y * world_len)]["part"] = 1
                                    world[x + ((y + 1) * world_len)]["part"] = 2
                                    new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                    new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y + 1) * world_len)]})
                                    built = True
                        elif current_item[0] == "biomass_burner" and can_craft:
                            if world[x + (y * world_len)]["building"] == None:
                                if world[x + (y * world_len)]["tile"] == "leaves":
                                    world[x + (y * world_len)]["tile"] = "grass"
                                world[x + (y * world_len)]["building"] = "biomass_burner"
                                world[x + (y * world_len)]["inventory"] = {}
                                world[x + (y * world_len)]["timer"] = 0
                                world[x + (y * world_len)]["tick_timer"] = 0
                                world[x + (y * world_len)]["rotation"] = current_item[1]
                                world[x + (y * world_len)]["part"] = 1
                                new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                built = True
                        elif current_item[0] == "conveyor_belt_mk1" and can_craft:
                            if world[x + (y * world_len)]["building"] == None:
                                if world[x + (y * world_len)]["tile"] == "leaves":
                                    world[x + (y * world_len)]["tile"] = "grass"
                                world[x + (y * world_len)]["building"] = "conveyor_belt"
                                world[x + (y * world_len)]["inventory"] = {}
                                world[x + (y * world_len)]["rotation"] = current_item[1]
                                world[x + (y * world_len)]["part"] = 1
                                new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                built = True                            
                        elif current_item[0] == "disassemble":
                            if world[x + (y * world_len)]["building"] == "drill":
                                if world[x + (y * world_len)]["rotation"] == 0:
                                    destroyed = False
                                    if world[x + (y * world_len)]["part"] == 1:
                                        world[x + (y * world_len)]["building"] = None
                                        world[(x + 1) + (y * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[(x + 1) + (y * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[(x + 1) + (y * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                                        destroyed = True 
                                    else:
                                        world[x + (y * world_len)]["building"] = None
                                        world[(x - 1) + (y * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[(x - 1) + (y * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[(x - 1) + (y * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})       
                                        destroyed = True 
                                if world[x + (y * world_len)]["rotation"] == 90:
                                    if world[x + (y * world_len)]["part"] == 1:
                                        world[x + (y * world_len)]["building"] = None
                                        world[x + ((y - 1) * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[x + ((y - 1) * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[x + ((y - 1) * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                        destroyed = True 
                                    else:
                                        world[x + (y * world_len)]["building"] = None
                                        world[x + ((y + 1) * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[x + ((y + 1) * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[x + ((y + 1) * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})  
                                        destroyed = True 
                                if world[x + (y * world_len)]["rotation"] == 180:
                                    if world[x + (y * world_len)]["part"] == 2:
                                        world[x + (y * world_len)]["building"] = None
                                        world[(x + 1) + (y * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[(x + 1) + (y * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[(x + 1) + (y * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                                        destroyed = True 
                                    else:
                                        world[x + (y * world_len)]["building"] = None
                                        world[(x - 1) + (y * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[(x - 1) + (y * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[(x - 1) + (y * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})     
                                        destroyed = True 
                                if world[x + (y * world_len)]["rotation"] == 270:
                                    if world[x + (y * world_len)]["part"] == 2:
                                        world[x + (y * world_len)]["building"] = None
                                        world[x + ((y - 1) * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[x + ((y - 1) * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[x + ((y - 1) * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                        destroyed = True 
                                    else:
                                        world[x + (y * world_len)]["building"] = None
                                        world[x + ((y + 1) * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[x + ((y + 1) * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[x + ((y + 1) * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})  
                                        destroyed = True 
                                if destroyed:
                                    added = False
                                    for item_id, item in enumerate(inventory):
                                        if "item" in item and item["item"] ==  ("basic","drill") and item["amount"] < 200:
                                            inventory[item_id]["amount"] = inventory[item_id]["amount"] + 1
                                            added = True
                                            break
                                    if not(added):
                                        for item_id, item in enumerate(inventory):
                                            if item == {}:
                                                inventory[item_id] = {"item":("basic","drill"),"amount":1} 
                                                break                                                
                                    added = False
                                    for item_id, item in enumerate(inventory):
                                        if "item" in item and item["item"] ==  ("basic","wire") and item["amount"] < 200:
                                            inventory[item_id]["amount"] = inventory[item_id]["amount"] + 5
                                            added = True
                                            break
                                    if not(added):
                                        for item_id, item in enumerate(inventory):
                                            if item == {}:
                                                inventory[item_id] = {"item":("basic","wire"),"amount":5}
                                                break                                                
                                    added = False
                                    for item_id, item in enumerate(inventory):
                                        if "item" in item and item["item"] ==  ("basic","plate") and item["amount"] < 200:
                                            inventory[item_id]["amount"] = inventory[item_id]["amount"] + 3
                                            added = True
                                            break
                                    if not(added):
                                        for item_id, item in enumerate(inventory):
                                            if item == {}:
                                                inventory[item_id] = {"item":("basic","plate"),"amount":3}  
                                                break 
                            elif world[x + (y * world_len)]["building"] == "smelter":
                                if world[x + (y * world_len)]["rotation"] == 0:
                                    destroyed = False
                                    if world[x + (y * world_len)]["part"] == 1:
                                        world[x + (y * world_len)]["building"] = None
                                        world[(x + 1) + (y * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[(x + 1) + (y * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[(x + 1) + (y * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                                        destroyed = True 
                                    else:
                                        world[x + (y * world_len)]["building"] = None
                                        world[(x - 1) + (y * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[(x - 1) + (y * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[(x - 1) + (y * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})       
                                        destroyed = True 
                                if world[x + (y * world_len)]["rotation"] == 90:
                                    if world[x + (y * world_len)]["part"] == 1:
                                        world[x + (y * world_len)]["building"] = None
                                        world[x + ((y - 1) * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[x + ((y - 1) * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[x + ((y - 1) * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                        destroyed = True 
                                    else:
                                        world[x + (y * world_len)]["building"] = None
                                        world[x + ((y + 1) * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[x + ((y + 1) * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[x + ((y + 1) * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})  
                                        destroyed = True 
                                if world[x + (y * world_len)]["rotation"] == 180:
                                    if world[x + (y * world_len)]["part"] == 2:
                                        world[x + (y * world_len)]["building"] = None
                                        world[(x + 1) + (y * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[(x + 1) + (y * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[(x + 1) + (y * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                                        destroyed = True 
                                    else:
                                        world[x + (y * world_len)]["building"] = None
                                        world[(x - 1) + (y * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[(x - 1) + (y * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[(x - 1) + (y * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})     
                                        destroyed = True 
                                if world[x + (y * world_len)]["rotation"] == 270:
                                    if world[x + (y * world_len)]["part"] == 2:
                                        world[x + (y * world_len)]["building"] = None
                                        world[x + ((y - 1) * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[x + ((y - 1) * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[x + ((y - 1) * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                        destroyed = True 
                                    else:
                                        world[x + (y * world_len)]["building"] = None
                                        world[x + ((y + 1) * world_len)]["building"] = None
                                        world[x + (y * world_len)]["rotation"] = 0
                                        world[x + ((y + 1) * world_len)]["rotation"] = 0
                                        world[x + (y * world_len)]["part"] = 0
                                        world[x + ((y + 1) * world_len)]["part"] = 0
                                        new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                        new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})  
                                        destroyed = True 
                                if destroyed:
                                    added = False
                                    for item_id, item in enumerate(inventory):
                                        if "item" in item and item["item"] ==  ("basic","plate") and item["amount"] < 200:
                                            inventory[item_id]["amount"] = inventory[item_id]["amount"] + 2
                                            added = True
                                            break
                                    if not(added):
                                        for item_id, item in enumerate(inventory):
                                            if item == {}:
                                                inventory[item_id] = {"item":("basic","plate"),"amount":2} 
                                                break
                                    added = False
                                    for item_id, item in enumerate(inventory):
                                        if "item" in item and item["item"] ==  ("basic","wire") and item["amount"] < 200:
                                            inventory[item_id]["amount"] = inventory[item_id]["amount"] + 10
                                            added = True
                                            break
                                    if not(added):
                                        for item_id, item in enumerate(inventory):
                                            if item == {}:
                                                inventory[item_id] = {"item":("basic","wire"),"amount":10}
                                                break
                                    added = False
                                    for item_id, item in enumerate(inventory):
                                        if "item" in item and item["item"] ==  ("basic","rod") and item["amount"] < 200:
                                            inventory[item_id]["amount"] = inventory[item_id]["amount"] + 5
                                            added = True
                                            break
                                    if not(added):
                                        for item_id, item in enumerate(inventory):
                                            if item == {}:
                                                inventory[item_id] = {"item":("basic","rod"),"amount":3}   
                                                break
                            elif world[x + (y * world_len)]["building"] == "storage_container":
                                for item_id, item in enumerate(world[x + (y * world_len)]["inventory"]):
                                    for item_id_inv, item_inv in enumerate(inventory):
                                        if item != {} and item_inv == {}:
                                            inventory[item_id_inv] = item.copy()
                                            world[x + (y * world_len)]["inventory"][item_id] = {}
                                            break
                                        elif item != {} and item_inv["item"] == item["item"] and item_inv["amount"] <200:
                                            inventory[item_id_inv]["amount"] += item["amount"]
                                            world[x + (y * world_len)]["inventory"][item_id] = {}
                                            break
                                if world[x + (y * world_len)]["inventory"] == [{},{},{},{},{},{},{},{},{},{}]:
                                    if world[x + (y * world_len)]["rotation"] == 0:
                                        destroyed = False
                                        if world[x + (y * world_len)]["part"] == 1:
                                            world[x + (y * world_len)]["building"] = None
                                            world[(x + 1) + (y * world_len)]["building"] = None
                                            world[x + (y * world_len)]["rotation"] = 0
                                            world[(x + 1) + (y * world_len)]["rotation"] = 0
                                            world[x + (y * world_len)]["part"] = 0
                                            world[(x + 1) + (y * world_len)]["part"] = 0
                                            new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                            new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                                            destroyed = True 
                                        else:
                                            world[x + (y * world_len)]["building"] = None
                                            world[(x - 1) + (y * world_len)]["building"] = None
                                            world[x + (y * world_len)]["rotation"] = 0
                                            world[(x - 1) + (y * world_len)]["rotation"] = 0
                                            world[x + (y * world_len)]["part"] = 0
                                            world[(x - 1) + (y * world_len)]["part"] = 0
                                            new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                            new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})       
                                            destroyed = True 
                                    if world[x + (y * world_len)]["rotation"] == 90:
                                        if world[x + (y * world_len)]["part"] == 1:
                                            world[x + (y * world_len)]["building"] = None
                                            world[x + ((y - 1) * world_len)]["building"] = None
                                            world[x + (y * world_len)]["rotation"] = 0
                                            world[x + ((y - 1) * world_len)]["rotation"] = 0
                                            world[x + (y * world_len)]["part"] = 0
                                            world[x + ((y - 1) * world_len)]["part"] = 0
                                            new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                            new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                            destroyed = True 
                                        else:
                                            world[x + (y * world_len)]["building"] = None
                                            world[x + ((y + 1) * world_len)]["building"] = None
                                            world[x + (y * world_len)]["rotation"] = 0
                                            world[x + ((y + 1) * world_len)]["rotation"] = 0
                                            world[x + (y * world_len)]["part"] = 0
                                            world[x + ((y + 1) * world_len)]["part"] = 0
                                            new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                            new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})  
                                            destroyed = True 
                                    if world[x + (y * world_len)]["rotation"] == 180:
                                        if world[x + (y * world_len)]["part"] == 2:
                                            world[x + (y * world_len)]["building"] = None
                                            world[(x + 1) + (y * world_len)]["building"] = None
                                            world[x + (y * world_len)]["rotation"] = 0
                                            world[(x + 1) + (y * world_len)]["rotation"] = 0
                                            world[x + (y * world_len)]["part"] = 0
                                            world[(x + 1) + (y * world_len)]["part"] = 0
                                            new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                            new_blocks.append({"id": (x + 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})
                                            destroyed = True 
                                        else:
                                            world[x + (y * world_len)]["building"] = None
                                            world[(x - 1) + (y * world_len)]["building"] = None
                                            world[x + (y * world_len)]["rotation"] = 0
                                            world[(x - 1) + (y * world_len)]["rotation"] = 0
                                            world[x + (y * world_len)]["part"] = 0
                                            world[(x - 1) + (y * world_len)]["part"] = 0
                                            new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                            new_blocks.append({"id": (x - 1) + (y * world_len), "tile": world[(x + 1) + (y * world_len)]})     
                                            destroyed = True 
                                    if world[x + (y * world_len)]["rotation"] == 270:
                                        if world[x + (y * world_len)]["part"] == 2:
                                            world[x + (y * world_len)]["building"] = None
                                            world[x + ((y - 1) * world_len)]["building"] = None
                                            world[x + (y * world_len)]["rotation"] = 0
                                            world[x + ((y - 1) * world_len)]["rotation"] = 0
                                            world[x + (y * world_len)]["part"] = 0
                                            world[x + ((y - 1) * world_len)]["part"] = 0
                                            new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                            new_blocks.append({"id": x + ((y - 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})
                                            destroyed = True 
                                        else:
                                            world[x + (y * world_len)]["building"] = None
                                            world[x + ((y + 1) * world_len)]["building"] = None
                                            world[x + (y * world_len)]["rotation"] = 0
                                            world[x + ((y + 1) * world_len)]["rotation"] = 0
                                            world[x + (y * world_len)]["part"] = 0
                                            world[x + ((y + 1) * world_len)]["part"] = 0
                                            new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                            new_blocks.append({"id": x + ((y + 1) * world_len), "tile": world[x + ((y - 1) * world_len)]})  
                                            destroyed = True 
                                    if destroyed:
                                        added = False
                                        for item_id, item in enumerate(inventory):
                                            if "item" in item and item["item"] ==  ("basic","plate") and item["amount"] < 200:
                                                inventory[item_id]["amount"] = inventory[item_id]["amount"] + 5
                                                added = True
                                                break
                                        if not(added):
                                            for item_id, item in enumerate(inventory):
                                                if item == {}:
                                                    inventory[item_id] = {"item":("basic","plate"),"amount":5} 
                                                    break
                                        added = False
                                        for item_id, item in enumerate(inventory):
                                            if "item" in item and item["item"] ==  ("basic","rod") and item["amount"] < 200:
                                                inventory[item_id]["amount"] = inventory[item_id]["amount"] + 2
                                                added = True
                                                break
                                        if not(added):
                                            for item_id, item in enumerate(inventory):
                                                if item == {}:
                                                    inventory[item_id] = {"item":("basic","rod"),"amount":2}   
                                                    break
                            elif world[x + (y * world_len)]["building"] == "biomass_burner":
                                world[x + (y * world_len)]["building"] = None
                                world[x + (y * world_len)]["rotation"] = 0
                                world[x + (y * world_len)]["part"] = 0
                                new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                added = False
                                for item_id, item in enumerate(inventory):
                                    if "item" in item and item["item"] ==  ("basic","wire") and item["amount"] < 200:
                                        inventory[item_id]["amount"] = inventory[item_id]["amount"] + 10
                                        added = True
                                        break
                                if not(added):
                                    for item_id, item in enumerate(inventory):
                                        if item == {}:
                                            inventory[item_id] = {"item":("basic","wire"),"amount":10}
                                            break
                                added = False
                                for item_id, item in enumerate(inventory):
                                    if "item" in item and item["item"] ==  ("basic","plate") and item["amount"] < 200:
                                        inventory[item_id]["amount"] = inventory[item_id]["amount"] + 5
                                        added = True
                                if not(added):
                                    for item_id, item in inventory:
                                        if item == {}:
                                            inventory[item_id] = {"item":("basic","plate"),"amount":5}
                                if world[x + (y * world_len)]["inventory"] != {}:
                                    for item_id, item in enumerate(inventory):
                                        if "item" in item and item["item"] ==  world[x + (y * world_len)]["inventory"]["item"] and item["amount"] < 200:
                                            inventory[item_id]["amount"] = inventory[item_id]["amount"] + world[x + (y * world_len)]["inventory"]["amount"]
                                            added = True
                                    if not(added):
                                        for item_id, item in inventory:
                                            if item == {}:
                                                inventory[item_id] = world[x + (y * world_len)]["inventory"]                                
                            elif world[x + (y * world_len)]["building"] == "conveyor_belt":
                                world[x + (y * world_len)]["building"] = None
                                world[x + (y * world_len)]["rotation"] = 0
                                world[x + (y * world_len)]["part"] = 0
                                new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})
                                added = False
                                for item_id, item in enumerate(inventory):
                                    if "item" in item and item["item"] ==  ("basic","wire") and item["amount"] < 200:
                                        inventory[item_id]["amount"] = inventory[item_id]["amount"] + 10
                                        added = True
                                        break
                                if not(added):
                                    for item_id, item in enumerate(inventory):
                                        if item == {}:
                                            inventory[item_id] = {"item":("basic","plate"),"amount":1}
                                            break
                                            
                        if built:
                            can_craft = False
                            added = False
                            item_ids = []
                            ids_to_pop = []
                            for item in current_item[3]:
                                for inv_item_id, inv_item in enumerate(inventory):
                                    can_craft = False
                                    if inv_item != {} and item[0] == inv_item["item"] and item[1] <= inv_item["amount"]:
                                        can_craft = True
                                        item_ids.append((inv_item_id,item[1]))
                                        break
                                if can_craft == False:  
                                    break
                            if can_craft:
                                for i, item_id in enumerate(item_ids):
                                    item = current_item[3][i]
                                    if item[1] < inventory[item_id[0]]["amount"]:
                                        inventory[item_id[0]]["amount"] -= item[1]
                                    else:
                                        ids_to_pop.append(item_id[0])
                                for id_to_pop in reversed(sorted(ids_to_pop)):
                                    inventory[id_to_pop] = {}
                                added = True                               
                            
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
            if keys[pg.K_e] and menu == "hidden" and inventory_tile == "" and dialogue[0] == []:
                menu = "opening"
                menu_tick = 10
            elif keys[pg.K_e] and menu == "open" and inventory_tile == "" and dialogue[0] == []:
                menu = "closing"
                menu_tick = 10
                cursor_tile_id = -1
            elif keys[pg.K_e] and inventory_tile != "" and dialogue[0] == []:
                inventory_tile = ""
                menu = "closing"
                menu_tick = 10   
                cursor_tile_id = -1
            elif keys[pg.K_RETURN] and dialogue[0] != [] and not("choice" in dialogue[0][dialogue[1]]):
                if len(dialogue[0]) != dialogue[1]+1: 
                    dialogue[1] += 1
                else: 
                    dialogue[0] = []
                    dialogue[1] = 0

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
                if mode == "!building" and not(chat_open) and menu=="hidden":
                    added = False
                    if world[x + y * world_len]["building"] == "biomass_burner" or world[x + y * world_len]["building"] == "smelter" or world[x + y * world_len]["building"] == "drill" or world[x + y * world_len]["building"] == "storage_container":
                        inventory_tile =x + (y * world_len)
                        menu = "opening"
                        menu_tick = 10                         
                    elif world[x + y * world_len]["tile"] == "iron_ore":
                        for item_id, item in enumerate(inventory):
                            if "item" in item and item["item"] == ("unprocessed", "iron") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 15
                                player_state = "dig_active"
                                break
                        if not(added):
                            for item_id, item in enumerate(inventory):
                                if item == {}:
                                    inventory[item_id] ={"item": ("unprocessed", "iron"), "amount": 1, "info": ("Iron ore", "Iron, waiting to be", "melted. Can be transf-", "ormed to iron ingot.", "")}
                                    break
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "copper_ore":
                        for item_id, item in enumerate(inventory):
                            if "item" in item and item["item"] == ("unprocessed", "copper") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 5
                                player_state = "dig_active"
                                break
                        if not(added):
                            for item_id, item in enumerate(inventory):
                                if item == {}:
                                    inventory[item_id] ={"item": ("unprocessed", "copper"), "amount": 1, "info": ("Copper ore", "Copper, waiting to be", "melted. Can be transf-", "ormed to copper ingot.", "")}
                                    break
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "tungsten_ore":
                        for item_id, item in enumerate(inventory):
                            if "item" in item and item["item"] == ("unprocessed", "tungsten") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 5
                                player_state = "dig_active"
                                break
                        if not(added):
                            for item_id, item in enumerate(inventory):
                                if item == {}:
                                    inventory[item_id] =                            {"item": ("unprocessed", "tungsten"), "amount": 1, "info": ("Raw tungsten", "Raw metal that can glow.", "", "", "")}
                                    break                                    
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "coal_ore":
                        for item_id, item in enumerate(inventory):
                            if "item" in item and item["item"] == ("unprocessed", "coal") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 5
                                player_state = "dig_active"
                                break
                        if not(added):
                            for item_id, item in enumerate(inventory):
                                if item == {}:
                                    inventory[item_id] =                             {"item": ("unprocessed", "coal"), "amount": 1, "info": ("Coal", "Natural material.", "Good for making steel.", "", "")}
                                    break
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "resin_ore":
                        for item_id, item in enumerate(inventory):
                            if "item" in item and item["item"] == ("unprocessed", "resin") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 5
                                player_state = "dig_active"
                                break
                        if not(added):
                            for item_id, item in enumerate(inventory):
                                if item == {}:
                                    inventory[item_id] =      {"item": ("unprocessed", "resin"), "amount": 1, "info": ("Raw resin", "Natural material.", "Good for isolatin","wires.", "")}
                                    break
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "uranium_ore":
                        for item_id, item in enumerate(inventory):
                            if "item" in item and item["item"] == ("unprocessed", "uranium") and item["amount"] < 200:
                                inventory[item_id]["amount"] += 1
                                added = True
                                player_state_timer = 5
                                player_state = "dig_active"
                                break
                        if not(added):
                            for item_id, item in enumerate(inventory):
                                if item == {}:
                                    inventory[item_id] = {"item": ("unprocessed", "uranium"), "amount": 1}
    
                                    break                                    
                            player_state_timer = 5
                            player_state = "dig_active"
                    elif world[x + y * world_len]["tile"] == "leaves":
                        for item_id, item in enumerate(inventory):
                            if "item" in item and item["item"] == ("bio", "leaves") and item["amount"] < 500:
                                inventory[item_id]["amount"] += 1
                                added = True
                                world[x + y * world_len]["tile"] = "grass"
                                temp_new_blocks.append({"id": x + (y * world_len), "tile": world[x + (y * world_len)]})                                
                                player_state_timer = 5
                                player_state = "dig_active" 
                                break
                        if not(added) and len(inventory):
                            for item_id, item in enumerate(inventory):
                                if item == {}:
                                    inventory[item_id] ={"item": ("bio", "leaves"), "amount": 1, "info": ("Leaves", "Natural material, but", "has a little radiation in", "it. Can be transformed", "to Biofiber")}
                                    break
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
                            if inventory[x + y * 9] != {}:
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
                                    text_tooltip2 = dosfont.render(item["info"][5], True, (0, 0, 0))
                                    window.blit(text_tooltip2, (cursor_pos[0] + cell_size * 1.2, cursor_pos[1] + cell_size * 2.6))                                
                                except:pass
                        except:pass
        pg.display.update()
        clock.tick(45)
        tick += 1
        #print(new_blocks,len(new_blocks))
    elif game_mode == "title":
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif evt.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] >= cell_size * 4 and mouse_pos[0] <= cell_size * 8:
                    if mouse_pos[1] >= cell_size * 12 and mouse_pos[1] <= cell_size * 12.5:
                        game_mode = "singleplayer_setup"
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
                    elif mouse_pos[1] >= cell_size * 10 and mouse_pos[1] <= cell_size * 10.5:
                        selected = 2
                    elif mouse_pos[1] >= cell_size * 16 and mouse_pos[1] <= cell_size * 16.5:
                        selected = 3                    
            elif evt.type == pg.KEYDOWN:
                if evt.key == pg.K_RETURN:
                    port = int(port) if port.isdigit() and int(port) < 65535 and int(port) > 0 else 8000
                    clientSocket = socket.socket()

                    try:
                        if player_type.lower() != "alphen" or player_type.lower() != "fury" or player_type.lower() != "a" or player_type.lower() != "f":
                            player_type = random.choice(["alphen","fury"])
                        else:
                            if player_type.lower() == "a":
                                player_type = "alphen"
                            elif player_type.lower() == "f":
                                player_type = "fury"
                            player_type = player_type.lower()
                            
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
                    except:
                        game_mode = "error"
                        splash = ["Error","Failed to connect, check IP and port"]
                        break
                    chat = []
                    def socketThread():
                        global clientSocket, running_thread, users, pos, world, new_blocks, starting_blocks, temp_new_blocks,chat, recent_messages, send, current_message,game_mode,splash,power_down,power_capacity,power_capacity_current,power_max,power_usage,clockA

                        while running_thread:
                            try:
                                if send:
                                    data = {"nickname": nick, "self": [pos,player_state,facing,player_type], "new_blocks": new_blocks, "temp_new_blocks":temp_new_blocks,"msg":current_message,"power_down":power_down}
                                    send = False
                                    current_message = ""
                                else:
                                    data = {"nickname": nick, "self": [pos,player_state,facing,player_type], "new_blocks": new_blocks, "temp_new_blocks":temp_new_blocks,"msg":"","power_down":power_down}
                                #print(data)
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
                                if received_new_blocks != new_blocks:
                                    for block in received_new_blocks:
                                        if not block in new_blocks:
                                            new_blocks.append(block)
                                            world[block["id"]] = block["tile"]  
                                received_temp_new_blocks = received["temp_new_blocks"]
                                power_down = received["power"][0]
                                power_capacity = received["power"][1]
                                power_capacity_current = received["power"][2]
                                power_max = received["power"][3]
                                power_usage = received["power"][4]
                                if chat != received["chat"]:
                                    #sounds["msg"].play()
                                    recent_messages = [{"user":x["user"],"text":x["text"],"timer":90} for x in received["chat"] if x not in chat]
                                    chat = received["chat"]
                                
                                        
                                for block in received_temp_new_blocks:
                                    world[block["id"]] = block["tile"]
                            except:
                                running_thread = False
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
                    elif selected == 3:
                        player_type = player_type[:-1]                    
                else:
                    if selected == 0 and len(port) < 5:
                        port += evt.unicode
                    elif selected == 1 and len(ip) < 14:
                        ip += evt.unicode
                    elif selected == 2 and len(nick) < 15:
                        nick += evt.unicode
                    elif selected == 3 and len(player_type) < 6:
                        player_type += evt.unicode                    
        draw_multiplayer(window, port, ip, nick)
        cursor_pos = pg.mouse.get_pos()
        window.blit(pg.transform.scale(ui["cursor"], (cell_size * 2, cell_size * 2)), cursor_pos)
        pg.display.update()
        tick += 1
    elif game_mode == "singleplayer_setup":
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                pg.quit()
                sys.exit()                 
            elif evt.type == pg.KEYDOWN:
                if evt.key == pg.K_RETURN:
                    if player_type.lower() != "alphen" and player_type.lower() != "fury" and player_type.lower() != "a" and player_type.lower() != "f":
                        player_type = random.choice(["alphen","fury"])
                    else:
                        if player_type.lower() == "a":
                            player_type = "alphen"
                        elif player_type.lower() == "f":
                            player_type = "fury"
                        else:
                            player_type = player_type.lower() 
                    game_mode = "singleplayer"
                elif evt.key == pg.K_BACKSPACE:
                    player_type = player_type[:-1]                    
                else:
                    player_type += evt.unicode   
                    player_type = player_type.lower()
        draw_singleplayer(window)
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

    if text_cycle == len(RUNNING_TEXT+"  ")*13:
        text_cycle = 0
    text_running = dosfontbig.render((RUNNING_TEXT+" ")*40,True,(255,0,0))
    window.blit(text_running,(0-text_cycle,10))
    text_cycle+=1 
    text_version = dosfontbig.render("Version "+str(VERSION),True,(255,0,0))
    window.blit(text_version,(0,cell_size*20-24))
    pg.display.update()
