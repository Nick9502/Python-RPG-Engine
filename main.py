import pygame, sys, time, math
from scripts.UltraColor import *
from scripts.textures import *
from scripts.SpriteSheet import *
from scripts.map_engine import *
from scripts.camera import *
from scripts.NPC import *
from scripts.player import *
from scripts.meloonatic_gui import *
from scripts.Globals import *

pygame.init()
#Initializing Globals
cSec, cFrame, FPS, deltatime = 0,0,0,0

fps_font = pygame.font.Font("C:\\Windows\\Fonts\\Verdana.ttf",20)

Globals.currentRoom=""
terrain = Map_Engine.load_map("test.map")

def display_fps():
    fps_overlay = fps_font.render(str(FPS), True, Color.Gold)
    window.blit(fps_overlay,(0,0))

def create_window():
    global window, w_height, w_width, w_title
    w_width, w_height = (800,600)
    w_title= 'Python RPG Project'
    pygame.display.set_caption(w_title)
    window = pygame.display.set_mode((w_width,w_height), pygame.HWSURFACE|pygame.DOUBLEBUF)

def fps_counter():
    global cSec, cFrame, FPS, deltatime

    if cSec == time.strftime('%S'): #Gets time in seconds so. FPS.
        cFrame += 1 #Adds as much frames per one second
    else:
        FPS = cFrame
        cFrame = 0 #Resets framew and starts over
        cSec = time.strftime('%S')
        if FPS > 0: #deltatime function
            deltatime = 1/FPS

# Initialize GUI
def play():
    Globals.scene = "game"

def exit_game():
    sys.exit()

#  Create World Button
btn_play = Menu.Button(text = "Create World", rect=(20, 20, 160, 60), bg = Color.Gray,
                      fg=Color.White,bgr=Color.CornflowerBlue,bgc=Color.Green,tag=("menu", None))
btn_play.Command=play
btn_play.Left= Globals.WIN_WIDTH / 2 - btn_play.Width/2

# Exit Button
btn_exit = Menu.Button(text = "Exit", rect=(20, 100, 160, 60), bg = Color.Gray,
                      fg=Color.White,bgr=Color.CornflowerBlue, bgc=Color.Green,tag=("menu", None))

btn_exit.Command = exit_game
btn_exit.Left = Globals.WIN_WIDTH / 2 - btn_exit.Width/2


create_window()

#Player Variable
player = Player("Nick")
player_w,player_h = player.width,player.height
player_x = (w_width / 2 - player_w / 2-Globals.cam_x)/ Tiles.Size
player_y = (w_height / 2 - player_h / 2-Globals.cam_y)/ Tiles.Size


isRunning = True


pygame.key.set_repeat(10, 10)  # Repeats KeyDowns every 10 milliseconds for held key events.
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and Globals.isMoving == False:
                player.facing="north"
                Globals.cam_Move = 'Up'
                Globals.isMoving = True
            elif event.key == pygame.K_s and Globals.isMoving == False:
                player.facing = "south"
                Globals.cam_Move = 'Down'
                Globals.isMoving = True
            elif event.key == pygame.K_a and Globals.isMoving == False:
                player.facing = "west"
                Globals.cam_Move = 'Left'
                Globals.isMoving = True
            elif event.key == pygame.K_d and Globals.isMoving == False:
                player.facing = "east"
                Globals.cam_Move = 'Right'
                Globals.isMoving = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                if Globals.isMoving:
                    Globals.isMoving = False
                    Globals.cam_Move = 'None'
            elif event.key == pygame.K_s:
                if Globals.isMoving:
                    Globals.isMoving = False
                    Globals.cam_Move = 'None'
            elif event.key == pygame.K_a:
                if Globals.isMoving:
                    Globals.isMoving = False
                    Globals.cam_Move = 'None'
            elif event.key == pygame.K_d:
                if Globals.isMoving:
                    Globals.isMoving = False
                    Globals.cam_Move = 'None'

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Left Click
                for btn in Menu.Button.All: #Cycle through list of all buttons
                    if btn.Tag[0] == Globals.scene and btn.Rolling:
                        btn.Clicked=True
                        if btn.Command != None:
                            btn.Command()
                            btn.Rolling = False
                            break




    #Render Game Scene
    if Globals.scene == "game":
        #Game Logic
        if Globals.cam_Move == 'Up':
            if not Tiles.Blocked_At((round(player_x), math.floor(player_y))):
                Globals.cam_y+=(100*deltatime)
                player.yvel+=(100*deltatime)
        elif Globals.cam_Move == 'Down':
            if not Tiles.Blocked_At((round(player_x), math.ceil(player_y))):
                Globals.cam_y -= (100 * deltatime)
                player.yvel-=(100*deltatime)
        elif Globals.cam_Move == 'Left':
            if not Tiles.Blocked_At((math.floor(player_x), round(player_y))):
                Globals.cam_x += (100 * deltatime)
                player.xvel+=(100*deltatime)
        elif Globals.cam_Move == 'Right':
            if not Tiles.Blocked_At((math.ceil(player_x), round(player_y))):
                Globals.cam_x -= (100 * deltatime)
                player.xvel-=(100*deltatime)

        player_x = (w_width / 2 - player_w / 2 - Globals.cam_x) / Tiles.Size
        player_y = (w_height / 2 - player_h / 2 - Globals.cam_y) / Tiles.Size

        #Render Graphics
        window.blit(Background.sky_BG, (0,0))
        window.blit(terrain, (Globals.cam_x,Globals.cam_y))
        player.render(window, (w_width / 2 - player_w / 2, w_height / 2 - player_h / 2))



    elif Globals.scene == "menu":
        window.fill(Color.Fog)
        btn_play.Render(window)
        btn_exit.Render(window)


    display_fps()
    pygame.display.update() #Draws to the window
    fps_counter()

pygame.quit()
sys.exit()