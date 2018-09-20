#!/usr/bin/python3
from appJar import gui
import os



app = gui('MP3 Guess That Song Game')

#local scripts
import config
from game import attach_windows
from functions import button_callback,gs


gs['app'] = app



#enable buttons first
for controller in config.players:
	controller[0].on() #turn LED off
	controller[1].when_pressed = button_callback


def go(b):
	global gs
	dir = app.getEntry('files') # get the file directory

	songlist = [os.path.join(dir, file) for file in os.listdir(dir) if file.lower().endswith('.mp3')]	

	if len(songlist) == 0:
		app.errorBox('no files',
'''There is no mp3 files in this folder, please check the correct directory again, 
or if you are certain, submit an issue on github
directory is '{}' '''.format(dir))
		return	#cancel the "go" function

	gs['songlist'] =  songlist
	gs['state'] = 'countdown' # starts the timer
	gs['countdown'] = 5
		
	#set scores to 0 initially
	gs['scores'] = {'1':0,'2':0,'3':0,'4':0}
	app.showSubWindow('game')


app.addLabel('Folder for MP3:')
app.addDirectoryEntry('files')
app.addButton('Go',go)
app.setButtonBg('Go','green')
app.setButtonFg('Go','white')
app.setButtonWidth('Go',40)
app.setButtonHeight('Go',7)
app.setButtonPadding('Go',[40,14])
attach_windows(app)

app.go()
