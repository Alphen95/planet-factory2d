import pygame as pg
import sys, random, os, datetime
from pprint import pprint

os.makedirs("logs",exist_ok=True)
log_file = open(os.path.join("logs","log-{}.txt".format(str(datetime.datetime.now())[:-7])),"w+")
log_file.write("[INFO] program started, time: {}\n".format(str(datetime.datetime.now())[:-7]))

ores = [
    pg.image.load(os.path.join("res","ore_iron.png")),
    pg.image.load(os.path.join("res","ore_copper.png")),
    pg.image.load(os.path.join("res","ore_zinc.png")),
    pg.image.load(os.path.join("res","ore_tin.png")),
    pg.image.load(os.path.join("res","ore_kelp.png")), 
    pg.image.load(os.path.join("res","ore_coal.png"))
]

ui = [
    pg.image.load(os.path.join("res","tooltip_box.png"))
]

buildings = {
    "drill":[
        pg.image.load(os.path.join("res","drill_part1.png")),
        pg.image.load(os.path.join("res","drill_part2.png"))
    ],
    "conveyor":[
        pg.image.load(os.path.join("res","conveyor_belt0.png")) ,
        pg.image.load(os.path.join("res","conveyor_belt1.png")) , 
        pg.image.load(os.path.join("res","conveyor_belt2.png")) ,
        pg.image.load(os.path.join("res","conveyor_belt3.png")) 
    ]
}

ground_tiles = [
    pg.image.load(os.path.join("res","stone.png")),
    pg.image.load(os.path.join("res","water.png"))
]

tick = 0
tooltip_tick = -1
tooltip_tile = {}
menu = "hidden"
menu_tick = 0
current_item = [None,0]
mode = None

screen_size = (600,600)

window = pg.display.set_mode(screen_size)
clock = pg.time.Clock()
pg.init()
font = pg.font.SysFont("Verdana",12)
pos = [0,0]

#world define
world = []
for i in range(0,1600):
    world.append({"item":None,"building":None, "tile":None,"part":0,"rotation":0})

for i in range(0, 18):
    x = random.randint(0,39)
    y = random.randint(0,39)    
    if i == 0 or i == 1 or i == 6 or i == 7 or i == 12 or i == 13:
        world[x+(y*40)] = {"item":None,"building":None,"tile":"coal_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed coal ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 2 or i == 8 or i == 14:
        world[x+(y*40)] = {"item":None,"building":None,"tile":"iron_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed iron ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 3 or i == 9 or i == 15:
        world[x+(y*40)] = {"item":None,"building":None,"tile":"copper_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed copper ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 4 or i == 10 or i == 16:
        world[x+(y*40)] = {"item":None,"building":None,"tile":"tin_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed tin ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 5 or i == 11 or i == 17:
        world[x+(y*40)] = {"item":None,"building":None,"tile":"zinc_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed zinc ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
x = random.randint(0,37)
y = random.randint(0,37)
for i in range(0,3):
    for i1 in range(0,3):
        world[(x+i)+((y+i1)*40)] = {"item":None,"building":None,"tile":"water","part":0,"rotation":0}
        if i==1 and i1 ==1:
            world[(x+i)+((y+i1)*40)] = {"item":None,"building":None,"tile":"kelp","part":0,"rotation":0}

world[0] = {"item":None,"building":"drill","tile":"coal_ore","part":1,"rotation":0}
world[1] = {"item":None,"building":"drill","tile":None,"part":2,"rotation":0}
world[2] = {"item":None,"building":"conveyor_belt","tile":None,"part":0,"rotation":0}

def draw_world(world,winobj,tick, pos,tooltip_props, menu_props):
    winobj.fill((25,25,25))
    x = 0
    x1 = 0
    y = 0
    y1 = 0
    x_borders = [pos[0]-10,pos[0]+10]
    y_borders = [pos[1]-10,pos[1]+10]
    for tile_id, tile in enumerate(world):
        if x == 40:
            x = 0
            y+=1
        if y >= y_borders[0] and y <= y_borders[1] and x >= x_borders[0] and x<= x_borders[1]:
            block = tile["tile"]
            block_rotation = tile["rotation"]
            block_part = tile["part"]
            block_building = tile["building"]
            x1 = x
            y1 = y
            if x_borders[0] < 0: x1 += abs(x_borders[0])
            else: x1 -= x_borders[0]
            if y_borders[0] < 0: y1 += abs(y_borders[0])
            else: y1 -= y_borders[0]
            winobj.blit(pg.transform.scale(ground_tiles[0],(30,30)),(x1*30,y1*30))
            if block == "coal_ore":
                winobj.blit(pg.transform.scale(ores[-1],(30,30)),(x1*30,y1*30))
            elif block == "iron_ore":
                winobj.blit(pg.transform.scale(ores[0],(30,30)),(x1*30,y1*30))
            elif block == "copper_ore":
                winobj.blit(pg.transform.scale(ores[1],(30,30)),(x1*30,y1*30))
            elif block == "zinc_ore":
                winobj.blit(pg.transform.scale(ores[2],(30,30)),(x1*30,y1*30))
            elif block == "tin_ore":
                winobj.blit(pg.transform.scale(ores[3],(30,30)),(x1*30,y1*30))
            elif block == "kelp":
                winobj.blit(pg.transform.scale(ores[4],(30,30)),(x1*30,y1*30))  
            elif block == "water":
                winobj.blit(pg.transform.scale(ground_tiles[1],(30,30)),(x1*30,y1*30))              
            if block_building == "drill":
                if block_part == 1:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][0],block_rotation),(30,30)),(x1*30,y1*30))
                elif block_part == 2:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][1],block_rotation),(30,30)),(x1*30,y1*30))
            elif block_building == "conveyor_belt":
                if tick <= 11:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0],block_rotation),(30,30)),(x1*30,y1*30))
                elif tick <= 22:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1],block_rotation),(30,30)),(x1*30,y1*30))
                elif tick <= 33:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2],block_rotation),(30,30)),(x1*30,y1*30))
                elif tick <= 44:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][3],block_rotation),(30,30)),(x1*30,y1*30))
        x+=1
    if tooltip_props[0] != -1 and tooltip_props[1] != {}:
        block = tooltip_props[1]["tile"]
        block_rotation = tooltip_props[1]["rotation"]
        block_part =tooltip_props[1]["part"]
        block_building =tooltip_props[1]["building"]
        block_item =tooltip_props[1]["item"]
        ypos = 0
        xpos = 6*30
        if tooltip_props[0] >= 104:
            ypos = 3*(104-tooltip_props[0])
        if tooltip_props[0] <= 20:
            ypos = -60+tooltip_props[0]*3
        winobj.blit(pg.transform.scale(pg.transform.rotate(ui[0],0),(190,60)),(xpos+10,ypos))
        text_tile = font.render("Tile:{}".format(block),True,(0,0,0))
        text_build = font.render("Building:{}".format(block_building),True,(0,0,0))
        text_item = font.render("Item:{}".format(block_item),True,(0,0,0))
        winobj.blit(text_tile,(xpos+55,ypos+5))
        winobj.blit(text_build,(xpos+55,ypos+17))
        winobj.blit(text_item,(xpos+55,ypos+30))
        if block == "coal_ore":
            winobj.blit(pg.transform.scale(ores[-1],(30,30)),(xpos+20,ypos+10))
        elif block == "iron_ore":
            winobj.blit(pg.transform.scale(ores[0],(30,30)),(xpos+20,ypos+10))
        elif block == "copper_ore":
            winobj.blit(pg.transform.scale(ores[1],(30,30)),(xpos+20,ypos+10))
        elif block == "zinc_ore":
            winobj.blit(pg.transform.scale(ores[2],(30,30)),(xpos+20,ypos+10))
        elif block == "tin_ore":
            winobj.blit(pg.transform.scale(ores[3],(30,30)),(xpos+20,ypos+10))
        if block_building == "drill":
            if block_part == 1:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][0],block_rotation),(30,30)),(xpos+20,ypos+10))
            elif block_part == 2:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][1],block_rotation),(30,30)),(xpos+20,ypos+10))
        elif block_building == "conveyor_belt":
            if tick <= 11:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0],block_rotation),(30,30)),(xpos+20,ypos+10))
            elif tick <= 22:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1],block_rotation),(30,30)),(xpos+20,ypos+10))
            elif tick <= 33:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2],block_rotation),(30,30)),(xpos+20,ypos+10))
            elif tick <= 44:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][3],block_rotation),(30,30)),(xpos+20,ypos+10)) 
    if menu_props[1] != "hidden":
        ypos = 0
        xpos = 570
        if menu_props[1] == "opening" or menu_props[1] == "open":
            xpos += menu_props[0]
        elif menu_props[1] == "closing" or menu_props[1] == "hidden":
            xpos += 30-menu_props[0]
        winobj.blit(pg.transform.scale(pg.transform.rotate(ui[0],270),(30,600)),(xpos,ypos))
        

#main cycle
while 1:
    if tick == 45:
        tick = 0
    if tooltip_tick != -1:
        tooltip_tick -= 1
    if menu_tick != 0:
        menu_tick -= 1
    if tooltip_tick == -1:
        tooltip_tile = {}
    if menu_tick == 0 and menu == "closing":
        menu = "hidden"
    if menu_tick == 0 and menu == "opening":
        menu = "open"
    draw_world(world,window,tick,pos,[tooltip_tick,tooltip_tile],[menu_tick,menu])
    for evt in pg.event.get():
        if evt.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif evt.type == pg.MOUSEBUTTONDOWN:
            coords = evt.pos
            #tooltip on middle-click
            #build on right-click
            x = int(coords[1]/30)
            y = int(coords[0]/30)
            x2= 0
            y2= 0
            x_borders = [pos[0]-10,pos[0]+10]
            y_borders = [pos[1]-10,pos[1]+10]
            visible_part = {}
            for x1 in range(x_borders[0],x_borders[1]):
                for y1 in range(y_borders[0],y_borders[1]):
                    visible_part[str(x1)+"_"+str(y1)] = {}
            for i in range(0,1600):
                if x2 == 40:
                    x2 = 0
                    y2 += 1
                if x2 >= x_borders[0] and x2 <= x_borders[1] and y2 >= y_borders[0] and y2 <= y_borders[1]:
                    visible_part[str(x2)+"_"+str(y2)] = world[i]
                x2 += 1
            true_visible_part = []
            for x1 in range(x_borders[0],x_borders[1]):
                for y1 in range(y_borders[0],y_borders[1]):
                    true_visible_part.append(visible_part[str(x1)+"_"+str(y1)])
            if evt.button == 0:
                if mode == "building":
                    if current_item[0] == "drill":
                        if current_item[1] == 0:
                            if x > 0 and x < 39  and y >= 0 and y <= 39:
                                world[x+(y*40)]["building"] = "drill"
                                world[(x+1)+(y*40)]["building"] = "drill"
                                world[x+(y*40)]["rotation"]= 90
                                world[(x+1)+(y*40)]["rotation"]= 90
                                world[x+(y*40)]["part"]=1
                                world[(x+1)+(y*40)]["part"]=2                        
                        elif current_item[1] == 90:
                            if y > 0 and y < 39  and x >= 0 and x <= 39:
                                world[x+(y*40)]["building"] = "drill"
                                world[x+((y+1)*40)]["building"] = "drill"
                                world[x+(y*40)]["rotation"]= 90
                                world[x+((y+1)*40)]["rotation"]= 90
                                world[x+(y*40)]["part"]=1
                                world[x+((y+1)*40)]["part"]=2
                
            if evt.button == 2:
                tooltip_tile = true_visible_part[x+y*20]
                tooltip_tick = 125                    
        elif evt.type == pg.KEYDOWN:
            if evt.key == pg.K_UP and pos[1] != 0:
                pos[1] -= 1
            elif evt.key == pg.K_DOWN and pos[1] != 40:
                pos[1] += 1
            elif evt.key == pg.K_LEFT and pos[0] != 0:
                pos[0] -= 1
            elif evt.key == pg.K_RIGHT and pos[0] != 40:
                pos[0] += 1
    coords = pg.mouse.get_pos()
    if coords[0] >= 585 and menu == "hidden":
        menu = "opening"
        menu_tick = 30
    elif coords[0] <= 570 and menu == "open":
        menu = "closing"
        menu_tick = 30
    pg.display.update()
    clock.tick(45)
    tick += 1