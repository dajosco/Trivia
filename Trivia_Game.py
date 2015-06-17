##############################################################################################################
# LUMMA - TRIVIA
#
# Author: Daniel J. Scokin
# Version: 1.00
# Date: May-2015

# Description of the Game:
# - There are 2 teams
# - A question is presented to both teams at the same time along with three different answers to choose from.
# - A person in each team has to push one of the three push buttons, where each one belongs to an answer.
# - If no answer is received in a lapse of 30sec. no points will be accredited to the team.
# - Each team is credited with:
#       - 10 points per correct answer
#       - 5 extra points to the first to answer
# - Wins the team with more points
#
#############################################################################################################
__author__ = 'dajosco'
import random
import os

# Number of questions to be ask during the game
Game_Questions = 3

# Each element contains the correct answer to each one of the questions in numerical order
Question_Answer = [1, 1, 2, 3, 2, 1, 3, 1, 1, 2, 2, 3, 1, 2, 3]

# Flag to avoid repeating questions
Question_executed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


######################################################################################
# Choose Qustion
# Randomly selectects a question and verifies that has not bein asked in the same game
def Choose_Question():
	current_question = 0
	loop_count = 0

	while True:
		current_question = random.randrange(0, len(Question_Answer))

		loop_count += 1

		if Question_executed[current_question] == 0:
			break

		if loop_count > (Game_Questions + 1):
			print("Something went wrong! Stuck inside subrutine: %s %d times" % ('Choose_Question', loop_count))
			break

	Question_executed[current_question] = 1
	return current_question


######################################################################################
# Initialize Question Table
# Sets all the question executed flags to 0
def Initialize_Qestion_table():
    for x in range(0, len(Question_Answer)):
        Question_executed[x] = 0


######################################################################################
# Main
# Main subrutine
def main():
	Team1_Score = 0
	Team2_Score = 0
	current_question = -1  # Stores the question being asked
	QuienJuega=0
	
    #### for Simulation
	Team2_Table = {'q': 1, 'w': 2, 'e': 3}

	Initialize_Qestion_table()  # clears all the flags
	
	print ("\033c")
	 
	print ("\n \n \n Playing: Video 0: Invitacion a jugar equipo Rojo / Azul \n")
	QuienJuega = raw_input ("[A]zul o [R]ojo : ")

	if QuienJuega == 'A':
		print ("Playing: Video 1: invitacion a jugar Equipo Rojo - Tenemos a Azul \n")
	else:
		print ("Playing: Video 2: invitacion a jugar Equipo Azul - Tenemos a Rojo \n")
	
	QuienJuega = raw_input("[A]zul o [R]")
	
	print ("\nPlaying: Video 2b: VIDEO REGLAS... \n")
	
	
    # Ask 3 questions
	for x in range(1, Game_Questions + 1):
		current_question = Choose_Question()

		
		print("-----------------------------------------------------------\n"
			"Playing: Video %d\n"
			"Pregunta #%d  codigo %d" % (x+8,x, current_question + 1))

        #### TODO: replace simulation by actual inputs
        #### For Simulation, will be replaced with pushbuttons

		Teams_Answers = ""

		while len(Teams_Answers) < 2:
			Teams_Answers = raw_input("\nTeam 1 answers with (1,2,3)\nTeam 2 answers with (Q,W,E)\n")
			
		First_Answer = Teams_Answers[0]
		Second_Answer = Teams_Answers[1]

        # Findout who replayed first
		if First_Answer.isdigit():
			First_Team_to_Answer = 1
			Team1_Answer = int(First_Answer)
			Team2_Answer = Team2_Table[Second_Answer]
		else:
			First_Team_to_Answer = 2
			Team1_Answer = int(Second_Answer)
			Team2_Answer = Team2_Table[First_Answer]
        #### End Simulation

        ###TODO: Real Inputs
        # There would be 2 groups of 3 inputs each
        # The code should detect the first input set on each group
        # and to take it as the desired answer for that team
        # - Identify which input on each group was activated first
        # - Identify which group was activated first
        # - Debouce
        # - If between the group no input is detected in 30sec, signal timeout.
        # - Once an option is pressed in a group it won't take in consideration the rest

        # initialize round scores
		Team1_Round_Score = 0
		Team2_Round_Score = 0

		# Calculate the scores for Team1
		if Team1_Answer == Question_Answer[current_question]:
			Team1_Round_Score = 10
			if First_Team_to_Answer == 1:
				Team1_Round_Score += 5

		# Calculate the scores for Team2
		if Team2_Answer == Question_Answer[current_question]:
			Team2_Round_Score = 10
			if First_Team_to_Answer == 2:
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
		print('\Pregunta #%d  Code %d - correct Answer: %d' % (
		x, current_question + 1, Question_Answer[current_question]))

        # Present who was the winner
		if Round_Winner > 0:
			print("\nPlaying: Video %d: Equipo %d wins this round" % (Round_Winner+6,Round_Winner))
		else:
			print("\nPlaying: Video 6: Respondieron ambos incorrectamente")

        # Present partial scores
		print('\nTeam 1 Score=%d points\nTeam 2 Score=%d points\n' % (Team1_Score, Team2_Score))

    # End of the Game
    # Present the winner of the Game and the points
	print("=============================================================")
	if Team1_Score > Team2_Score:
		print('  TEAM 1 is the Winner!!! with %d over %d' % (Team1_Score, Team2_Score))
	elif Team1_Score < Team2_Score:
		print("  TEAM 2 is the Winner!!! with %d over %d" % (Team2_Score, Team1_Score))
	else:
		print("  It's a Tie!!! : Team 1 = %d points   and   Team 2 = %d points" % (Team1_Score, Team2_Score))
	print("=============================================================")

    # Show the question tables
	print("\n")
	print(Question_Answer)
	print(Question_executed)


if __name__ == "__main__":
	main()
