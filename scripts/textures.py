import pygame
from scripts.SpriteSheet import *

pygame.init()

class Tiles:

    Size = 32

    Blocked=[]

    Blocked_Type=["3", "4", "5", "6",'7','8',"9","10","11"]

    def Blocked_At(pos):
        if list(pos) in Tiles.Blocked:
            return True
        else:
            return False

    def Load_Texture(file, Size):
        bitmap = pygame.image.load(file)
        bitmap = pygame.transform.scale(bitmap, (Size, Size))
        surface = pygame.Surface((Size, Size), pygame.HWSURFACE| pygame.SRCALPHA) # Hardware Accelerated
        surface.blit(bitmap, (0,0))
        return surface

    grass = Load_Texture("graphics\\grass.png", Size)
    stone = Load_Texture("graphics\\stone.png", Size)
    water = Load_Texture("graphics\\water.png", Size)
    water_N = Load_Texture("graphics\\water_N.png", Size)
    water_S = Load_Texture("graphics\\water_S.png", Size)
    water_E = Load_Texture("graphics\\water_E.png", Size)
    water_W = Load_Texture("graphics\\water_W.png", Size)
    water_NE = Load_Texture("graphics\\water_NE.png", Size)
    water_NW = Load_Texture("graphics\\water_NW.png", Size)
    water_SE = Load_Texture("graphics\\water_SE.png", Size)
    water_SW = Load_Texture("graphics\\water_SW.png", Size)

    Tilesets = {"1" : grass, "2" : stone, "3" : water, "4" : water_N, "5" : water_S, "6" : water_E, "7" : water_W,
                "8": water_NE, "9" : water_NW, "10" : water_SE, "11" : water_SW}

class Background:

    def Load_Background(file):
        bg = pygame.image.load(file)
        BG = pygame.Surface(bg.get_size(), pygame.HWSURFACE)
        BG.blit(bg, (0, 0))
        del bg
        return BG

    sky_BG= Load_Background("graphics\\sky.png")

class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print ('Unable to load spritesheet image:', filename)
            raise SystemExit(message)
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size,pygame.HWSURFACE|pygame.SRCALPHA).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

#Importing SpriteSheets
#TM = spritesheet("graphics\\RPG_Tilemap_M.png")
#Grass =TM.image_at((1, 34, 32, 32))


