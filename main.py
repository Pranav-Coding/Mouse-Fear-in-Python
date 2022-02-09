import pygame
import sys
import random
from pygame import mixer

pygame.init()
#Pygame Setting
background = pygame.image.load("background.jpg")
screen = pygame.display.set_mode((800,600))
screen_rect = screen.get_rect()
pygame.display.set_caption("Cursor Fear")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)

#Colors
green = (0,255,0)
red = (255,0,0)
Hcolor = green

#Variables
gravity = 0.04
movement = 0
jumpcount = 2
sy = 150
state = ""
timer = 0
ltime = 1000
rnum = random.randint(100,200)
Hp = 100
gameon = False
camera = [0,0]

#Sprites 
##Player
# player_surface = pygame.Surface((40,60))
p1 = pygame.image.load("player1.png").convert_alpha()
p2 = pygame.image.load("player2.png").convert_alpha()
p3 = pygame.image.load("player3.png").convert_alpha()
pindex = 1
p_frames = [p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3,p1,p2,p3]
# player_surface = pygame.image.load("p1.png")
player_surface = p_frames[pindex]
player_rect = player_surface.get_rect(center = (100,400))
# ground = pygame.Surface((300,100))
wground = pygame.Surface((300,100))
wground.fill((255,255,255))
ground = pygame.image.load("ground.png").convert_alpha()
# ground.fill((255,255,255))


#Levels and setting
level = 1
level_1 = ["11110110011001010101112"]
level_2 = ["110011001000111001010101100111110002"]
level_3 = ["101100110010001110010101011001111100010010001112"]
level_4 = ["1101011001100100011100101010110011111000100100011100001110011102"]
level_5 = ["11010110011001000111001010101100111110001001000111000011100111011100112"]
level_6 = ["0000000000000000000000000"]
levels = [level_1,level_2,level_3,level_4,level_5]






#Functions
def showscore():
    Health = font.render("Health" , True, (255,255,255))
    screen.blit(Health, (580, 10))
    pass
def ShowLevel():
	Clevel = font.render("Level:-"+ str(level), True, (255,255,255))
	screen.blit(Clevel, (10,10))
def showstate():
	x = font.render(f"{state}", True, (255,255,255))
	screen.blit(x, (250,sy+150))
def showtimer():
	t = font.render(f"best:{str(ltime)}", True, (255,255,255))
	screen.blit(t, (0,580))
def showtimeinscreen():
	r = font.render(f"time:{str(timer)}", True, (255,255,255))
	screen.blit(r, (100,10))
def splashscreen():
	img = pygame.image.load("splash2.png")
	screen.blit(img, (250,sy))
	ctp = pygame.image.load("ctp1.png")
	screen.blit(ctp, (270,sy+230))
	showstate()
	showtimer()
def loadlevel():
	global level
	global Hp
	global camera
	x = 0
	index = 0
	global jumpcount
	def collide_ground(ply, surface):
		return True if ply.colliderect(surface) else False
	
	for s in levels[(level-1)]:
		index += 1
		for i in s:
			if i == str(1):
				ground_rect = ground.get_rect(topleft=(x-camera[0],500))
				screen.blit(ground, ground_rect)
				x += 300
				if collide_ground(player_rect, ground_rect):
					player_rect.midbottom = (player_rect.centerx,500)
					Hp -= 3
					jumpcount += 1
				else:
					Hp += 0.1
			elif i == str(2):
				wground_rect = wground.get_rect(topleft=(x-camera[0],500))
				screen.blit(wground, wground_rect)
				if collide_ground(player_rect, wground_rect):
					player_rect.midbottom = (player_rect.centerx,500)
					player_rect.centerx = 100
					player_rect.centery = 150
					camera = [0,0]
					x = 0
					level += 1
					loadlevel()
					break


			elif i == str(0):
				x += rnum
def is_over(rect, pos):
	return True if rect.collidepoint(pos[0], pos[1]) else False


#User Events
time = pygame.USEREVENT
pygame.time.set_timer(time, 1000)
legup = pygame.USEREVENT+1
pygame.time.set_timer(legup, 100)

 #Background Music
pygame.mixer.Channel(0).play(pygame.mixer.Sound('back.wav'))


while True:
	screen.fill((0,0,0))
	screen.blit(background,(0,0))

	if jumpcount > 2:
		jumpcount = 2
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == time:
			timer += 1
			if sy == 155:
				sy = 150
			else:
				sy = 155
		if event.type == legup:
			pindex += 1
		if jumpcount > 0:
			if event.type == pygame.MOUSEBUTTONUP:
				movement = 0
				movement = -3
				jumpcount -= 1
				mixer.music.load('jump.wav')
				mixer.music.play()
			if event.type == pygame.MOUSEBUTTONUP and gameon == False:
				gameon = True
				loadlevel()
				player_rect.centerx = 100
				player_rect.centery = 200
				camera = [0,0]
				x = 0

	if gameon:
		loadlevel()

		mouse_pos = pygame.mouse.get_pos()
		# if (mouse_pos[0] >= player_rect.centerx - 100) and (mouse_pos[0] <= player_rect.centerx + 100):
		# 	print(mouse_pos)
		if (mouse_pos[0] >= player_rect.centerx - 100) and ((mouse_pos[0] <= player_rect.centerx+50) and ((mouse_pos[1] >= player_rect.centery - 100) and (mouse_pos[1] <= player_rect.centery + 200))) :
			player_rect.centerx += abs((mouse_pos[0] - player_rect.centerx) / 50)
	
		if (mouse_pos[0] <= player_rect.centerx + 100) and ((mouse_pos[0] >= player_rect.centerx) and ((mouse_pos[1] >= player_rect.centery - 100) and (mouse_pos[1] <= player_rect.centery +200))) :
			player_rect.centerx -= abs((mouse_pos[0] - player_rect.centerx) / 50)

		if (mouse_pos[1] >= player_rect.centery - 100) and (mouse_pos[1] <= player_rect.centery) :
			player_rect.centery += abs((mouse_pos[1] - player_rect.centerx) / 95)

	
		if is_over(player_rect, mouse_pos) or (player_rect.centery > 570 ):
			level = 1
			state = "Why don't you try a bit harder"
			mixer.music.load('scream.wav')
			mixer.music.play()
			loadlevel()
			timer = 0
			x = 0
			gameon = False

	
		screen.blit(player_surface, player_rect)
		movement += gravity
		player_rect.centery += movement
	
			

	
			
		camera[0] += 1
		camera[1] -= 2
		if Hp < 5:
			player_rect.centerx = 100
			player_rect.centery = 50
			timer = 0
			gameon = False
			level = 1
			mixer.music.load('scream.wav')
			mixer.music.play()
			camera = [0,0]
			x = 0
			Hp = 100
			loadlevel()
		showscore()
		ShowLevel()
		if Hp >= 100:
			Hp = 100
		if Hp < 70:
			Hcolor = red
		Hp_bar_surface = pygame.Surface((Hp,20))
		Hp_bar_surface.fill(Hcolor)
		screen.blit(Hp_bar_surface, (650,10))
		
		
		if level > 5:
			state = "You WIN NOICE I Try harder"
			loadlevel()
			gameon = False
			level = 1
			if timer < ltime:
				ltime = timer
		else:
			Hcolor = green
		showtimeinscreen()
		
		
		player_surface = p_frames[pindex]
		if pindex > 2:
			pindex = 0
		if player_rect.centerx > 770:
			player_rect.centerx = 770

	else:
		splashscreen()

	pygame.display.flip()
	clock.tick(60)