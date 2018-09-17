

def count_down():
	''' ticktock function
		used for handling the game state every second
		and setting the correct data on the gui
	'''
	global g_state
	global app

	# countdown state
	# starting up the game with a simple countdown timer
	if g_state['state'] == 'countdown':
		if g_state['countdown'] > 0:
			app.setLabel('song_name','  ...'+str(g_state['countdown']))
			app.setLabel('player_stage','')
			app.setLabel('guess','Get Ready')
			g_state['countdown'] -= 1
			time.sleep(1) #shouldn't do this but it'll do for the quick and dirty
		else:
			# timer reached 0, load new song
			load_new_song()

	# waiting state
	# waiting for a player to hit the buzzer and tell us what the song is 
	elif g_state['state'] == 'waiting':
		# waiting for button press here
		if g_state['c'] is not None: #button press
			app.setLabel('player_stage','Player '+str(g_state['c']))
			mixer.music.pause()
			g_state['state'] = 'stage'


	# stage state
	# a player has the stage, all eyes on the player to make the right song
	elif g_state['state'] == 'stage' :
		if g_state['player'][1].is_pressed:
			#pass back to open
			while(g_state['player'][1].is_pressed):
				time.sleep(0.2) #just block until it is released
			mixer.music.unpause()
			g_state['state'] = 'waiting'
			app.setLabel('player_stage','Player {} passed back, waiting for next player'.format(g_state['c']))
			g_state['c'] = None
			g_state['controllers'] = 'on'
			turnoff_lights()

	# reveal state
	# show the 
	elif g_state['state'] == 'reveal':
		pass


def key_press(key):
	global g_state
	if g_state['state'] == 'stage':
		app.setLabel('song_name',g_state['song']) #show the song
		app.setLabel('song_artist',g_state['artist'])

		app.setLabel('player_stage','Did Player {} get it correct? Enter Key for yes, Space for No'
			.format(g_state['c']))
		g_state['state'] = 'showdown'

	elif g_state['state'] == 'showdown':
		if key == '<Return>':
			#they got the song right, stop and load new song
			app.setLabel('song_name','CORRECT! Player {} gains 1 point'.format(g_state['c']))
			app.setLabel('guess','yey!')
			app.setLabel('player_stage', 'Good work smarty pants')
			g_state['scores'][str(g_state['c'])] += 1
			app.setTextArea('history','{} {} CORRECT\n'.format(g_state['song'] , 'P'+str(g_state['c'])),end=False)
		elif key == '<space>':
			#they got the song wrong,no point continuing song because we've already shown it.
			app.setLabel('song_name','INCORRECT! Player {} loses 1 point'.format(g_state['c']))
			app.setLabel('guess','uh oh')
			app.setLabel('player_stage', 'better luck next time')
			g_state['scores'][str(g_state['c'])] -= 1
			app.setTextArea('history','{} {} WRONG\n'.format(g_state['song'] , 'P'+str(g_state['c'])),end=False)
		else:
			#shouldn't get here, something triggered the keypress. 
			#this will probably, hopefully, never get called, so we can just quit out of the function
			return	
		app.setLabel('song_artist','')
		g_state['state'] = 'prepare'

	elif g_state['state'] == 'prepare':
		#load next song
		load_new_song()

			
def show_song():
	global g_state
	if g_state['state'] == 'stage':
		#show the song
		#we've shown the song, so start again
		app.enableEnter(load_new_song)
		app.bindKey('<Space>',stage_again)


def load_new_song():
	global g_state
	if len(g_state['songlist']) == 0:
		#out of songs, time to quit
		show_scores()
		return
	#load the song, start playing
	mp3file = g_state['songlist'].pop()
	print(mp3file)
	mixer.music.load(mp3file)
	mixer.music.play()			
	filename = mp3file.split('/')[-1]
	print(filename)
	mp3f = eyed3.load(mp3file)
	name_tag = mp3f.tag.title
	artist_tag = mp3f.tag.artist
	g_state['song'] = name_tag or filename
	g_state['artist'] = artist_tag or ''



	g_state['state'] = 'waiting'
	g_state['c'] = None
	app.setLabel('song_name','')
	app.setLabel('guess',"What's this song?")
	app.setLabel('player_stage','Waiting for button press')

	# wait for button press
	g_state['controllers'] = 'on'

def show_scores():
	app.hideSubWindow('game')
	app.setLabel('p1','Player 1: {}'.format(g_state['scores']['1']))
	app.setLabel('p2','Player 2: {}'.format(g_state['scores']['2']))
	app.setLabel('p3','Player 3: {}'.format(g_state['scores']['3']))
	app.setLabel('p4','Player 4: {}'.format(g_state['scores']['4']))
	#app.setMessage('history',g_state['history'])
	app.showSubWindow('scores')


