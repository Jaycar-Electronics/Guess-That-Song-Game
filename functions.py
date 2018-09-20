from config import find_player, players
from pygame import mixer
from appJar import gui
import time
import eyed3

# functions.py
'''
	This file defines all (most) of the functions of the game
	different things that need to be managed
	such as when to start the count-down and pause the music and etc.

	Ideally, this would be combined 
	to make an "game" object
	which is then the controller to the whole process
	but we'll do it this way for now, maybe later versions might do the above
'''

# initialise the pygame mixer plugin, which handles playing music
mixer.init()

# gs is our game state machine, it will handle all the information to pass between different screens and etc
gs = {
	'countdown': 5,		# initiall countdown
	'state': 'stopped', # game switch sets what state the game is in 
	'all_controllers': 'off', # don't accept controller input
	'player': None,		# no selected Player
	'controller': None,			# no selected controller
	'scores':{			# player scores
		'1':0,
		'2':0,
		'3':0,
		'4':0,
	},
	'about':'Created by Jaycar Electronics', # promo
	'song': '',			# current playing song
	'artist': '',		# current playing artist
	'app': None
}



def display_hidden_song():
	gs['app'].setLabel('song_name','')
	gs['app'].setLabel('guess',"What's this song?")
	gs['app'].setLabel('player_spotlight','Waiting for button press')

def display_song(name,artist,player):
	gs['app'].setLabel('song_name',name) #show the song name
	gs['app'].setLabel('song_artist',artist) # show the song artist

	gs['app'].setLabel('player_spotlight',
		'Did Player {} get it correct? Enter Key for yes, Space for No'
		.format(player))

def display_countdown(time):
	gs['app'].setLabel('song_name','  ...'+str(time))
	gs['app'].setLabel('player_spotlight','')
	gs['app'].setLabel('guess','Get Ready')

def display_correct(player):
	gs['app'].setLabel('song_name','CORRECT! Player {} gains 1 point'.format(gs['player']))
	gs['app'].setLabel('guess','yey!')
	gs['app'].setLabel('song_artist','')
	gs['app'].setLabel('player_spotlight', 'Good work smarty pants')
	#add history for end of game
	gs['app'].setTextArea('history','{} {} CORRECT\n'.format(gs['song'] , 'P'+str(gs['player'])),end=False)

def display_incorrect(player):
	gs['app'].setLabel('song_name','INCORRECT! Player {} loses 1 point'.format(gs['player']))
	gs['app'].setLabel('guess','uh oh')
	gs['app'].setLabel('song_artist','')
	gs['app'].setLabel('player_spotlight', 'better luck next time')
	#add history for end of game
	gs['app'].setTextArea('history','{} {} WRONG\n'.format(gs['song'] , 'P'+str(gs['player'])),end=False)

def modify_scores(player,points):
	gs['scores'][player] += points


def spotlight(player):
	gs['app'].setLabel('player_spotlight',
		'Player {} has the spotlight'.format(player))
	mixer.music.pause()

def cancel_spotlight():
	mixer.music.unpause()
	turnoff_lights()
	gs['app'].setLabel('player_spotlight',
		'Player {} passed back, playing for next player'.format(gs['player']))
	gs['player'] = None
	gs['controller'] = None
	gs['all_controllers'] = 'on'
	
def process_game():
	''' process function
		used for handling the game state every second
		and setting the correct data on the gui
	
	'''

	# =============================
	# countdown state
	# =============================
	# starting up the game with a simple countdown timer
	if gs['state'] == 'countdown':
		
		if gs['countdown'] > 0:
			
			#function to manage the countdown display
			display_countdown(gs['countdown'])

			gs['countdown'] -= 1

			time.sleep(1) #functions should not "sleep" for a second but this is quick and dirty

		else: # it's countdown and reached 0
			load_new_song()

	# =============================
	# playing state
	# =============================
	# playing song, waiting for a player to hit the buzzer and tell us what the song is 
	elif gs['state'] == 'playing':

		# playing for button press here, don't do anything until we caught a controller
		if gs['player'] is not None: 

			spotlight(gs['player']) # spotlight the player, pause music

			gs['state'] = 'spotlight'


	# =============================
	# spotlight state
	# =============================
	# a player has the spotlight, all eyes on the player to make the right suggestion
	elif gs['state'] == 'spotlight' :

		if gs['controller'][1].is_pressed:	#check if button is pressed while in spotlight
			
			#dirty way of blocking until they release the button	
			while(gs['controller'][1].is_pressed):
				time.sleep(0.2) 
			
			#pass back to open
			cancel_spotlight()
			gs['state'] = 'playing'
		

	# =============================
	# reveal state
	# =============================
	# show the song name and artist, asks if they got it right or not
	elif gs['state'] == 'reveal':

		display_song(gs['song'],
					gs['artist'],
					gs['player'])

		gs['state'] = 'showdown'
	
	# =============================
	# prepare state
	# =============================
	# this is a filler, don't do anything here, we're playing for another keypress to load next song
	elif gs['state'] == 'prepare':
		pass

def key_press(key):

	if gs['state'] == 'spotlight':
		gs['state'] = 'reveal'

	elif gs['state'] == 'playing': 
		if key in [str(x) for x in range(3)]:
			button_bootstrap(key)

	elif gs['state'] == 'showdown':

		player = str(gs['player'])

		if key == '<Return>': #song correct, pressed enter key
			display_correct(player)
			modify_scores(player, 1)

		elif key == '<space>': # song incorrect, press space bar
			display_incorrect(player)
			modify_scores(player,-1)

		else:
			#some other key was presssed, disregard completely, skip the next bit of code
			return	

		gs['state'] = 'prepare' #go in to prepare state, which does nothing, to catch the next if below on keypress

	elif gs['state'] == 'prepare':  # we've shown the scores and
									# it's another keypress
		load_new_song()				# so load new song.

			
def load_new_song():

	if len(gs['songlist']) == 0:
		#out of songs, time to quit
		show_scores()
		return

	#load the song, start playing
	mp3filepath = gs['songlist'].pop()
	
	mp3tags = eyed3.load(mp3filepath)
	mp3tags = mp3tags.tag
	mixer.music.load(mp3filepath)
	mixer.music.play() #play now so it can load up later
	
	filename = mp3filepath.split('/')[-1]

	#neat feature of python, 'or' in the middle of variable assignment
	# so if mp3tags.tag.title is None, it will use something else	
	gs['song'] = mp3tags.title or filename
	gs['artist'] = mp3tags.artist or ''
	
	# disable controllers, set back to playing state
	gs['player'] = None
	gs['controller'] = None
	gs['state'] = 'playing'
	
	display_hidden_song()

	# wait for button press
	gs['all_controllers'] = 'on'

def show_scores():
	gs['app'].hideSubWindow('game')
	gs['app'].setLabel('p1','Player 1: {}'.format(gs['scores']['1']))
	gs['app'].setLabel('p2','Player 2: {}'.format(gs['scores']['2']))
	gs['app'].setLabel('p3','Player 3: {}'.format(gs['scores']['3']))
	gs['app'].setLabel('p4','Player 4: {}'.format(gs['scores']['4']))
	gs['app'].showSubWindow('scores')


def turnoff_lights():
	for p in players:
		p[0].on() # turning on the gpio deactivates the 

def button_bootstrap(key): #bootstrap just so we can dev/test with keyboard 
	gs['player'] = key
	gs['controller'] = [LED(0),Button(1)] # dummies

def button_callback(gpiobutton):
	if gs['all_controllers'] == 'on': #only process if all_controllers is on
		gs['all_controllers'] = 'off' #we caught one button, so disable so that others can't hijack it
		p = find_player(gpiobutton.pin)
		p[0].off() #turn on their LED
		gs['player'] = players.index(p) + 1
		gs['controller'] = p

