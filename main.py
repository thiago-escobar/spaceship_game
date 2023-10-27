import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load("imgs/space.jpg"), (WIDTH*4, HEIGHT*4))
PLAYER_WIDTH = 70
PLAYER_HEIGHT = 70
PLAYER_VEL = 5
CENTER_SPACESHIP = pygame.transform.scale(pygame.image.load("imgs/spaceship.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
LEFT_SPACESHIP = pygame.transform.scale(pygame.image.load("imgs/spaceship_left.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
RIGHT_SPACESHIP = pygame.transform.scale(pygame.image.load("imgs/spaceship_right.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
METEOR_WIDTH = 50
METEOR_HEIGHT = 50
METEOR_VEL = 2
METEOR = pygame.transform.scale(pygame.image.load("imgs/meteor.png"), (METEOR_WIDTH, METEOR_HEIGHT))
FONT = pygame.font.SysFont("comicsans", 30)
SHOT_COOLDOWN = 30
spacehip_manouver = "center"
pygame.display.set_caption("Meteor Destroyer")

def main():
    run = True
    player = pygame.Rect(WIDTH/2-PLAYER_WIDTH/2, HEIGHT-PLAYER_HEIGHT-20, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    meteor_add_increment = 2000
    meteor_count = 0
    meteors = []
    shots = []
    hit = False
    secounds_since_last_shot = SHOT_COOLDOWN
    global spacehip_manouver
    while run:
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
                velocity = random.randint(1,7)
                this_meteor = Meteor(meteor, meteor_size, meteor_x, -meteor_size, meteor_x_vel, velocity, 0, 0)
                meteors.append(this_meteor)
                meteor_count = 0
                meteor_add_increment = max(200, meteor_add_increment-5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys_pressed = pygame.key.get_pressed()
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
                    this_shot = Shot(shot, player.x, player.y)
                    shots.append(this_shot)
                    secounds_since_last_shot = 0
        meteor_counter = 0
        for shot in shots:
            shot.rect.y -= 10
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
        for meteor in meteors[:]:
            meteor.rect.y += meteor.vel_y
            meteor.rect.x += meteor.vel_x
            meteor.ang += meteor.vel_ang
            if meteor.rect.y > HEIGHT:
                meteors.remove(meteor)
            elif meteor.rect.y + meteor.rect.height > player.y:
                if meteor.rect.colliderect(player):
                    meteors.remove(meteor)
                    hit = True
                    break
            else:
                for shot in shots[:]:
                    if shot.rect.y >= meteor.y and shot.rect.y+shot.rect.width<=meteor.rect.y+meteor.rect.width and shot.rect.x>meteor.rect.x and shot.rect.x < meteor.rect.x+meteor.rect.width:
                        meteors.remove(meteor)
                        shots.remove(shot)
        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break
        draw(player, elapsed_time, meteors, shots)
    pygame.quit()

def draw(player, elapsed_time, meteors, shots):
    WIN.blit(BG, (0, (elapsed_time*10)-1800))
    #pygame.draw.rect(WIN, "red", player)
    if spacehip_manouver == "center":
        WIN.blit(CENTER_SPACESHIP, (player.x,player.y))
    else:
        if spacehip_manouver == "left":
            WIN.blit(LEFT_SPACESHIP, (player.x,player.y))
        else:
            WIN.blit(RIGHT_SPACESHIP, (player.x,player.y))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    for shot in shots[:]:
        #pygame.draw.rect(WIN, "white", shot.rect)
        SHOT_IMAGE = pygame.transform.scale(pygame.image.load("imgs/shot.png"), (10,25))
        WIN.blit(SHOT_IMAGE,(shot.rect.x, shot.rect.y))
    for meteor in meteors:
        #pygame.draw.rect(WIN, "white", meteor.rect)
        METEOR_IMAGE = pygame.transform.scale(pygame.image.load("imgs/meteor.png"), (meteor.size, meteor.size))
        meteor_angled = pygame.transform.rotate(METEOR_IMAGE, meteor.ang)
        WIN.blit(meteor_angled,(meteor.rect.x, meteor.rect.y))
    WIN.blit(time_text, (10, 10))
    pygame.display.update()


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
    def __init__(self, rect, x, y):
        self.rect = rect
        self.x = x
        self.y = y

if __name__ == "__main__":
    main()