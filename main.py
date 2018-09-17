#!/usr/bin/python3
from appJar import gui
import os
#local scripts
import config
from game import *


app = gui()

#enable buttons first
for controller in config.players:
	controller[1].when_pressed = button_callback
	controller[0].on() #turn LED off


def go(b):
	global g_state
	g_state['state'] = 'countdown' # starts the timer
	g_state['countdown'] = 5
	dir = app.getEntry('files')
	print(dir)
	g_state['songlist'] = [os.path.join(dir, file) for file in os.listdir(dir) if file.lower().endswith('.mp3')]

	app.showSubWindow('game')


app.addLabel('title','MP3 Guess That song Game')
app.addLabel('Folder for MP3:')
app.addDirectoryEntry('files')

attachwindow(app)

app.addButton('Go',go)


app.go()
