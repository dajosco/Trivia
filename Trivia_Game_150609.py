##############################################################################################################
# LUMMA - TRIVIA
#
# Description of the Game:
# - There are 2 teams
# - A question is presented to both teams at the same time along with three different answers to choice from
# - A person in each team has to push one of the three push buttons where each one belongs to a choice
# - If no answer is received in a lapse of 30sec. no points will be accredited to the team.
# - Each team is credited with 10 points per correct answer and 5 extra points to be the first one to answer
# - Wins the team with more points
#
# Author: Daniel J. Scokin
# Version: 1.00
# Date: May-2015
#############################################################################################################

__author__ = "Rob Knight, Gavin Huttley, and Peter Maxwell"
__credits__ = ["Daniel Scokin", "Marcos Franco"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Daniel Scokin"
__email__ = "dajosco@gmail.com"
__status__ = "development"

from time import sleep
import sys
import os
import random
import signal
import pifacedigitalio as piface
import pygame
from pyomxplayer import OMXPlayer

#Each element contains the correct answer to each one of the questions in numerical order
Question_Answer = [1, 1, 2, 3, 2, 1, 3, 1, 1, 2, 2, 3, 1, 2, 3]

sandclock2=("-","\\","|","/")
sandclock=("<-  ","<-- ","<---"," <--","  <-"," <--","<---","<-- ")

#PiFace declaration
pf = piface.PiFaceDigital()
listener = piface.InputEventListener(chip=pf)

Team1Option=0
Team2Option=0
firstteam=0
Team1_Score=0
Team2_Score=0
screen=0
movie=0

#Dictionary of images and videos
screen_dict = {
				"invitacion_a_jugar"	  	: "Trivia_video0.mpg", 
				"invitacion_a_jugar_rojo" 	: "Trivia_video1.mpg",
				"invitacion_a_jugar_azul" 	: "Trivia_video2.mpg",
				"explicar_juego"		  	: "Trivia_video3.mpg",
				"pregunta_1"				: "Trivia_Foto4.png",   	# cambiar a jpg
				"pregunta_2"				: "Trivia_Foto5.png",		# cambiar a jpg
				"pregunta_3"				: "Trivia_Foto6.png",		# cambiar a jpg
				"video_pregunta_1"			: "Trivia_video7.mpg",
				"video_pregunta_2"			: "Trivia_video8.mpg",
				"video_pregunta_3"			: "Trivia_video9.mpg",
				"correcto_azul"				: "Trivia_foto10.jpg",
				"correcto_rojo"				: "Trivia_foto11.jpg",
				"correcto_ambos"			: "Trivia_foto12.jpg",
				"incorrecto_ambos"			: "Trivia_foto13.jpg",
				"respondio_primero_azul"	: "Trivia_foto14.jpg",
				"respondio_primero_rojo"	: "Trivia_foto15.jpg",
				"gano_azul"					: "Trivia_video16.mpg",
				"gano_rojo"					: "Trivia_video17.mpg",
				"empate"					: "Trivia_video18.mpg",
				"puntajes_finales"			: "Trivia_foto19.jpg"
			  }

current_question = -1       #Stores the question being asked

def init_screen():
	global screen
	
	disp_no = os.getenv("DISPLAY")
	if disp_no:
		print "I'm running under X display = {0}".format(disp_no)
	else:
		print "I'm NOT running undex X display = {0}".format(disp_no)

		# Check which frame buffer drivers are available
	#Start with fbcon since directfb hangs with composite output
	# drivers = ['fbcon', 'directfb', 'svgalib']
	
	# found = False
	
	# for driver in drivers:
	#	Make sure that SDL_VIDEODRIVER is set
		# if not os.getenv('SDL_VIDEODRIVER'):
			# os.putenv('SDL_VIDEODRIVER', driver)
		
		# try:
	#		See problem with: http://stackoverflow.com/questions/17035699/pygame-requires-keyboard-interrupt-to-init-display
			# print("Trying driver: %s" % (driver))
	pygame.display.init()
		# except pygame.error:
			# print 'Driver: {0} failed.'.format(driver)
			# continue
		
		# found = True
		# break

	# if not found:
		# raise Exception('No suitable video driver found!')
		
	size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
	print "Framebuffer size: %d x %d" % (size[0], size[1])
	
	screen = pygame.display.set_mode(size) #, pygame.FULLSCREEN)
	
	# Clear the screen to start
	screen.fill((0, 0, 0))        
	# Initialise font support
	pygame.font.init()
	# Render the screen
	pygame.display.update()
	
######################################################################################
# ButtonPressed
# Interruption event handler for PiFace IO card
def ButtonPressed(event):
	
	global Team1Option
	global Team2Option
	global firstteam
	
	TeamButton=""

	#IF TEAM1 pressed a button
	if event.pin_num>=0 and event.pin_num<=2:
		if Team1Option==0:
			Team1Option=event.pin_num+1
			if Team2Option==0:
				firstteam=1
				
			pf.leds[0].turn_off()
			pf.leds[1].turn_off()
			pf.leds[2].turn_off()
			pf.leds[event.pin_num].turn_on()
			#printxy(2,5,"Team 1 Option:%d" % (Team1Option))
	
	#IF TEAM2 pressed a button
	if event.pin_num>=3 and event.pin_num<=5:
		if Team2Option==0:
			Team2Option=event.pin_num-2			#adjust for pin possition
			if Team1Option==0:
				firstteam=2
				
			pf.leds[3].turn_off()
			pf.leds[4].turn_off()
			pf.leds[5].turn_off()
			pf.leds[event.pin_num].turn_on()

######################################################################################
# Wait_for_Key
# wait until a pushbutton is pressed a returns which team has pressed it.
def Wait_for_Key(x,y,message_on_screen):
	sandclockindex=0
	global movie
	global firstteam
	
	firstteam=0
			
	while firstteam==0:
		try:
			printxy(x,y,"%s %s"                       % (message_on_screen,sandclock[sandclockindex]))
		except:
			print("Unexpected error %s" % sys.exc_info()[0])
			exit()
					
		sandclockindex+=1
		if sandclockindex >= len(sandclock):
			sandclockindex=0
#		if not movie.get_busy():
#			movie.rewind()
#			movie.play()
			
		sleep(.1)
	
	return firstteam



######################################################################################
# Init_vars
# Initialize global variables
def init_vars():
	global firstteam,Team1Option,Team2Option
	
	firstteam=0
	Team1Option=0
	Team2Option=0

######################################################################################
# update_scr
# Updates terminal screen info
def update_scr(question_num, question_code, timeout_tmr, sandclockindex):

	global firstteam
	global Team1Option
	global Team2Option
	global sandclock2
	global Team1_Score
	global Team2_Score

	os.system('clear')
	
	printxy(2,2,"Question #%d - Question Code %s" %(question_num,question_code))
	printxy(2,4,"Clock: %d  %s" %(timeout_tmr, sandclock2[sandclockindex]))
	printxy(2,6,"Team 1 Option:%d     Score:%d" %(Team1Option,Team1_Score))
	printxy(2,7,"Team 2 Option:%d     Score:%d" %(Team2Option,Team2_Score))
	printxy(2,8,"First Team to answer: %d" %(firstteam))
	
	
######################################################################################
# Print XY 
# Print text @ X,Y coordenates of the screen
def printxy(x, y, text):
	sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
	sys.stdout.flush()
 
######################################################################################
# Choose Question
# Randomly selectects a question and verifies that has not being asked in the same game
def choose_question(question_array,question_executed):
	current_question = 0
	loop_count = 0

	while True:
		current_question = random.randrange(0, len(question_array))

		loop_count += 1

		if question_executed[current_question] == 0:
			break

		if loop_count > (len(question_array) + 1):		#Ensure that goes through all the questions
			print("Something went wrong! Stuck inside subrutine: %s %d times" % ('Choose_Question', loop_count))
			break

	question_executed[current_question] = 1
	return current_question

######################################################################################
# Initialize Question Table
# Sets all the question executed flags to 0
def initialize_question_table(question_array):
	for x in range(0, len(question_array)):
		question_array[x] = 0

######################################################################################
# Stop
# Stops execution of the game and go back to OS
def stop():
	global pf
	global movie
	
	printxy (2,18,"got KeyboardInterrupt, stopping.")
	pf.output_pins[7].turn_off()
	movie.stop()
	pygame.quit()
	listener.deactivate()
	pf.deinit_board()
	sys.exit()
	
######################################################################################
# Main
# Main subrutine
def main():

	global Team1Option
	global Team2Option
	global firstteam
	global Team1_Score
	global Team2_Score
	global screen
	global movie
	
	Team1_Score = 0
	Team2_Score = 0	
	Team_color= ("Ambos","Azul","Rojo")
	_Rojo = (255,0,0)
	_Azul = (0,0,255)
	
	#Configure interrupt handlers for inputs 0 to 5 
	#which are connected to the teams push buttons options
	#Team 1 : Azul
	listener.register(0,piface.IODIR_FALLING_EDGE, ButtonPressed)	# Team 1 - Option A
	listener.register(1,piface.IODIR_FALLING_EDGE, ButtonPressed)	# Team 1 - Option B
	listener.register(2,piface.IODIR_FALLING_EDGE, ButtonPressed)	# Team 1 - Option C
	#Team 2 : Rojo
	listener.register(3,piface.IODIR_FALLING_EDGE, ButtonPressed)	# Team 2 - Option A
	listener.register(4,piface.IODIR_FALLING_EDGE, ButtonPressed)	# Team 2 - Option B
	listener.register(5,piface.IODIR_FALLING_EDGE, ButtonPressed)	# Team 2 - Option C
	
	#Activate the interrupt handler
	listener.activate()
	
	#Create an array of flags. Each element indicates if that question was already asked or not,
	#to avoid repeating the same question during a game session
	question_executed = [0] * len(Question_Answer)
	
	#Clear console screen
	os.system('clear')
	
	init_screen()

	#TODO: Play video: "invitacion_a_jugar"
	#TODO: Wait of any of the Teams to press a key
	
	##########
	printxy(2,0,"Play video: Invitacion a Jugar!")
	omx = OMXPlayer("media/Trivia_Video0.mp4")
	movie = pygame.movie.Movie('media/Trivia_Video6.mpg')
	screen = pygame.display.set_mode((1920,1080))#movie.get_size())#,pygame.FULLSCREEN)
	movie_screen = pygame.Surface(movie.get_size()).convert()
	movie.set_display(movie_screen)
#	movie.play()
#	playing = True
#	while playing:
#		for event in pygame.event.get():
#			if event.type == pygame.QUIT:
#				movie.stop()
#				playing = False
#
#		screen.blit(movie_screen,(0,0))
#		pygame.display.update()
#		clock.tick(FPS)

#	pygame.quit()
	#movie = pygame.movie.Movie('media/hst_1.mpg')
#	movie.play()
	
#	while movie.get_busy():
#		for event in pygame.event.get():
#			if event.type == pygame.KEYDOWN:
#				movie.stop()				
#		pygame.quit()
	
	
	init_vars()
	firstteam=Wait_for_Key(2,1,"Waiting for a Team to accept playing !   ")
#	movie.stop()
	omx.stop()
	
	#TODO: Detect which team pressed a key 
	if firstteam==1:
		#play video: invitacion_a_jugar_rojo
		wait_for_team=2
		omx = OMXPlayer("media/Trivia_Video1.mp4")
	else:
		#play video: invitacion_a_jugar_Azul
		wait_for_team=1
		omx = OMXPlayer("media/Trivia_Video2.mp4")
	printxy (2,3,"Team %s is on!" %(Team_color[firstteam]))
	
	init_vars()
	firstteam=0

##########
	#movie = pygame.movie.Movie('media/Trivia_Video0.mpg')
	#movie = pygame.movie.Movie('media/hst_1.mpg')
	#movie.play()
	
	while firstteam<>wait_for_team:
		init_vars()
		#TODO: Play invitacion_a_jugar_rojo o invitacion_a_jugar_Azul depending on who already pressed a button
		firstteam=Wait_for_Key(2,5,"Waiting for Team %s to accept!         " % (Team_color[wait_for_team]))
		
	#movie.stop()
	omx.stop()
	
#	while firstteam<>wait_for_team:
#		init_vars()
#		#TODO: Play invitacion_a_jugar_rojo o invitacion_a_jugar_Azul depending on who already pressed a button
#		firstteam=Wait_for_Key(2,5,"Waiting for Team %s to accept!         " % (Team_color[wait_for_team]))
		
					
		
	printxy (2,8,"Team %s accepted the challenge!" % (Team_color[wait_for_team]))
	omx = OMXPlayer("media/Trivia_Video3.mp4")
	printxy (2,10,"Play video - Explicar Juego!")
	sleep(5)
	
	#TODO: Play video: explicar_juego
	
	#Ask 3 questions
	for x in range(1, 4):
		
		init_vars()
		timeout_tmr=0
		sandclockindex=0
		
		current_question = choose_question(Question_Answer,question_executed)

		# initialize round scores
		Team1_Round_Score = 0
		Team2_Round_Score = 0
		
		background = pygame.image.load('media/'+screen_dict['pregunta_%d' % (x)]).convert_alpha()
		background = pygame.transform.scale(background , (1920,1080))
	
		font = pygame.font.SysFont("renegademaster", 150, bold = 0)
		
		
		while Team1Option==0 or Team2Option==0:
			update_scr(x,current_question+1,timeout_tmr, sandclockindex)
			timeout_tmr+=1
		
			pf.output_pins[7].toggle()
		
			sleep(1)
			sandclockindex+=1
			if sandclockindex>=len(sandclock2):
				sandclockindex=0
		
			if timeout_tmr>30:
				if Team1Option==0:
					Team1Option=99
				if Team2Option==0:
					Team2Option=99
		
			count_down = font.render("{:02d}".format(timeout_tmr),True, (255,255,0)) 
			count_down_pos = count_down.get_rect()
			count_down_pos.centerx = background.get_rect().centerx
			count_down_pos.centery = 900

			screen.blit(background, (0, 0))
			screen.blit(count_down, count_down_pos)
			pygame.display.update()
			
			update_scr(x,current_question+1,timeout_tmr, sandclockindex)
		
		# Calculate the scores for Team1
		if Team1Option == Question_Answer[current_question]:
			Team1_Round_Score = 10
			if firstteam == 1:
				Team1_Round_Score += 5

		# Calculate the scores for Team2
		if Team2Option == Question_Answer[current_question]:
			Team2_Round_Score = 10
			if firstteam == 2:
				Team2_Round_Score += 5

		# Set the winner
		if Team1_Round_Score > Team2_Round_Score:
			Round_Winner = 1
		elif Team1_Round_Score < Team2_Round_Score:
			Round_Winner = 2
		else:
			Round_Winner = 0

		# Accumulate the total scores
		Team1_Score += Team1_Round_Score
		Team2_Score += Team2_Round_Score

		# Present the correct answer
		printxy(2,10,'Pregunta #%d  Code %d - correct Answer: %d' % (
		x, current_question + 1, Question_Answer[current_question]))

		# Present who was the winner
		if Round_Winner > 0:
			printxy(2,12,"Playing: Video %d: Equipo %d wins this round" % (Round_Winner+6,Round_Winner))
		else:
			if Team1Option==99 and Team2Option==99:
				printxy(2,12,"Playing: Video x: Time Out! nadie respondio")
			else:
				printxy(2,12,"Playing: Video 6: Respondieron ambos incorrectamente")

		
		#printxy(2,12,"Question #%d  Question Code %d - correct Answer: %d" % (x, current_question + 1, Question_Answer[current_question]))
		printxy(2,14,"Team 1 Score=%d" % (Team1_Score))
		printxy(2,15,"Team 2 Score=%d" % (Team2_Score))

		printxy(2,18,"Play video: Explicacion pregunta %d" % (current_question+1))
		omx = OMXPlayer("media/Trivia_Video%d.mp4" % (x+6))
		sleep(10)

	os.system('clear')
	printxy(2,2,"=============================================================")
	if Team1_Score>Team2_Score:
		printxy(2,4,'TEAM 1 is the Winner!!! with %d over %d' % (Team1_Score, Team2_Score))
	elif Team1_Score<Team2_Score:
		printxy(2,4,"TEAM 2 is the Winner!!! with %d over %d" % (Team2_Score, Team1_Score))
	else:
		printxy(2,4,"Tie : both team with Team 1=%d and Team 2=%d" % (Team1_Score, Team2_Score))
	printxy(2,6,"=============================================================")

	printxy(2,8,Question_Answer)
	printxy(2,9,question_executed)
	stop()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		stop()