import pygame
from scripts.textures import *
from scripts.Globals import *

class Map_Engine:

    def add_tile(tile, position, surf):
        surf.blit(tile, (position[0] * Tiles.Size, position[1]* Tiles.Size))

    def load_map(file):
        with open(file, "r") as mapfile:
            map_data = mapfile.read()

    # Read Tile Data
        map_data = map_data.split("-") #Splits into list of tiles 0,0:1"-"

        map_size = map_data[len(map_data) - 1] # Get map dimensions. Last argumnet (10,10) example
        map_data.remove(map_size) # Remove dimensions from map_data to avoid crash. (Only want arguments)
        map_size = map_size.split(",") #split map_size so to seperate x from y  map_size=[10,10]
        map_size[0] = int(map_size[0]) * Tiles.Size #Convert to int and adjust to size. Convert to 32 x 32 coordinates
        map_size[1] = int(map_size[1]) * Tiles.Size  # Convert to int and adjust to size. Convert to 32 x 32 coordinates
        Globals.room_width=map_size[0]#
        Globals.room_height=map_size[1]

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

            tiles[tiles.index(tile)] = (position,tile[1]) # Save tile to list in (x,y) format

        #High Performance Map Rendering Algorithm. Lol
        terrain = pygame.Surface(map_size, pygame.HWSURFACE)

        for tile in tiles:
            if tile[1] in Tiles.Tilesets:
                Map_Engine.add_tile(Tiles.Tilesets[tile[1]], tile[0], terrain)

            if tile[1] in Tiles.Blocked_Type:
                Tiles.Blocked.append(tile[0]) # Append position



        return terrain
