
#Each element contains the correct answer to each one of the questions in numerical order
#Can be added any amount of questions as long we have enough memory ;-)
question_answer = [3, 3, 2] 	#3, 2, 1, 3, 1, 1, 2, 2, 3, 1, 2, 3]

#########################################################################
# Images and Videos
#########################################################################
#Dictionary of images and videos:
#first column represents the reference name. "DO NOT MODIFY!!!"
#second column stores the real name of the file containing either the 
#movie or image. It can be modified as needed
#ALL THE MEDIA FILES SHALL BE IN A FOLDER CALLED "media"
#TODO: set in a different file
screen_dict = {
				"invitacion_a_jugar"	  		: "media/Trivia_Video0.mp4", 
				"invitacion_a_jugar_rojo" 	: "media/Trivia_Video1.mp4",
				"invitacion_a_jugar_azul" 	: "media/Trivia_Video2.mp4",
				"explicar_juego"		  			: "media/Trivia_Video3.mp4",
				"pregunta_1"						: "media/Trivia_Foto4.png",   	
				"pregunta_2"						: "media/Trivia_Foto5.png",		
				"pregunta_3"						: "media/Trivia_Foto6.png",		
				"video_pregunta_1"			: "media/Trivia_Video7.mp4",
				"video_pregunta_2"			: "media/Trivia_Video8.mp4",
				"video_pregunta_3"			: "media/Trivia_Video9.mp4",
				"correcto_azul"					: "media/Trivia_Foto10.jpg",
				"correcto_rojo"					: "media/Trivia_Foto11.jpg",
				"correcto_ambos"				: "media/Trivia_Foto12.jpg",
				"incorrecto_ambos"			: "media/Trivia_Foto13.jpg",
				"respondio_primero_azul"	: "media/Trivia_Foto14.jpg",
				"respondio_primero_rojo"	: "media/Trivia_Foto15.jpg",
				"gano_azul"						: "media/Trivia_Video16.mp4",
				"gano_rojo"						: "media/Trivia_Video17.mp4",
				"empate"							: "media/Trivia_Video18.mp4",
				"puntajes_finales"				: "media/Trivia_Foto19.jpg"
				}

#Screen Resolution
SCREEN_RESOLUTION = (1920,1080)

#SCORE Font 
SCORE_FONT 		= "renegademaster"
SCORE_FONT_SIZE = 150

#Team1 score text placement coordinates			  
TEAM1_SCORE_POS_X = 400
TEAM1_SCORE_POS_Y = 900
TEAM1_SCORE_TXT_COLOR = (255,0,0)		# RED # (RED,GREEN,BLUE) : 0-255

#Team2 score text placement coordinates
TEAM2_SCORE_POS_X = 1450
TEAM2_SCORE_POS_Y = 900
TEAM2_SCORE_TXT_COLOR = (0,0,255)		# BLUE # (RED,GREEN,BLUE) : 0-255

#COUNTDOWN Settings
COUNTDOWN_FONT 	= "renegademaster"
COUNTDOWN_FONT_SIZE = 150
COUNTDOWN_TXT_COLOR = (255,255,0)		# YELLOW # (RED,GREEN,BLUE) : 0-255
COUNTDOWN_POS_X = 960
COUNTDOWN_POS_Y = 900

#Sounds
SCORE_DING = "media/ding3.mp3"
COUNTDOWN_DING = "media/ding.mp3"


