import pygame, sys, time, math

from scripts.UltraColor import *
from scripts.textures import *


def export_map(file):
    map_data = ""

    # Get Map Dimensions
    max_x = 0
    max_y = 0

    for t in tile_data:
        if t[0] > max_x:
            max_x = t[0]
        if t[1] > max_y:
            max_y = t[1]

    # Save Map Tiles
    for tile in tile_data:
        map_data = map_data + str(int(tile[0]/ Tiles.Size)) + "," + str(int(tile[1]/ Tiles.Size)) + ":" + tile[2] + "-"

    #Save Map Dimensions
    map_data = map_data + str(int(max_x/Tiles.Size)) + "," + str(int(max_y/ Tiles.Size))

    #Write file
    with open(file, "w") as mapfile:
        mapfile.write(map_data)


def import_map(file):
    global tile_data
    with open(file, "r") as mapfile:
        map_data=mapfile.read()
    # Read Tile Data
        map_data = map_data.split("-") #Splits into list of tiles 0,0:1"-"

        map_size = map_data[len(map_data) - 1] # Get map dimensions. Last argumnet (10,10) example
        map_data.remove(map_size) # Remove dimensions from map_data to avoid crash. (Only want arguments)
        map_size = map_size.split(",") #split map_size so to seperate x from y  map_size=[10,10]
        map_size[0] = int(map_size[0]) * Tiles.Size #Convert to int and adjust to size. Convert to 32 x 32 coordinates
        map_size[1] = int(map_size[1]) * Tiles.Size  # Convert to int and adjust to size. Convert to 32 x 32 coordinates

        tiles = []
        #Formatting Map Data into readable
        for tile in range(len(map_data)):
            map_data[tile] = map_data[tile].replace("\n","")#Replace any newlines with blank strings. Converts to one line.
            tiles.append(map_data[tile].split(":"))#appending coordinates and Spliting colon from coordinates (0,0:1)

        for tile in tiles: #Cycle through all tiles. one by one
            tile[0] = tile[0].split(",") # Split position into list [(x,y)] becomes [x,y]
            position = tile[0]
            for p in position:
                position[position.index(p)] = int(p) # Convert each individual coordinate in position to int.
            # Save tile to list in (x,y, brush) format
            tiles[tiles.index(tile)] = (position[0]*Tiles.Size, position[1]*Tiles.Size, tile[1])

        tile_data = tiles




window = pygame.display.set_mode((640,480),pygame.HWSURFACE)
pygame.display.set_caption("Map Editor")
clock = pygame.time.Clock()

txt_font = pygame.font.Font("C:\\Windows\\Fonts\\Verdana.ttf",20)

mouse_pos = 0
mouse_x, mouse_y = 0, 0
cSec, cFrame, FPS= 0,0,0

map_width,map_height = 50* Tiles.Size, 50* Tiles.Size #100 Tiles of 32 x 32 Size

Ghosts={"Adding":Color.WithAlpha(100, Color.CornflowerBlue), # Alpha goes (0,255) 100 for Translucency
        "Removing":Color.WithAlpha(100, Color.LightCoral )
        }
#New Surface for Highliting Tiles. Supports Translucent squares through use of alpha
select = pygame.Surface((Tiles.Size, Tiles.Size), pygame.HWSURFACE|pygame.SRCALPHA)
select.fill(Ghosts["Adding"])


#Store tiles that are in the map
tile_data = []

cam_x, cam_y = 0, 0
cam_Move = ""
isMoving=False

brush = "1" #Default to grass


def fps_counter():
    global cSec, cFrame, FPS

    if cSec == time.strftime('%S'): #Gets time in seconds so. FPS.
        cFrame += 1 #Adds as much frames per one second
    else:
        FPS = cFrame
        cFrame = 0 #Resets framew and starts over
        cSec = time.strftime('%S')

def display_fps():
    fps_overlay = txt_font.render(str(FPS), True, Color.Gold)
    window.blit(fps_overlay, (0, 0))

#Initialize Default Map
for x in range(0,map_width, Tiles.Size):
    for y in range(0, map_height, Tiles.Size):
        tile_data.append([x, y, "1"])

isRunning = True
pygame.key.set_repeat(10, 10) #Repeats KeyDowns every 10 millisecons for held key events.
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:

            #CAMERA MOVEMENT
            if event.key == pygame.K_w:
                cam_Move = "Up"
                isMoving = True
            elif event.key == pygame.K_s:
                cam_Move = "Down"
                isMoving = True
            elif event.key == pygame.K_a:
                cam_Move = "Left"
                isMoving = True
            elif event.key == pygame.K_d:
                cam_Move = "Right"
                isMoving = True


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w :
                if isMoving:
                    isMoving = False
                    cam_Move = 'None'
            elif event.key == pygame.K_s:
                if isMoving:
                    isMoving = False
                    cam_Move = 'None'
            elif event.key == pygame.K_a:
                if isMoving:
                    isMoving = False
                    cam_Move = 'None'
            elif event.key == pygame.K_d:
                if isMoving:
                    isMoving = False
                    cam_Move = 'None'

            # BRUSHES/TOOLTIPS
            elif event.key == pygame.K_F1:
                choice = input("Brush Tag: ")
                brush = choice
                print("A brush has been selected. You may now add tiles.")

            elif event.key == pygame.K_F2:
                brush = "r"
                print("The Brush has been changed to the Tile Remover")

            # SAVE MAP
            elif event.key == pygame.K_F11:
                name = input("Map Name: ")
                export_map(name + ".map")
                print("Map Saved Successfully!")

            elif event.key == pygame.K_F10:
                name = input("Map Name: ")
                import_map(name + ".map")
                print("Map Loaded Successfully!")


        #Keeping Track of the Cursor
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = math.floor(mouse_pos[0] / Tiles.Size) * Tiles.Size # Round to nearest tile
            mouse_y = math.floor(mouse_pos[1] / Tiles.Size) * Tiles.Size # .floor() used for accuracy

        if event.type == pygame.MOUSEBUTTONDOWN:
            tile = [mouse_x - cam_x, mouse_y - cam_y, brush] # Keep as list. [x,y,Tile ID]

            found = False
            for t in tile_data:
                if t[0] == tile[0] and t[1] == tile[1]: #If there is a tile at the position you clicked
                    found = True
                    break #Exit mouse click

            if not found:
                if not brush == "r":
                    tile_data.append(tile)
            else:
                if brush == "r":
                    #Remove Tile
                    for t in tile_data:
                        if t[0] == tile[0] and t[1] == tile[1]:
                            tile_data.remove(t)
                            print("Tile Removed")
                else:
                    print('A tile is already placed here.')




        #Logic
        if cam_Move == "Up":
            cam_y+= Tiles.Size
        elif cam_Move == "Down":
            cam_y-=Tiles.Size
        elif cam_Move == "Left":
            cam_x-= Tiles.Size
        elif cam_Move == "Right":
            cam_x+=Tiles.Size


        #Render Graphics
        window.fill(Color.Blue)

        #Drawing Map
        for tile in tile_data:
            try:
                window.blit(Tiles.Tilesets[tile[2]], (tile[0] + cam_x, tile[1] + cam_y))
            except:
                pass

        #Draw Tile Highlighter
        window.blit(select,(mouse_x,mouse_y))

        display_fps()
        pygame.display.update()
        fps_counter()


        clock.tick(60) #60 FPS





pygame.quit()
sys.exit()