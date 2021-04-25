import pygame as pg
import sys, random, os, datetime, argparse
from pprint import pprint

os.makedirs("logs",exist_ok=True)
log_file = open(os.path.join("logs","log-{}.txt".format(str(datetime.datetime.now())[:-7])),"w+")
log_file.write("[INFO] program started, time: {}\n".format(str(datetime.datetime.now())[:-7]))
parser = argparse.ArgumentParser(description='Satisfactorey denmake on Python. These options are fully extra.')
parser.add_argument("--size",type=int,help="Changes the field size (default = 40). WARNING: Larger sizes make the world generate longer.")
parser.add_argument("--cell",type=int,help="Changes the cell size (default = 30).")

ores = [
    pg.image.load(os.path.join("res","ore_iron.png")),
    pg.image.load(os.path.join("res","ore_copper.png")),
    pg.image.load(os.path.join("res","ore_zinc.png")),
    pg.image.load(os.path.join("res","ore_tin.png")),
    pg.image.load(os.path.join("res","ore_kelp.png")), 
    pg.image.load(os.path.join("res","leaves.png")),
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
    pg.image.load(os.path.join("res","water.png")),
    pg.image.load(os.path.join("res","grass.png"))
]

tick = 0
tooltip_tick = -1
tooltip_tile = {}
menu = "hidden"
menu_tick = 0
current_item = ["drill",90]
mode = "building"

args = parser.parse_args()
if args.size != None: cell_size = args.size
else: cell_size = 40
screen_size = (cell_size*20,cell_size*20)
if args.cell != None: world_len = args.cell
else:world_len = 40


window = pg.display.set_mode(screen_size)
clock = pg.time.Clock()
pg.init()
font = pg.font.SysFont("Verdana",12)
dosfont = pg.font.Font(os.path.join("res","dosfont.ttf"),12)
pos = [0,0]
menubar = []

#world define
world = []
for i in range(0,world_len*world_len):
    world.append({"item":None,"building":None, "tile":"stone","part":0,"rotation":0})

for i in range(0,random.randint(5,20)):
    size = random.randint(1,10)
    x = random.randint(0,world_len-(size+1))
    y = random.randint(0,world_len-(size+1))
    for xpos in range(0,size):
        for ypos in range(0,size):
            grass_chance = ["grass","grass","leaves"]
            world[x+xpos+((y+ypos)*world_len)]["tile"] = random.choice(grass_chance)
    

for i in range(0, 6):
    x = random.randint(0,world_len-1)
    y = random.randint(0,world_len-1)    
    if i == 0 or i == 1:
        world[x+(y*world_len)] = {"item":None,"building":None,"tile":"coal_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed coal ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 2:
        world[x+(y*world_len)] = {"item":None,"building":None,"tile":"iron_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed iron ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 3:
        world[x+(y*world_len)] = {"item":None,"building":None,"tile":"copper_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed copper ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 4:
        world[x+(y*world_len)] = {"item":None,"building":None,"tile":"tin_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed tin ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 5:
        world[x+(y*world_len)] = {"item":None,"building":None,"tile":"zinc_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed zinc ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
for i1 in range(0,int((world_len-20)/2)):
    x = random.randint(0,world_len-1)
    y = random.randint(0,world_len-1)     
    i = random.randint(0,6)
    if i == 0 or i == 1:
        world[x+(y*world_len)] = {"item":None,"building":None,"tile":"coal_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed coal ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 2:
        world[x+(y*world_len)] = {"item":None,"building":None,"tile":"iron_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed iron ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 3:
        world[x+(y*world_len)] = {"item":None,"building":None,"tile":"copper_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed copper ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 4:
        world[x+(y*world_len)] = {"item":None,"building":None,"tile":"tin_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed tin ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 5:
        world[x+(y*world_len)] = {"item":None,"building":None,"tile":"zinc_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed zinc ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))    
x = random.randint(0,world_len-3)
y = random.randint(0,world_len-3)
for i in range(0,3):
    for i1 in range(0,3):
        world[(x+i)+((y+i1)*world_len)] = {"item":None,"building":None,"tile":"water","part":0,"rotation":0}
        if i==1 and i1 ==1:
            world[(x+i)+((y+i1)*world_len)] = {"item":None,"building":None,"tile":"kelp","part":0,"rotation":0}

world[0] = {"item":None,"building":"drill","tile":"coal_ore","part":1,"rotation":0}
world[1] = {"item":None,"building":"drill","tile":None,"part":2,"rotation":0}
world[2] = {"item":None,"building":"conveyor_belt","tile":None,"part":0,"rotation":0}

def draw_world(world,winobj,tick, pos,tooltip_props, menu_props,edit_mode):
    winobj.fill((25,25,25))
    x = 0
    x1 = 0
    y = 0
    y1 = 0
    x_borders = [pos[0]-10,pos[0]+10]
    y_borders = [pos[1]-10,pos[1]+10]
    for tile_id, tile in enumerate(world):
        if x == world_len:
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
            winobj.blit(pg.transform.scale(ground_tiles[0],(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
            if block == "coal_ore":
                winobj.blit(pg.transform.scale(ores[-1],(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
            elif block == "iron_ore":
                winobj.blit(pg.transform.scale(ores[0],(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
            elif block == "copper_ore":
                winobj.blit(pg.transform.scale(ores[1],(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
            elif block == "zinc_ore":
                winobj.blit(pg.transform.scale(ores[2],(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
            elif block == "tin_ore":
                winobj.blit(pg.transform.scale(ores[3],(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
            elif block == "kelp":
                winobj.blit(pg.transform.scale(ores[4],(cell_size,cell_size)),(x1*cell_size,y1*cell_size))  
            elif block == "water":
                winobj.blit(pg.transform.scale(ground_tiles[1],(cell_size,cell_size)),(x1*cell_size,y1*cell_size))              
            elif block == "grass":
                winobj.blit(pg.transform.scale(ground_tiles[2],(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
            elif block == "leaves":
                winobj.blit(pg.transform.scale(ground_tiles[2],(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
                winobj.blit(pg.transform.scale(ores[5],(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
            if block_building == "drill":
                if block_part == 1:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][0],block_rotation),(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
                elif block_part == 2:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][1],block_rotation),(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
            elif block_building == "conveyor_belt":
                if tick <= 11:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0],block_rotation),(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
                elif tick <= 22:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1],block_rotation),(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
                elif tick <= 33:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2],block_rotation),(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
                elif tick <= 44:
                    winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][3],block_rotation),(cell_size,cell_size)),(x1*cell_size,y1*cell_size))
        x+=1
    if tooltip_props[0] != -1 and tooltip_props[1] != {}:
        block = tooltip_props[1]["tile"]
        block_rotation = tooltip_props[1]["rotation"]
        block_part =tooltip_props[1]["part"]
        block_building =tooltip_props[1]["building"]
        block_item =tooltip_props[1]["item"]
        ypos = 0
        xpos = 6*cell_size
        if tooltip_props[0] >= 104:
            ypos = 3*(104-tooltip_props[0])
        if tooltip_props[0] <= 20:
            ypos = -60+tooltip_props[0]*3
        winobj.blit(pg.transform.scale(pg.transform.rotate(ui[0],0),(190,60)),(xpos+10,ypos))
        text_tile = font.render("Tile:{}".format(block),True,(0,0,0))
        text_build = font.render("Building:{}".format(block_building),True,(0,0,0))
        text_item = font.render("Item:{}".format(block_item),True,(0,0,0))
        winobj.blit(text_tile,(xpos+25+cell_size,ypos+5))
        winobj.blit(text_build,(xpos+25+cell_size,ypos+17))
        winobj.blit(text_item,(xpos+25+cell_size,ypos+30))
        if block == "coal_ore":
            winobj.blit(pg.transform.scale(ores[-1],(cell_size,cell_size)),(xpos+20,ypos+10))
        elif block == "iron_ore":
            winobj.blit(pg.transform.scale(ores[0],(cell_size,cell_size)),(xpos+20,ypos+10))
        elif block == "copper_ore":
            winobj.blit(pg.transform.scale(ores[1],(cell_size,cell_size)),(xpos+20,ypos+10))
        elif block == "zinc_ore":
            winobj.blit(pg.transform.scale(ores[2],(cell_size,cell_size)),(xpos+20,ypos+10))
        elif block == "tin_ore":
            winobj.blit(pg.transform.scale(ores[3],(cell_size,cell_size)),(xpos+20,ypos+10))
        elif block == "kelp":
            winobj.blit(pg.transform.scale(ores[4],(cell_size,cell_size)),(xpos+20,ypos+10))  
        elif block == "water":
            winobj.blit(pg.transform.scale(ground_tiles[1],(cell_size,cell_size)),(xpos+20,ypos+10)) 
        elif block == "grass":
            winobj.blit(pg.transform.scale(ground_tiles[2],(cell_size,cell_size)),(xpos+20,ypos+10))         
        elif block == "grass":
            winobj.blit(pg.transform.scale(ground_tiles[2],(cell_size,cell_size)),(xpos+20,ypos+10))
            winobj.blit(pg.transform.scale(ores[5],(cell_size,cell_size)),(xpos+20,ypos+10))
        if block_building == "drill":
            if block_part == 1:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][0],block_rotation),(cell_size,cell_size)),(xpos+20,ypos+10))
            elif block_part == 2:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["drill"][1],block_rotation),(cell_size,cell_size)),(xpos+20,ypos+10))
        elif block_building == "conveyor_belt":
            if tick <= 11:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][0],block_rotation),(cell_size,cell_size)),(xpos+20,ypos+10))
            elif tick <= 22:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][1],block_rotation),(cell_size,cell_size)),(xpos+20,ypos+10))
            elif tick <= 33:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][2],block_rotation),(cell_size,cell_size)),(xpos+20,ypos+10))
            elif tick <= 44:
                winobj.blit(pg.transform.scale(pg.transform.rotate(buildings["conveyor"][3],block_rotation),(cell_size,cell_size)),(xpos+20,ypos+10)) 
    if menu_props[1] != "hidden":
        ypos = 0
        xpos = screen_size[1] - cell_size
        if menu_props[1] == "opening" or menu_props[1] == "open":
            xpos += menu_props[0]
        elif menu_props[1] == "closing" or menu_props[1] == "hidden":
            xpos += cell_size-menu_props[0]
        winobj.blit(pg.transform.scale(pg.transform.rotate(ui[0],270),(cell_size,screen_size[1])),(xpos,ypos))
    if edit_mode:
        pg.draw.polygon(winobj,(100,100,100),[[0,screen_size[1]-50],[screen_size[1],screen_size[1]-50],[screen_size[1],screen_size[1]],[0,screen_size[1]]])
        pg.draw.polygon(winobj,(0,0,0),[[0+10,screen_size[1]-40],[screen_size[1]-10,screen_size[1]-40],[screen_size[1]-10,screen_size[1]-10],[0+10,screen_size[1]-10]])
        text_tile = dosfont.render("Rotate: [R]    Current roation: {0}˚  Current item: {1}".format(current_item[1], current_item[0]),True,(0,255,0))
        winobj.blit(text_tile,(0+40,screen_size[1] - 30))  
        
        

#main cycle
while 1:
    if tick == 45:
        tick = 0
        for tile_id, tile in enumerate(world):
            cond = random.choice([False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True])
            if tile["tile"] == "grass" and cond and tile["building"] == None:
                world[tile_id]["tile"] = "leaves"
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
    draw_world(world,window,tick,pos,[tooltip_tick,tooltip_tile],[menu_tick,menu],True)
    for evt in pg.event.get():
        if evt.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif evt.type == pg.MOUSEBUTTONDOWN:
            coords = evt.pos
            #tooltip on middle-click
            #build on right-click
            x = int(coords[1]/cell_size)
            y = int(coords[0]/cell_size)
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
            if evt.button == 1:
                x = int(coords[0]/cell_size)
                y =int(coords[1]/cell_size)
                if x_borders[0] < 0: x -= abs(x_borders[0])
                else: x += x_borders[0]
                if y_borders[0] < 0: y -= abs(y_borders[0])
                else: y += y_borders[0]
                if mode == "building":
                    if current_item[0] == "drill":
                        if current_item[1] == 0:
                            if x >= 0 and x < world_len-1  and y >= 0 and y <= world_len-1 and world[x+(y*world_len)]["building"] == None and world[(x+1)+(y*world_len)]["building"] == None:
                                if world[x+(y*world_len)]["tile"] == "leaves": world[x+(y*world_len)]["tile"] = "grass"
                                if world[(x+1)+(y*world_len)]["tile"] == "leaves": world[(x+1)+(y*world_len)]["tile"] = "grass"
                                world[x+(y*world_len)]["building"] = "drill"
                                world[(x+1)+(y*world_len)]["building"] = "drill"
                                world[x+(y*world_len)]["rotation"]= 0
                                world[(x+1)+(y*world_len)]["rotation"]= 0
                                world[x+(y*world_len)]["part"]=1
                                world[(x+1)+(y*world_len)]["part"]=2                        
                        elif current_item[1] == 90:
                            if y > 0 and y <= world_len-1  and x >= 0 and x <= world_len-1 and world[x+(y*world_len)]["building"]  == None and world[x+((y-1)*world_len)]["building"] == None:
                                if world[x+(y*world_len)]["tile"] == "leaves": world[x+(y*world_len)]["tile"] = "grass"
                                if world[x+((y-1)*world_len)]["tile"] == "leaves": world[x+((y-1)*world_len)]["tile"] = "grass"                                
                                world[x+(y*world_len)]["building"] = "drill"
                                world[x+((y-1)*world_len)]["building"] = "drill"
                                world[x+(y*world_len)]["rotation"]= 90
                                world[x+((y-1)*world_len)]["rotation"]= 90
                                world[x+(y*world_len)]["part"]=1
                                world[x+((y-1)*world_len)]["part"]=2
                        elif current_item[1] == 180:
                            if x > 0 and x <= world_len-1  and y >= 0 and y <= world_len-1 and world[x+(y*world_len)]["building"] == None and world[(x-1)+(y*world_len)]["building"] == None:
                                if world[x+(y*world_len)]["tile"] == "leaves": world[x+(y*world_len)]["tile"] = "grass"
                                if world[(x-1)+(y*world_len)]["tile"] == "leaves": world[(x-1)+(y*world_len)]["tile"] = "grass"
                                world[x+(y*world_len)]["building"] = "drill"
                                world[(x-1)+(y*world_len)]["building"] = "drill"
                                world[x+(y*world_len)]["rotation"]= 0
                                world[(x-1)+(y*world_len)]["rotation"]= 0
                                world[x+(y*world_len)]["part"]=1
                                world[(x-1)+(y*world_len)]["part"]=2 
                
            elif evt.button == 2:
                tooltip_tile = true_visible_part[x+y*20]
                tooltip_tick = 125                    
        else:
            keys = pg.key.get_pressed()
            if keys[pg.K_LALT]:speed = 4
            else: speed = 1
            if keys[pg.K_UP] and pos[1] != 0:
                pos[1] -= speed
            elif keys[pg.K_DOWN] and pos[1] != world_len:
                pos[1] += speed
            elif keys[pg.K_LEFT] and pos[0] != 0:
                pos[0] -= speed
            elif keys[pg.K_RIGHT]and pos[0] != world_len:
                pos[0] += speed
    coords = pg.mouse.get_pos()
    if coords[0] >= screen_size[1]-cell_size/2 and menu == "hidden":
        menu = "opening"
        menu_tick = 30
    elif coords[0] <= screen_size[1]-cell_size and menu == "open":
        menu = "closing"
        menu_tick = 30
    pg.display.update()
    clock.tick(45)
    tick += 1