import pygame
import time
import random
import math
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load("imgs/space.jpg"), (WIDTH*4, HEIGHT*4))
PLAYER_WIDTH = 70
PLAYER_HEIGHT = 70
PLAYER_VEL = 5
GAME_LOGO = pygame.transform.scale(pygame.image.load("imgs/logo.png"), (598, 287))
GAME_TUTORIAL = pygame.transform.scale(pygame.image.load("imgs/tutorial.png"), (420, 258))
CENTER_SPACESHIP = pygame.transform.scale(pygame.image.load("imgs/spaceship.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
LEFT_SPACESHIP = pygame.transform.scale(pygame.image.load("imgs/spaceship_left.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
RIGHT_SPACESHIP = pygame.transform.scale(pygame.image.load("imgs/spaceship_right.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
METEOR_WIDTH = 50
METEOR_HEIGHT = 50
METEOR_VEL = 2
METEOR = pygame.transform.scale(pygame.image.load("imgs/meteor.png"), (METEOR_WIDTH, METEOR_HEIGHT))
FONT = pygame.font.SysFont("pixellari", 30)
SMALL_FONT = pygame.font.SysFont("pixellari", 20)
BIG_FONT = pygame.font.SysFont("pixellari", 50)
SHOT_COOLDOWN = 30
SCREENS = ["start", "game", "finish", "tutorial"]
TOTAL_TIME = 120
MUSICS = ["music/start_music.mp3", "music/game_music.mp3", "music/gameover_music.mp3"]
spacehip_manouver = "center"
pygame.display.set_caption("Meteor Destroyer")
screen = SCREENS[0]
music = -1
game_lost = False
def main():
    pygame.display.init()
    run = True
    player = pygame.Rect(WIDTH/2-PLAYER_WIDTH/2, HEIGHT-PLAYER_HEIGHT-20, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    meteor_add_increment = 2000
    meteor_count = 0
    meteors = []
    shots = []
    metals = []
    metals_collected = 0
    hit = False
    secounds_since_last_shot = SHOT_COOLDOWN
    global game_lost
    global spacehip_manouver
    global screen
    global music
    pygame.mixer.init()
    playMusic(0)
    while run:
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        if screen == SCREENS[0]:
            if keys_pressed[pygame.K_KP_ENTER]:
                playMusic(1)
                game_lost = False
                start_time = time.time()
                screen = SCREENS[1]
            if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
                screen = SCREENS[3]
        elif screen == SCREENS[1]:
            meteor_count += clock.tick(60)
            elapsed_time = time.time() - start_time
            secounds_since_last_shot += 1
            if meteor_count>meteor_add_increment:
                for _ in range(2):
                    meteor_size = random.randint(50, 150)
                    meteor_x = random.randint(0, WIDTH-meteor_size)
                    meteor_x_vel = (random.random()*2)-1
                    meteor = pygame.Rect(meteor_x, -meteor_size, meteor_size, meteor_size)
                    ang_vel = (random.random()*2)-1
                    meteor_y_vel =random.random()*5
                    this_meteor = Meteor(meteor, meteor_size, meteor_x, -meteor_size, meteor_x_vel, meteor_y_vel, 0, 0)
                    meteors.append(this_meteor)
                    meteor_count = 0
                    meteor_add_increment = max(2000, meteor_add_increment)
            if keys_pressed[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if keys_pressed[pygame.K_RIGHT] and player.x+PLAYER_WIDTH <= WIDTH:
                player.x += PLAYER_VEL
            if not(keys_pressed[pygame.K_LEFT]) and not(keys_pressed[pygame.K_RIGHT]):
                spacehip_manouver = "center"
            else:
                if keys_pressed[pygame.K_LEFT]:
                    spacehip_manouver = "left"
                if keys_pressed[pygame.K_RIGHT]:
                    spacehip_manouver = "right"
            if keys_pressed[pygame.K_UP]:
                    if secounds_since_last_shot>SHOT_COOLDOWN:
                        shot = pygame.Rect(player.x+(PLAYER_WIDTH/2)-5, player.y, 10, 25)
                        this_shot = Shot(shot, player.x, player.y, 0)
                        shots.append(this_shot)
                        secounds_since_last_shot = 0
            meteor_counter = 0
            for shot in shots:
                shot.rect.y -= 10
                shot.rect.x += shot.vel_x
                if shot.rect.y < -100:
                    shots.remove(shot)
            for meteor in meteors:
                other_meteor_counter = 0
                for other_meteor in meteors:
                    if meteor_counter != other_meteor_counter:
                        if(meteor.rect.colliderect(other_meteor)):
                            if(meteor.x+(meteor.size/2) > other_meteor.x+(other_meteor.size/2)):
                                meteor.vel_x += 0.1
                                other_meteor.vel_x -= 0.1
                            else:
                                meteor.vel_x -= 0.1
                                other_meteor.vel_x += 0.1
                    other_meteor_counter += 1
                meteor_counter += 1
                for metal in metals:
                    if(meteor.rect.colliderect(metal)):
                        if(meteor.x+(meteor.size/2) > metal.x+15):
                            if metal.vel_x>-3:
                                metal.vel_x -= 0.1
                        else:
                            if metal.vel_x<3:
                                metal.vel_x += 0.1
                        if(meteor.y-(meteor.size/2)> metal.y+15):
                            metal.vel_y -= 0.1
                        else:
                            metal.vel_y += 0.1
            for meteor in meteors[:]:
                meteor.rect.y += meteor.vel_y
                meteor.rect.x += meteor.vel_x
                meteor.ang += meteor.vel_ang
                if meteor.rect.y > HEIGHT:
                    meteors.remove(meteor)
                elif meteor.rect.y< -300:
                    meteors.remove(meteor)
                elif meteor.rect.x> WIDTH+10:
                    meteors.remove(meteor)
                elif meteor.rect.x<-300:
                    meteors.remove(meteor)
                elif meteor.rect.y + meteor.rect.height > player.y:
                    if meteor.rect.colliderect(player):
                        meteors.remove(meteor)
                        hit = True
                        break
                else:
                    for shot in shots[:]:
                        if shot.rect.y >= meteor.y and shot.rect.y+shot.rect.width<=meteor.rect.y+meteor.rect.width and shot.rect.x>meteor.rect.x and shot.rect.x < meteor.rect.x+meteor.rect.width:
                            metal_amount = round(meteor.rect.width/25)
                            for i in range(metal_amount):
                                metal_x = meteor.rect.x+(meteor.rect.width/2)-25
                                metal_y = meteor.rect.y+(meteor.rect.height/2)-25
                                if metal_amount == 2:
                                    if i == 0:
                                        metal_x -= 10
                                        metal_y += 10
                                    if i == 1:
                                        metal_x += 10
                                        metal_y -= 10
                                elif metal_amount == 3:
                                    if i == 0:
                                        metal_x -= 20
                                        metal_y -= 20
                                    if i == 1:
                                        metal_y += 10
                                    if i == 2:
                                        metal_x += 20
                                        metal_y -= 20
                                elif metal_amount == 4:
                                    if i == 0:
                                        metal_x += 30
                                        metal_y += 0
                                    if i == 1:
                                        metal_x += 0
                                        metal_y += 30
                                    if i == 2:
                                        metal_x -= 30
                                        metal_y += 0
                                    if i == 3:
                                        metal_x += 0
                                        metal_y -= 30
                                elif metal_amount == 5:
                                    if i == 0:
                                        metal_x += 35
                                        metal_y += 0
                                    if i == 1:
                                        metal_x += 0
                                        metal_y += 35
                                    if i == 2:
                                        metal_x -= 35
                                        metal_y += 0
                                    if i == 3:
                                        metal_x += 0
                                        metal_y -= 35
                                elif metal_amount == 6:
                                    if i == 0:
                                        metal_x -= 35
                                        metal_y -= 20
                                    if i == 1:
                                        metal_x -= 20
                                        metal_y += 30
                                    if i == 2:
                                        metal_x += 20
                                        metal_y += 30
                                    if i == 3:
                                        metal_x += 35
                                        metal_y -= 20
                                    if i == 4:
                                        metal_y -= 45
                                    
                                metal = pygame.Rect(metal_x, metal_y, 50, 50)
                                metals.append(Metal(metal, metal_x, metal_y, meteor.vel_x, meteor.vel_y))
                            meteors.remove(meteor)
                            shots.remove(shot)  
            metal_counter = 0
            for metal in metals:
                if metal.rect.y > HEIGHT:
                    metals.remove(metal)
                elif metal.rect.y + metal.rect.height > player.y:
                    if metal.rect.colliderect(player):
                        metals.remove(metal)
                        metals_collected+=1
                        break
                other_metal_counter = 0
                for other_metal in metals:
                    if metal_counter != other_metal_counter:
                        if(metal.rect.colliderect(other_metal)):
                            if(metal.x > other_metal.x):
                                if metal.vel_x<3:
                                    metal.vel_x += 0.05
                                if other_metal.vel_x>-3:
                                    other_metal.vel_x -= 0.05
                            else:
                                if metal.vel_x>-3:
                                    metal.vel_x -= 0.05
                                if other_metal.vel_x<3:
                                    other_metal.vel_x += 0.05
                            if(metal.y > other_metal.y):
                                if metal.vel_y<3:
                                    metal.vel_y += 0.05
                                if other_metal.vel_y>-3:
                                    other_metal.vel_y -= 0.05
                            else:
                                if metal.vel_x>-3:
                                    metal.vel_y -= 0.05
                                if other_metal.vel_y<3:
                                    other_metal.vel_y += 0.05
                    other_meteor_counter += 1
                for shot in shots:
                    if(metal.rect.colliderect(shot)):
                        if metal.vel_y<5 :
                            metal.vel_y -= 0.5
                        if metal.rect.x<shot.rect.x :
                            if metal.vel_x>-5:
                                metal.vel_x -= 0.5
                            shot.vel_x += 1
                        else:
                            if metal.vel_x<5:
                                metal.vel_x += 0.5
                            shot.vel_x -= 1
                metal_counter += 1
                metal.rect.y += metal.vel_y
                metal.rect.x += metal.vel_x
                if metal.rect.y > HEIGHT:
                    metals.remove(metal)
            if metals_collected>= 70:
                game_lost = True
                lost_text = FONT.render("You Won!", 1, "white")
                WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(1500)
                hit = False
                elapsed_time = 0
                meteor_count = 0
                meteors = []
                shots = []
                metals = []
                spacehip_manouver = "center"
                screen = SCREENS[2]
                playMusic(2)
                player.x = WIDTH/2-PLAYER_WIDTH/2
                metals_collected = 0
                meteor_add_increment = 200
            if hit:
                game_lost = True
                lost_text = FONT.render("You Lost!", 1, "white")
                WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(1500)
                hit = False
                elapsed_time = 0
                meteor_count = 0
                meteors = []
                shots = []
                metals = []
                spacehip_manouver = "center"
                screen = SCREENS[0]
                player.x = WIDTH/2-PLAYER_WIDTH/2
                metals_collected = 0
                meteor_add_increment = 0
                playMusic(0)
                #break
            if elapsed_time >= TOTAL_TIME:
                game_lost = True
                lost_text = FONT.render("Time up!", 1, "white")
                WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(1500)
                hit = False
                elapsed_time = 0
                meteor_count = 0
                meteors = []
                shots = []
                metals = []
                spacehip_manouver = "center"
                screen = SCREENS[0]
                player.x = WIDTH/2-PLAYER_WIDTH/2
                metals_collected = 0
                meteor_add_increment = 0
                playMusic(0)
        elif screen == SCREENS[2] or screen == SCREENS[3]:
            if keys_pressed[pygame.K_KP_ENTER]:
                playMusic(1)
                game_lost = False
                start_time = time.time()
                screen = SCREENS[1]
            if keys_pressed[pygame.K_ESCAPE]:
                playMusic(0)
                screen = SCREENS[0]           
        draw(player, elapsed_time, meteors, shots, metals, metals_collected)
    pygame.quit()

def draw(player, elapsed_time, meteors, shots, metals, metals_collected):
    if screen == SCREENS[0]:
        WIN.fill((0, 0, 0))
        WIN.blit(GAME_LOGO,(WIDTH/2-299, 50))
        start_text = FONT.render("Press Enter to Start Game", 1, "white")
        WIN.blit(start_text, (WIDTH/2-180, HEIGHT/2+100))
        how_to_play_text = FONT.render("Press Shift to learn how to play", 1, "white")
        WIN.blit(how_to_play_text, (WIDTH/2-220, HEIGHT/2+170))
        credits_text = SMALL_FONT.render("Game made by Thiago Escobar", 1, "green")
        WIN.blit(credits_text, (WIDTH/2-150, HEIGHT/2+270))
    elif screen == SCREENS[1] :
        WIN.blit(BG, (0, (elapsed_time*10)-1800))
        #pygame.draw.rect(WIN, "red", player)
        if spacehip_manouver == "center":
            WIN.blit(CENTER_SPACESHIP, (player.x,player.y))
        else:
            if spacehip_manouver == "left":
                WIN.blit(LEFT_SPACESHIP, (player.x,player.y))
            else:
                WIN.blit(RIGHT_SPACESHIP, (player.x,player.y))
        #time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
        for shot in shots[:]:
            #pygame.draw.rect(WIN, "white", shot.rect)
            SHOT_IMAGE = pygame.transform.scale(pygame.image.load("imgs/shot.png"), (10,25))
            WIN.blit(SHOT_IMAGE,(shot.rect.x, shot.rect.y))
        for meteor in meteors:
            #pygame.draw.rect(WIN, "white", meteor.rect)
            METEOR_IMAGE = pygame.transform.scale(pygame.image.load("imgs/meteor.png"), (meteor.size, meteor.size))
            meteor_angled = pygame.transform.rotate(METEOR_IMAGE, meteor.ang)
            WIN.blit(meteor_angled,(meteor.rect.x, meteor.rect.y))
        for metal in metals:
            #pygame.draw.rect(WIN, "green", metal.rect)
            METAL_IMAGE = pygame.transform.scale(pygame.image.load("imgs/metal.png"), (30, 30))
            WIN.blit(METAL_IMAGE,(metal.rect.x, metal.rect.y))
        pygame.draw.rect(WIN, "gray", pygame.Rect(215, 8, 92, 30))
        pygame.draw.rect(WIN, "black", pygame.Rect(217, 10, 88, 26))
        for i in range(metals_collected):
            pygame.draw.rect(WIN, "white", pygame.Rect(220+(i*1.2), 13, 1, 20))
        metals_collected_text = FONT.render("Metal Collected", 1, "white")
        WIN.blit(metals_collected_text, (10, 10))
        minutes_left = math.floor((TOTAL_TIME-round(elapsed_time))/60)
        secounds_left = (TOTAL_TIME-round(elapsed_time))-(minutes_left*60)
        if secounds_left<10:
            secounds_left = "0"+str(secounds_left)
        time_left_text = FONT.render(f"Time: {minutes_left}:{secounds_left}", 1, "white")
        WIN.blit(time_left_text, (10, 50))
        #WIN.blit(time_text, (10, 10))
    elif screen == SCREENS[2] :
        WIN.fill((0, 0, 0))
        start_text = BIG_FONT.render("YOU WON!", 1, "green")
        WIN.blit(start_text, (WIDTH/2-125, HEIGHT/2-80))
        start_text = FONT.render("Press Enter to Play Again", 1, "white")
        WIN.blit(start_text, (WIDTH/2-170, HEIGHT/2+170))
        return_text = FONT.render("Press Esc to return", 1, "white")
        WIN.blit(return_text, (WIDTH/2-140, HEIGHT/2+210))
        thanks_text = SMALL_FONT.render("Thank You for play", 1, "green")
        WIN.blit(thanks_text, (WIDTH/2-85, HEIGHT/2+270))
    else:
        WIN.fill((0, 0, 0))
        tutorial_text_1 = FONT.render("Fly through the asteroids", 1, "green")
        WIN.blit(tutorial_text_1, (20, 35))
        tutorial_text_2 = FONT.render("field shooting them to", 1, "green")
        WIN.blit(tutorial_text_2, (20, 65))
        tutorial_text_3 = FONT.render("collect enought metal in 2", 1, "green")
        WIN.blit(tutorial_text_3, (20, 95))
        tutorial_text_4 = FONT.render("minutes or less.", 1, "green")
        WIN.blit(tutorial_text_4, (20, 125))
        WIN.blit(GAME_TUTORIAL,(WIDTH/2-50, 150))
        start_text = FONT.render("Press Enter to Start Game", 1, "white")
        WIN.blit(start_text, (WIDTH/2-180, HEIGHT/2+250))
        return_text = FONT.render("Press Esc to return", 1, "white")
        WIN.blit(return_text, (WIDTH/2-140, HEIGHT/2+210))
    pygame.display.update()

def playMusic(music_number):
    global music
    if music != music_number:
        music = music_number
        pygame.mixer.music.load(MUSICS[music_number])
        pygame.mixer.music.play(-1)

class Meteor:
    def __init__(self, rect, size, x, y, vel_x, vel_y, ang, vel_ang):
        self.rect = rect
        self.size = size
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.ang = ang
        self.vel_ang = vel_ang

class Shot:
    def __init__(self, rect, x, y, vel_x):
        self.rect = rect
        self.x = x
        self.y = y
        self.vel_x = vel_x

class Metal:
    def __init__(self, rect, x, y, vel_x, vel_y):
        self.rect = rect
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y

if __name__ == "__main__":
    main()