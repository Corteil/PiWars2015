import sys, pygame
from pygame.locals import *
import time
import subprocess
import os

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
pygame.init()


# define function for printing text in a specific place and with a specific colour and add a border
def make_button(text,boxColour,TextColour, hight, width, xpo, ypo):
    font = pygame.font.Font(None, 24)
    label = font.render(str(text), 1, (TextColour))
    screen.blit(label, (xpo, ypo))
    pygame.draw.rect(screen, boxColour, (xpo - 5, ypo - 5, width, hight), 1)


# define function that checks for mouse location
def on_click():
    click_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    # check to see if exit has been pressed
    if 200 <= click_pos[0] <= 300 and 130 <= click_pos[1] <= 230:
        #print "You pressed exit"
        button(0)
    # now check to see if button 1 was pressed
    if 15 <= click_pos[0] <= 150 and 15 <= click_pos[1] <= 50:
        #print "You pressed button 1"
        button(1)
    # now check to see if button 2 was pressed
    if 15 <= click_pos[0] <= 150 and 65 <= click_pos[1] <= 100:
        #print "You pressed button 2"
        button(2)
    # now check to see if button 3 was pressed
    if 15 <= click_pos[0] <= 150 and 115 <= click_pos[1] <= 150:
        #print "You pressed button 3"
        button(3)
    # now check to see if button 4 was pressed
    if 15 <= click_pos[0] <= 150 and 165 <= click_pos[1] <= 200:
        #print "You pressed button 4"
        button(4)


# define action on pressing buttons
def button(number):
    """

    :type number:
    """
    print "You pressed button ", number
    if number == 0:  # specific script when exiting
        screen.fill(black)
        font = pygame.font.Font(None, 36)
        label1 = font.render("Human Robot Display", 1, dark_gray)
        label2 = font.render("Interface Shutting Down", 1 , dark_gray)
        screen.blit(label1, (25, 80))
        screen.blit(label2, (10, 120))
        pygame.display.flip()
        print('Human Robot Interface Shutting Down')
        time.sleep(5)
        sys.exit()

    if number == 1:
        print("distance.py started")
        screen.fill(light_gray)
        logo = pygame.image.load("/home/pi/PiWars2015/logo.png")
        screen.blit(logo, (90, 5))
        font = pygame.font.Font(None, 42)
        label1 = font.render("Proximity alert", 1 , dark_gray)
        screen.blit(label1, (50, 120))
        pygame.display.flip()
        os.system('python /home/pi/PiWars2015/distance.py')
        print("distance finished")

        # Display Wall!! on screen

        screen.fill(light_gray)
        logo = pygame.image.load("/home/pi/PiWars2015/logo.png")
        screen.blit(logo, (90, 5))
        font = pygame.font.Font(None, 96)
        label1 = font.render("WALL!", 1 , red)
        screen.blit(label1, (50, 120))
        pygame.display.flip()
        time.sleep(5)
        mainMenu(screen)

    elif number == 2:
        print("3 Point Turn started")
        screen.fill(light_gray)
        logo = pygame.image.load("/home/pi/PiWars2015/logo.png")
        screen.blit(logo, (90, 5))
        font = pygame.font.Font(None, 72)
        label1 = font.render('DANGER! ', 1, red)
        font = pygame.font.Font(None, 36)
        label2 = font.render("Robot In Control", 1 , dark_gray)
        font = pygame.font.Font(None, 24)
        label3 = font.render('Press "SELECT" to Release Control', 1, dark_gray)
        screen.blit(label1, (45, 90))
        screen.blit(label2, (55, 150))
        screen.blit(label3, (30, 190))
        pygame.display.flip()
        print("Human Robot Interface Shutting Down")
        os.system('python /home/pi/PiWars2015/3_point_turn_V2.py')
        print("robot control released")
        mainMenu(screen)

    elif number == 3:
        print("line Following started")
        screen.fill(light_gray)
        logo = pygame.image.load("/home/pi/PiWars2015/logo.png")
        screen.blit(logo, (90, 5))
        font = pygame.font.Font(None, 40)
        label1 = font.render("LINE FOLLOWING ", 1, red)
        font = pygame.font.Font(None, 36)
        label2 = font.render("Robot In Control", 1 , dark_gray)
        font = pygame.font.Font(None, 24)
        label3 = font.render('Press "SELECT" to Release Control', 1, dark_gray)
        screen.blit(label1, (05, 90))
        screen.blit(label2, (55, 150))
        screen.blit(label3, (30, 190))
        pygame.display.flip()
        print("Human Robot Interface Shutting Down")
        os.system('python /home/pi/PiWars2015/lineFollowing.py')
        print("robot control released")
        mainMenu(screen)

    elif number == 4:
        print("manual control started")
        screen.fill(light_gray)
        logo = pygame.image.load("/home/pi/PiWars2015/logo.png")
        screen.blit(logo, (90, 5))
        font = pygame.font.Font(None, 72)
        label1 = font.render("DANGER! ", 1, red)
        font = pygame.font.Font(None, 36)
        label2 = font.render("Human In Control", 1 , dark_gray)
        font = pygame.font.Font(None, 24)
        label3 = font.render('Press "SELECT" to Release Control', 1, dark_gray)
        screen.blit(label1, (45, 90))
        screen.blit(label2, (55, 150))
        screen.blit(label3, (30, 190))
        pygame.display.flip()
        print("Human Robot Interface Shutting Down")
        os.system('/home/pi/PiWars2015/runDiabloJoy.sh')
        print("manual control released")
        mainMenu(screen)


def mainMenu(screen):

    # set up the fixed items on the menu
    screen.fill(light_gray)  # change the colours if needed

    logo = pygame.image.load("/home/pi/PiWars2015/logo.png")
    exit = pygame.image.load("/home/pi/PiWars2015/exit.tiff")
    screen.blit(logo, (180, 5))
    screen.blit(exit, (200, 130))

    # hide the mouse pointer
    pygame.mouse.set_visible(False)

    # Add buttons and labels
    make_button("Proximity alert ", dark_gray, dark_gray, 35, 125, 20, 20)
    make_button("3 Point Turn", dark_gray, dark_gray, 35, 125, 20, 70)
    make_button("Line Following", dark_gray, dark_gray, 35, 125, 20, 120)
    make_button("Manual Mode", dark_gray, dark_gray, 35, 125, 20, 170)

# set size of the screen
size = width, height = 320, 240

# define colours
blue = 26, 0, 255
cream = 254, 255, 250
black = 0, 0, 0
red = 255, 0, 0
white = 255, 255, 255
light_gray = 192, 192, 192
dark_gray = 128, 128, 128

screen = pygame.display.set_mode(size)
mainMenu(screen)

# While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print "screen pressed"  # for debugging purposes
            pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            print pos  # for checking
            #pygame.draw.circle(screen, white, pos, 2,
                              # 0)  # for debugging purposes - adds a small dot where the screen is pressed
            on_click()

        # ensure there is always a safe way to end the program if the touch screen fails

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    pygame.display.update()
