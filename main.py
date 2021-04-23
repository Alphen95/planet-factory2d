import pygame as pg
import sys, random, os, datetime

os.makedirs("logs",exist_ok=True)
log_file = open(os.path.join("logs","log-{}.txt".format(str(datetime.datetime.now())[:-7])),"w+")
log_file.write("[INFO] program started, time: {}\n".format(str(datetime.datetime.now())[:-7]))

ores = [
    pg.image.load(os.path.join("res","ore_iron.png")),
    pg.image.load(os.path.join("res","ore_copper.png")),
    pg.image.load(os.path.join("res","ore_zinc.png")),
    pg.image.load(os.path.join("res","ore_tin.png")),
    pg.image.load(os.path.join("res","ore_coal.png"))
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

stone = pg.image.load(os.path.join("res","stone.png"))
tick = 0

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
    x = random.randint(0,40)
    y = random.randint(0,40)    
    if i == 0 or i == 1 or i == 6 or i == 7 or i == 12 or i == 13:
        world[x+y*10] = {"item":None,"building":None,"tile":"coal_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed coal ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 2 or i == 8 or i == 14:
        world[x+y*10] = {"item":None,"building":None,"tile":"iron_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed iron ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 3 or i == 9 or i == 15:
        world[x+y*10] = {"item":None,"building":None,"tile":"copper_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed copper ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 4 or i == 10 or i == 16:
        world[x+y*10] = {"item":None,"building":None,"tile":"tin_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed tin ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))
    elif i == 5 or i == 11 or i == 17:
        world[x+y*10] = {"item":None,"building":None,"tile":"zinc_ore","part":0,"rotation":0}
        log_file.write("[DEBUG] placed zinc ore in x:{0} y:{1}, time:{2}\n".format(x,y,str(datetime.datetime.now())[:-7]))

world[0] = {"item":None,"building":"drill","tile":"coal_ore","part":1,"rotation":0}
world[1] = {"item":None,"building":"drill","tile":None,"part":2,"rotation":0}
world[2] = {"item":None,"building":"conveyor_belt","tile":None,"part":0,"rotation":0}

def draw_world(world,winobj,tick, pos):
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
            winobj.blit(pg.transform.scale(stone,(30,30)),(x1*30,y1*30))
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

#main cycle
while 1:
    if tick == 45:
        tick = 0
    draw_world(world,window,tick,pos)
    #print(a)
    for i in pg.event.get():
        if i.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif i.type == pg.MOUSEBUTTONDOWN:
            coords = i.pos
            if i.button == 2:
                #tooltip on middle-click
                x = int(coords[0]/30)
                y = int(coords[1]/30)
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
                print(true_visible_part)
                print(x,y)
                print(true_visible_part[x+(y*20)])
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_UP and pos[1] != 0:
                pos[1] -= 1
            elif i.key == pg.K_DOWN and pos[1] != 40:
                pos[1] += 1
                print(pos[1])
            elif i.key == pg.K_LEFT and pos[0] != 0:
                pos[0] -= 1
            elif i.key == pg.K_RIGHT and pos[0] != 40:
                pos[0] += 1
                print(pos[1])
    pg.display.update()
    clock.tick(45)
    tick += 1