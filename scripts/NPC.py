import pygame


pygame.init()

def get_faces(sprite):
    faces = {}

    size = sprite.get_size()
    tile_size = (int(size[0] / 2),int(size[1] / 2)) # Sprite is 64x 64. Div 2 gets 32x32 sprite

    south= pygame.Surface(tile_size, pygame.HWSURFACE|pygame.SRCALPHA)#Alpha so sprite background cant be seen
    south.blit(sprite, (0,0), (0,0,tile_size[0],tile_size[1])) #(starting x, starting y, ending x, ending y)
    faces["south"]= south

    north = pygame.Surface(tile_size, pygame.HWSURFACE | pygame.SRCALPHA)  # Alpha so sprite background cant be seen
    north.blit(sprite, (0, 0), (tile_size[0], tile_size[1], tile_size[0], tile_size[1]))
    faces["north"] = north

    east = pygame.Surface(tile_size, pygame.HWSURFACE | pygame.SRCALPHA)  # Alpha so sprite background cant be seen
    east.blit(sprite, (0, 0), (0, tile_size[1], tile_size[0], tile_size[1]))
    faces["east"] = east

    west = pygame.Surface(tile_size, pygame.HWSURFACE | pygame.SRCALPHA)  # Alpha so sprite background cant be seen
    west.blit(sprite, (0, 0), (tile_size[0], 0, tile_size[0], tile_size[1]))
    faces["west"] = west

    return faces