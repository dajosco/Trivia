##############################################################################################################
# LUMMA - TRIVIA
#
# Description of the Game:
# - There are 2 teams
# - A question is presented to both teams at the same time along with three different answers to choice from
# - A person in each team has to push one of the three push buttons where each one belongs to a choice
# - If no answer is received in a lapse of 30sec no points will be accredited to the team.
# - Each team is credited with 10 points per correct answer and 5 extra points to be the first one to answer
# - Wins the team with more points
#
# Author: Daniel J. Scokin
# Version: 1.00
# Date: May-2015
#############################################################################################################

__author__ = ["Daniel Scokin"]
__credits__ = ["Daniel Scokin", "Marcos Franco", "LUMMA Team"]
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
Question_Answer = [3, 3, 2] #3, 2, 1, 3, 1, 1, 2, 2, 3, 1, 2, 3]

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
				"invitacion_a_jugar"	  	: "media/Trivia_Video0.mp4", 
				"invitacion_a_jugar_rojo" 	: "media/Trivia_Video1.mp4",
				"invitacion_a_jugar_azul" 	: "media/Trivia_Video2.mp4",
				"explicar_juego"		  	: "media/Trivia_Video3.mp4",
				"pregunta_1"				: "media/Trivia_Foto4.png",   	
				"pregunta_2"				: "media/Trivia_Foto5.png",		
				"pregunta_3"				: "media/Trivia_Foto6.png",		
				"video_pregunta_1"			: "media/Trivia_Video7.mp4",
				"video_pregunta_2"			: "media/Trivia_Video8.mp4",
				"video_pregunta_3"			: "media/Trivia_Video9.mp4",
				"correcto_azul"				: "media/Trivia_Foto10.jpg",
				"correcto_rojo"				: "media/Trivia_Foto11.jpg",
				"correcto_ambos"			: "media/Trivia_Foto12.jpg",
				"incorrecto_ambos"			: "media/Trivia_Foto13.jpg",
				"respondio_primero_azul"	: "media/Trivia_Foto14.jpg",
				"respondio_primero_rojo"	: "media/Trivia_Foto15.jpg",
				"gano_azul"					: "media/Trivia_Video16.mp4",
				"gano_rojo"					: "media/Trivia_Video17.mp4",
				"empate"					: "media/Trivia_Video18.mp4",
				"puntajes_finales"			: "media/Trivia_Foto19.jpg"
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
	# Start with fbcon since directfb hangs with composite output
	#drivers = ['fbcon', 'directfb', 'svgalib']
	
	#found = False
	
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
	
	screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
	
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

def turn_off_leds():
	pf.leds[0].turn_off()
	pf.leds[1].turn_off()
	pf.leds[2].turn_off()
	pf.leds[3].turn_off()
	pf.leds[4].turn_off()
	pf.leds[5].turn_off()

			
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
# Updates debug screen info
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
	#movie.stop()
	pygame.quit()
	listener.deactivate()
	pf.deinit_board()
	sys.exit()
	
def update_score(team1_score, team2_score ,background):

	_Rojo = (255,0,0)
	_Azul = (0,0,255)
	
	#Select the font used for the scores
	font = pygame.font.SysFont("renegademaster", 150, bold = 0)
	
	#Render the surface "TeamX_score_surface" that holds the text
	team1_score_surface = font.render("{:02d}".format(team1_score),True, _Azul) 
	team2_score_surface = font.render("{:02d}".format(team2_score),True, _Rojo)
	
	#get the text dimensions and calculate the final position of the text
	team1_score_pos = team1_score_surface.get_rect()
	team2_score_pos = team2_score_surface.get_rect()	
	#TODO: create parameters
	team1_score_pos.centerx = 400
	team1_score_pos.centery = 900
	team2_score_pos.centerx = 1450
	team2_score_pos.centery = 900
	
	#Paste the background on the screen
	screen.blit(background, (0, 0))
	#Paste the text on the screen at the desired position
	screen.blit(team1_score_surface, team1_score_pos)
	screen.blit(team2_score_surface, team2_score_pos)			
	#Update the screen
	pygame.display.update()

	
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
	
	Team_color= ("Ambos","Azul","Rojo")
	_Rojo = (255,0,0)
	_Azul = (0,0,255)
	
	turn_off_leds()
	
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
	
	#######################################
	# STEP 1: Invite to Play             
	#######################################
	#Initialize Graphic Screen
	init_screen()

	#Play Inviting to Play video
	printxy(2,0,"Play video: Invitacion a Jugar!")
	omx = OMXPlayer(screen_dict['invitacion_a_jugar'])

	#Initialize Game variables
	init_vars()
	#Wait until one of the teams presses a button
	firstteam=Wait_for_Key(2,1,"Waiting for a Team to accept playing !   ")
	
	#Stop Inviting to Play video
	omx.stop()

	#########################################################
	# STEP 2: Wait for the Other Team confirmation to play             
	#########################################################
	
	if firstteam==1:
		#play video: invitacion_a_jugar_rojo
		wait_for_team=2
		omx = OMXPlayer(screen_dict['invitacion_a_jugar_rojo'])
	else:
		#play video: invitacion_a_jugar_Azul
		wait_for_team=1
		omx = OMXPlayer(screen_dict['invitacion_a_jugar_azul'])
	
	printxy (2,3,"Team %s is on!" %(Team_color[firstteam]))
	
	init_vars()
	firstteam=0

	while firstteam<>wait_for_team:
		init_vars()
		#TODO: Play invitacion_a_jugar_rojo o invitacion_a_jugar_Azul depending on who already pressed a button
		firstteam=Wait_for_Key(2,5,"Waiting for Team %s to accept! %s        " % (Team_color[wait_for_team],screen_dict['invitacion_a_jugar_azul']))

	printxy (2,8,"Team %s accepted the challenge!"%Team_color[wait_for_team])
	
	omx.stop()

	#########################################################
	# STEP 3: Explain how to play this game
	#########################################################

	printxy (2,10,"Play video - Explicar Juego!")
	omx = OMXPlayer(screen_dict['explicar_juego'])
	
	#TODO: delay necesita ser igual a duracion del video
	sleep(10)
	omx.stop()
	
	#########################################################
	# STEP 4: Go through the questions
	#########################################################
	Team1_Score = 0
	Team2_Score = 0	
	
	
	#Ask 3 questions
	for x in range(1, 4):
		
		init_vars()
		timeout_tmr=30
		sandclockindex=0
		turn_off_leds()
		
		###################################################################
		# STEP 5: Select a question randomly and present it on the screen
		###################################################################		
		
		#Select one question randomly
		current_question = choose_question(Question_Answer,question_executed)

		#initialize round scores
		Team1_Round_Score = 0
		Team2_Round_Score = 0
		
		#Render to a surface "background" the question selected
		background = pygame.image.load(screen_dict['pregunta_%d' % (current_question+1)]).convert_alpha()
		background = pygame.transform.scale(background , (1920,1080))
		
		#Select the font used for the countdown timer
		font = pygame.font.SysFont("renegademaster", 150, bold = 0)
		
		#####################################################################
		# STEP 6: Wait for the answers of each team and start the countdown
		#####################################################################	

		#Wait until a team picks an option before the time runs out
		while Team1Option==0 or Team2Option==0:
			#update debug screen info
			update_scr(x,current_question+1,timeout_tmr, sandclockindex)
			
			#increase timeout timer in 1sec
			timeout_tmr-=1
		
			#Just make LED7 on Piface board toggle every second that passes to know that the system is alive!
			pf.output_pins[7].toggle()
		
			#Wait one second
			sleep(1)
			
			#Sandclock: is just an animation on the debug screen to know that the system is waiting
			#increase the sandclock pointer to control the animation
			sandclockindex+=1
			
			#reset pointer to loop back the animation
			if sandclockindex>=len(sandclock2):
				sandclockindex=0
			
			#If Time is up flag the teams that have not answered
			if timeout_tmr<=0:
				if Team1Option==0:
					Team1Option=99	#Team1 didn't answer on time
				if Team2Option==0:
					Team2Option=99	#Team2 didn't answer on time
		
			#Render the surface "count_down" that holds the text
			count_down = font.render("{:02d}".format(timeout_tmr),True, (255,255,0)) 
			
			#get the text dimensions and calculate the final position of the text
			count_down_pos = count_down.get_rect()
			count_down_pos.centerx = background.get_rect().centerx
			#TODO: create parameter
			count_down_pos.centery = 900

			#Paste the background on the screen
			screen.blit(background, (0, 0))
			#Paste the text on the screen at the desired position
			screen.blit(count_down, count_down_pos)
			#Update the screen
			pygame.display.update()
			
			#update the debug screen
			update_scr(x,current_question+1,timeout_tmr, sandclockindex)
		
		
		######################################
		# STEP 7: Show the correct answer 
		######################################

		#Clear the graphic screen
		screen.fill((0, 0, 0))	
		pygame.display.update()
		
		## Present the correct answer
		printxy(2,18,"Play video: Explicacion pregunta %d" % (current_question+1))
		omx = OMXPlayer(screen_dict['video_pregunta_%d' %(current_question+1)])

		printxy(2,10,'Pregunta #%d  Code %d - correct Answer: %d' % (
		x, current_question + 1, Question_Answer[current_question]))	
		
		#TODO: delay tiene que ser de la duracion del video de la pregunta
		sleep(10)
		omx.stop()
		
		Team1_Correct=False
		Team2_Correct=False
		
		# Who answered correctly?
		if Team1Option == Question_Answer[current_question]:
			Team1_Correct=True
		if Team2Option == Question_Answer[current_question]:
			Team2_Correct=True

		background_image = ""
		
		# Display the proper background	
		if   Team1_Correct and Team2_Correct:
			background_image = screen_dict['correcto_ambos']
		elif Team1_Correct and not Team2_Correct:
			background_image = screen_dict['correcto_azul']
		elif not Team1_Correct and Team2_Correct:
			background_image = screen_dict['correcto_rojo']
		else:
			background_image = screen_dict['incorrecto_ambos']
		
		#Render to a surface "background" the question selected
		background = pygame.image.load(background_image).convert_alpha()
		
		#Resize background to ensure it fills the screen
		background = pygame.transform.scale(background , (1920,1080))
		
		#Select the font used for the scores
		font = pygame.font.SysFont("renegademaster", 150, bold = 0)
		
		##########################################################
		# STEP 8: Calculate the scores and display on the screen
		##########################################################
		if Team1_Correct or Team2_Correct:	

			#count up to 10
			for score_board_counter in range(1,11):
			
				#Is the Team 1 Answer correct?
				if Team1_Correct:	
					Team1_Score += 1

				#Is the Team 2 Answer correct?
				if Team2_Correct:
					Team2_Score += 1

				update_score(Team1_Score,Team2_Score,background)

				#TODO: PLAY bing!!! sound
				sleep(.10)
				
			#Wait 5sec before jumping to the next step
			sleep(5)
			
			###########################################################
			# STEP 9: Give more point to the Team that answered first
			###########################################################
			
			#Render to a surface "background" with the team who answered first
			background = pygame.image.load(screen_dict['respondio_primero_%s'%(Team_color[firstteam].lower())]).convert_alpha()
			
			#Resize background to ensure it fills the screen
			background = pygame.transform.scale(background , (1920,1080))
			
			#Select the font used for the scores
			font = pygame.font.SysFont("renegademaster", 150, bold = 0)
			
			skip_section=False
			
			#count up to 5
			for score_board_counter in range(1,6):
			
				#Was Team 1 the first to Answer correctly?
				if firstteam == 1:
					if Team1_Correct:	
						Team1_Score += 1
					else:
						skip_section=True
						break
				
				#Was Team 2 the first to Answer correctly?
				if firstteam == 2:
					if Team2_Correct:	
						Team2_Score += 1
					else:
						skip_section=True
						break
				
				update_score(Team1_Score,Team2_Score,background)
				
				#TODO: PLAY bing!!! sound
				sleep(.10)

			#Wait 5sec before jumping to the next step
			if not skip_section:
				sleep(5)

		else:
			update_score(Team1_Score,Team2_Score,background)
			sleep(5)
				
		#Update debug screen with the scores
		printxy(2,14,"Team 1 Score=%d" % (Team1_Score))
		printxy(2,15,"Team 2 Score=%d" % (Team2_Score))

		
	###########################################################
	# STEP 10: Announce the Results: The winner is....
	###########################################################

	#Clear debug screen
	os.system('clear')
	printxy(2,2,"=============================================================")
	
	
	if Team1_Score>Team2_Score:
		#Team 1 is the winner
		#Update debug screen
		printxy(2,4,'TEAM 1 is the Winner!!! with %d over %d' % (Team1_Score, Team2_Score))
		
		#Play video: Winner Team #1
		omx = OMXPlayer(screen_dict['gano_%s' %(Team_color[1].lower())])
	
	elif Team1_Score<Team2_Score:
		#Team 2 is the winner
		#Update debug screen
		printxy(2,4,"TEAM 2 is the Winner!!! with %d over %d" % (Team2_Score, Team1_Score))
		
		#Play video: Winner Team #2
		omx = OMXPlayer(screen_dict['gano_%s' %(Team_color[2].lower())])
	
	else:
		# It's a TIE!
		#Update debug screen
		printxy(2,4,"Tie : both team with Team 1=%d and Team 2=%d" % (Team1_Score, Team2_Score))
		
		#Play video: It's a Tie!
		omx = OMXPlayer(screen_dict['empate'])

	printxy(2,6,"=============================================================")
	printxy(2,8,Question_Answer)
	printxy(2,9,question_executed)
	
	sleep(5)
	omx.stop()
	
	#Render to a surface "background" to show final scores
	background = pygame.image.load(screen_dict['puntajes_finales']).convert_alpha()
		
	#Resize background to ensureit fills the screen
	background = pygame.transform.scale(background , (1920,1080))
	update_score(Team1_Score,Team2_Score,background)
	
	
	#TODO: sleep duration mas be equal to the video length
	sleep(10)
	
	stop()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		stop()
