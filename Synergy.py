
import pygame
import random
import time
import sys
from math import *
from pygame.locals import *

pygame.init()
pygame.mixer.Channel(0).play(pygame.mixer.Sound('Soundtrack.ogg'),-1)
pygame.time.wait(200)
width = 350
height = 650

screen = pygame.display.set_mode((width,height)) 
"""Passing a Tuple as variable as it only accepts a single parameter
Variables instead of hard-coding to be able to change resolution later"""

pygame.display.set_caption("Synergy")

clock = pygame.time.Clock()

blue_ball = pygame.image.load("Blue copy.png")		# Loaded images in the background
red_ball = pygame.image.load("Red copy.png")		# Contained in the same directory
blue_ball = pygame.transform.scale(blue_ball,(26,26))
red_ball = pygame.transform.scale(red_ball,(26,26))

def message_display(msg,size):
	font = pygame.font.SysFont("helvetica",size)				
	for i in range(256):
		text = font.render(msg, True, (255-i,255-i,255-i))
		textrect = text.get_rect()
		textrect.center = ((width*0.5),(height*0.65))
		screen.fill((0,0,0))
		screen.blit(text,textrect)
		pygame.display.update()
		pygame.event.pump()
		time.sleep(0.0005)

def score_display(score):
	font = pygame.font.SysFont("helvetica",25)
	text = font.render(str(score), True,(255,255,255))
	textrect = text.get_rect()
	textrect.center = (20,15)
	screen.blit(text,textrect)

def lives_display(lives):
	font = pygame.font.SysFont("helvetica",20)
	text = font.render(str(lives), True,(255,255,255))
	textrect = text.get_rect()
	textrect.center = (width-15,15)
	screen.blit(text,textrect)
	font = pygame.font.SysFont("helvetica",20)
	text = font.render("Lives", True,(255,255,255))
	textrect = text.get_rect()
	textrect.center = (width-50,15)
	screen.blit(text,textrect)

def displaythings(l):
	for i in l:
		pygame.draw.rect(screen, (255,255,255),[i[0],i[1],i[2],i[3]])

def game_loop():

	global score
	global mod 
	global lives
	global scoremod
	global prevtime

	centre = (width*0.45,height*0.8)
	radius = 77
	angle = [0,180]
	theta = [radians(angle[0]),radians(angle[1])]
	omega = 6

	starting = ((round(centre[0]+ radius*cos(theta[0])),round(centre[1] + radius*sin(theta[0]))),(round(centre[0]+ radius*cos(theta[1])),round(centre[1] + radius*sin(theta[1]))))
	ball1 = [centre[0]+ radius*cos(theta[0]),centre[1] + radius*sin(theta[0])]
	ball2 = [centre[0]+ radius*cos(theta[1]),centre[1] + radius*sin(theta[1])]

	thing_startx = 0
	thing_starty = 0 
	thing_width = 0
	
	exitGame = False
	count = 0

	pygame.key.set_repeat(1, 10)

	things = []

	while not exitGame:
		omega = 6
		pygame.event.pump()

		score = (pygame.time.get_ticks()-prevtime)//scoremod
		if score%50 == 0 and mod>40:
			mod -= 2 					#Increasing difficulty with increasing score
		
		if count%mod == 0 :
			count = 0
			thing_width = random.randint(130,170)
			ch = random.randint(0,3)
			thing_speed = random.randint(4,6)
			# thing(x, y, w, h, color=[(255,255,255)])
			if ch == 0:
				thing_startx = 0
				thing_starty = 0 
				things.append([thing_startx,thing_starty,thing_width+10,25,thing_speed])
			elif ch == 1:
				thing_startx = width - thing_width + 25
				thing_starty = 0
				things.append([thing_startx,thing_starty,thing_width+10,25,thing_speed])
			elif ch == 2:
				thing_startx = -50
				thing_starty = 0 
				things.append([thing_startx,thing_starty,thing_width-20,25,thing_speed])
				thing_startx = width - thing_width + 25
				thing_starty = 0
				things.append([thing_startx,thing_starty,thing_width,25,thing_speed])

		for i in range(len(things)):
			if things[i][1] > height:
				print(i)
				things.pop(i)


		for event in pygame.event.get():	
			# Event handling loop that contains all the inputs and events
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:	
				if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
					pygame.quit()
					quit()
				ball1[0] = centre[0] + radius*cos(theta[0]) 
				ball1[1] = centre[1] + radius*sin(theta[0])	
				ball2[0] = centre[0] + radius*cos(theta[1]) 
				ball2[1] = centre[1] + radius*sin(theta[1])
				
				if event.key == pygame.K_LEFT:
					angle[0] -= omega
					angle[1] -= omega
					theta[0] = radians(angle[0])
					theta[1] = radians(angle[1])
				elif event.key == pygame.K_RIGHT:
					angle[0] += omega
					angle[1] += omega
					theta[0] = radians(angle[0])
					theta[1] = radians(angle[1])
				elif event.key == pygame.K_p:
					print("pause")
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					ball1 *=1
					ball2 *=1

		count += 1
		screen.fill((0,0,0))
		# pygame.draw.circle(screen, color, (x,y), radius, thickness)
		pygame.draw.circle(screen,(105,105,105),(round(centre[0]+10),round(centre[1])+10),radius+2,1)
		displaythings(things)

		for i in things:
			i[1] += i[4] # thing_speed
			if i[1] >= height:
				things.pop(things.index(i))

		screen.blit(blue_ball,(round(ball1[0]),round(ball1[1])))
		screen.blit(red_ball,(round(ball2[0]),round(ball2[1])))

		try:
			if screen.get_at((round(ball1[0]),round(ball1[1]))) == ((255,255,255,255)) or screen.get_at((round(ball2[0]),round(ball2[1]))) == ((255,255,255,255)):
				lives -= 1

				pygame.mixer.Channel(1).play(pygame.mixer.Sound('Crash2.ogg'))
				pygame.mixer.Channel(1).set_volume(2)
				pygame.time.wait(100)

				flag = False
				if lives == 0:	
					f = open("Highscore.txt","r")
					hs = int(f.readline())
					f.close()
					if hs < score:
						f = open("Highscore.txt","w")
						flag = True
						f.write(str(score))
						f.close()
					else:
						pygame.mixer.Channel(2).play(pygame.mixer.Sound('final.ogg'))
						pygame.event.pump()
						time.sleep(0.02)
					score = 0
					
					


				i = 0
				while True:
					if len(things)==0 and ((starting[0][0]==round(ball1[0]) and starting[0][1]==round(ball1[1])) or (starting[1][0]==round(ball2[0]) and starting[1][1]==round(ball2[1]))):
						break
					
					ball1[0] = centre[0] + radius*cos(theta[0]) 
					ball1[1] = centre[1] + radius*sin(theta[0])	
					ball2[0] = centre[0] + radius*cos(theta[1]) 
					ball2[1] = centre[1] + radius*sin(theta[1])	
					angle[0] -= omega
					angle[1] -= omega
					theta[0] = radians(angle[0])
					theta[1] = radians(angle[1])

					screen.fill((0,0,0))	
					# pygame.draw.circle(screen, color, (x,y), radius, thickness)
					pygame.draw.circle(screen,(105,105,105),(round(centre[0]+10),round(centre[1])+10),radius+2,1)

					screen.blit(blue_ball,(round(ball1[0]),round(ball1[1])))
					screen.blit(red_ball,(round(ball2[0]),round(ball2[1])))
					
					displaythings(things)
					score = (pygame.time.get_ticks()-prevtime)//scoremod
					score_display(score)
					lives_display(lives)
					
					if lives == 0 and i != 256 and (not flag):
						font = pygame.font.SysFont("helvetica",20)
						f = open("Captions.txt","r")
						text = font.render(f.readline(), True, (255-i,255-i,255-i))
						f.close()
						textrect = text.get_rect()
						textrect.center = ((width*0.5),(height*0.65))
						screen.blit(text,textrect)
						i += 2
					elif lives == 0 and i!=256 and flag:
						font = pygame.font.SysFont("helvetica",30)
						text = font.render("Highscore!", True, (255-i,255-i,255-i))
						f.close()
						textrect = text.get_rect()
						textrect.center = ((width*0.5),(height*0.65))
						screen.blit(text,textrect)
						i += 2
						time.sleep(0.01)

					pygame.display.flip()
					clock.tick()
					pygame.event.pump()
					time.sleep(0.01)
					for z in things:
						z[1] -= 2*z[4] # thing_speed
						if z[1] < 0:
							things.pop(things.index(z))	

					
					if lives == 0 and i!=256:
						continue

				if lives == 0:
					lives = 3
					prevtime = pygame.time.get_ticks()
				pygame.event.clear()
				game_loop()
		except IndexError:
				print(end="")
		score_display(score)
		lives_display(lives)
		pygame.display.update()
		clock.tick(1000)	# Frames per second

message_display("Headphones reccommended",25)
score = 0
lives = 3
mod = 50
prevtime = pygame.time.get_ticks()
scoremod = 500

game_loop()

pygame.quit()
quit()
