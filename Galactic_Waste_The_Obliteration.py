#Intro to GameDev - main game file

#import libraries
import pgzrun
import random

#dimensions
WIDTH = 1000
HEIGHT = 600
SCOREBOARD_HEIGHT = 60

#defining colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#sprite images
BACKGROUND_TITLE = "background_title"
BACKGROUND_LEVEL1 = "level_1"
BACKGROUND_LEVEL2 = "level_2"
BACKGROUND_LEVEL3 = "level_3"

# start game with title screen
BACKGROUND_IMG = BACKGROUND_TITLE

#image files
BACKGROUND_IMG = "level_1"
PLAYER_IMG = "spaceship_beg_left"
JUNK_IMG = "space_junk"
SATELLITE_IMG = "satellite2"
DEBRIS_IMG = "space_debris2"
LASER_IMG = "laser_red"
START_IMG = "start_button_o"
INSTRUCTIONS_IMG = "instructions_button_o"

# initialize title screen buttons
start_button = Actor(START_IMG)
start_button.center = (WIDTH/2, 425)

instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 500)

#keep track of score
score = 0
level = 0
level_screen = 0

#counter variables
junk_collect = 0
lvl2_LIMIT = 10 #collect 5 junk to move to level 2 (can be changed later but right now the values are low so testing doesn't take too long)
lvl3_LIMIT = 20 #collect 10 junk to move to level 3

#speed of the sprites
junk_speed = 5 
satellite_speed = 3
debris_speed = 2

def on_mouse_down(pos):
    global level, level_screen

    #check start button
    if start_button.collidepoint(pos):
        level = 1
        level_screen = 1
        print("start button pressed!")

    if instructions_button.collidepoint(pos):
        level = -1
        print("instructions button pressed!")

def init():
    global player, junks, satellite, debris, lasers 
    # initializing spaceship
    player = Actor(PLAYER_IMG)
    player.midright = (WIDTH-15, HEIGHT/2)

    # initializing junks
    junks=[]
    for i in range(5):
        junk=Actor(JUNK_IMG)
        x_pos=random.randint(-700,-50)
        y_pos=random.randint(SCOREBOARD_HEIGHT,HEIGHT-junk.height)
        junk.topleft=(x_pos, y_pos)
        junks.append(junk)

    #initialize lasers
    lasers=[]
    player.laserActive = 1
    
    #initializing satellite
    satellite = Actor(SATELLITE_IMG)
    x_sat = random.randint(-700,-50)
    y_sat = random.randint(SCOREBOARD_HEIGHT, HEIGHT - satellite.height)
    satellite.topright = (x_sat, y_sat)

    #initialize debris
    debris = Actor(DEBRIS_IMG)
    x_deb = random.randint(-700,-50)
    y_deb = random.randint(SCOREBOARD_HEIGHT, HEIGHT - debris.height)
    debris.topright = (x_deb, y_deb)

    #background music
    music.play("spacelife")
    
#game loop
init()

def draw():
    screen.clear()
    screen.blit(BACKGROUND_TITLE, (0,0))

    if level == 0:
        start_button.draw()
        instructions_button.draw()

    if level == -1: #instructions screen
        screen.blit(BACKGROUND_IMG, (0,0))
        start_button.draw()

    if level >= 1:
        screen.blit(BACKGROUND_IMG, (0,0))
        player.draw()        
        for junk in junks: #this line of code will draw each piece of junk in the list 'junks'
            junk.draw()

    if level >= 2:
        satellite.draw()

    if level >= 3:
        debris.draw()
        for laser in lasers:
            laser.draw()
        
    #draw the text
    show_score = "Score: " + str(score)
    screen.draw.text(show_score, topleft=(650,25), fontsize=35, color='white')

    show_collect_value = "Junk: " + str(junk_collect)
    screen.draw.text(show_collect_value, topleft=(450,25), fontsize=35, color="WHITE")

    if level == -1: #instructions screen
        show_instructions="Use UP and DOWN arrow keys to move your player\n\nPress SPACEBAR to shoot lasers"
        screen.draw.text(show_instructions, midtop=(WIDTH/2, 250), fontsize=35, color='WHITE')

    if level >= 1:
        show_level = "LEVEL " + str(level)
        screen.draw.text(show_level, topright=(375, 25), fontsize=35, color="WHITE")

    if level_screen == 1:
        show_transition = "LEVEL " + str(level) + "\nCollect space junk\n\nPress ENTER to continue..."
        screen.draw.text(show_transition, center=(WIDTH/2, HEIGHT/2), fontsize=60, color="WHITE")

    if level_screen == 3:
        show_transition = "LEVEL " + str(level) + "\nContinue to collect space junk \nbut make sure to avoid crashing \ninto working satellites\n\nPress ENTER to continue..."
        screen.draw.text(show_transition, center=(WIDTH/2, HEIGHT/2), fontsize=60, color="WHITE")

    if  level_screen == 5:
        show_transition = "LEVEL " + str(level) + "\nContinue to collect space junk \nand avoid crashing into working satellites\n\nShoot broken satellites with lasers\n\nPress ENTER to continue..."
        screen.draw.text(show_transition, center=(WIDTH/2, HEIGHT/2), fontsize=60, color="WHITE")

    #game over screen
    if score < 0:
        game_over = "GAME OVER!\nPress ENTER to play again"
        screen.draw.text(game_over, center=(WIDTH/2, HEIGHT/2), fontsize=60, color="WHITE")

def update():
    global level, level_screen, BACKGROUND_IMG, junk_collect, score, junk_speed

    if level == -1: #instructions screen
        BACKGROUND_IMG = BACKGROUND_LEVEL1

    if junk_collect == lvl2_LIMIT: #level 2
        level = 2

    if junk_collect == lvl3_LIMIT: #level 3
        level = 3    

    if score >= 0 and level >= 1:
        if level_screen == 1: #level 1 transition screen
            BACKGROUND_IMG = BACKGROUND_LEVEL1
            if keyboard.RETURN == 1: #RETURN is the Enter key
                level_screen = 2
                print("ENTER key is pressed")
                
        if level_screen == 2: #level 1 gameplay screen
            updatePlayer()
            updateJunk()
            
        if level == 2 and level_screen <= 3:
            level_screen = 3 #level 2 transition screen
            BACKGROUND_IMG = BACKGROUND_LEVEL2
            if keyboard.RETURN == 1:
                level_screen = 4
                music.play("space_mysterious")
                print("ENTER key is pressed")
                
        if level_screen == 4: #level 2 gameplay screen
            updatePlayer()
            updateJunk()
            updateSatellite()
            junk_speed = 8
            satellite_speed = 8
            
        if level == 3 and level_screen <= 5:
            level_screen = 5 #level 3 transition screen
            BACKGROUND_IMG = BACKGROUND_LEVEL3
            if keyboard.RETURN == 1:
                level_screen = 6
                music.play("space_suspense")
                print("ENTER key is pressed")
                
        if level_screen == 6: #level 3 gameplay screen
            updatePlayer()
            updateJunk()
            updateSatellite()
            updateDebris()
            updateLasers()
            junk_speed = 10
            satellite_speed = 12
            debris_speed = 10

    if score < 0 or level == -2: #Game over
        music.stop()
        if keyboard.RETURN == 1:
            BACKGROUND_IMG = BACKGROUND_TITLE
            score = 0
            junk_collect = 0
            level = 0
            init()

def updateJunk():
    global score, junk_speed, junk_collect
    for junk in junks:
        junk.x += junk_speed #make junk move left to right across the screen; the higher the number, the faster junk's speed is
        collision = player.colliderect(junk) #detect collisions; if a collision occurs, player.colliderect(junk)=1 and when there is no collision, player.colliderect(junk)=0
    
        if (junk.left > WIDTH or collision == 1):
        #junk_speed = random.randint(2,10) #randomly set a new speed
            x_pos = -50
            y_pos = random.randint(SCOREBOARD_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)
        
        if (collision == 1):
            score += 1
            junk_collect += 1 #increase by 1 every time a collision occurs
            sounds.collect_pep.play()

def updatePlayer():
    #check for keyboard input
    if (keyboard.up == 1 or keyboard.w == 1):
        player.y -= 5

    elif (keyboard.down == 1 or keyboard.s == 1):
        player.y += 5

    #set boundaries
    if (player.top < 65):
        player.top = 65
    elif (player.bottom > HEIGHT):
        player.bottom = HEIGHT

    #check for uesr input; prevent player from moving off screen; check for firing lasers
    if (keyboard.space == 1) and level == 3:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft) #laser will appear at the left end of the spaceship
        fireLasers(laser)

def updateSatellite():
    global score, satellite_speed
    satellite.x += satellite_speed
    collision = player.colliderect(satellite)

    if (satellite.left > WIDTH or collision==1):
        x_sat = random.randint(-500,-50)
        y_sat = random.randint(SCOREBOARD_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    #collisions between player and satellite
    if (collision == 1):
        score -= 10

def updateDebris():
    global score, debris_speed
    debris.x += debris_speed
    collision = player.colliderect(debris)

    if (debris.left > WIDTH or collision==1):
        x_deb = random.randint(-500,-50)
        y_deb = random.randint(SCOREBOARD_HEIGHT, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)

    if (collision == 1):
        score -= 10

LASER_SPEED = -5 #since lasers are moving left, we use a negative x-value
def updateLasers():
    global score
    for laser in lasers:
        laser.x += LASER_SPEED
        collision_sat = satellite.colliderect(laser)
        collision_deb = debris.colliderect(laser)

        #remove laser if it moves off screen
        if laser.right < 0 or collision_sat == 1 or collision_deb == 1:
            lasers.remove(laser)

        # checking for collision with satellite
        if collision_sat == 1:
            x_sat = random.randint(-500,-50)
            y_sat = random.randint(SCOREBOARD_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score -= 5
            sounds.alien_device.play()

        # checking for collision with debris
        if collision_deb == 1:
            x_deb = random.randint(-500,-50)
            y_deb = random.randint(SCOREBOARD_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += 5
            sounds.explosion.play()
            
#=======================================================================================================================
player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list

pgzrun.go()
