from appJar import gui
from config import find_player, players
from functions import *
from pygame import mixer
import time
import eyed3

mixer.init()
g_state = {
'countdown': 5,
'state': 'stopped', # game switch sets what state the game is in 
'controllers': 'off',
'c': None,
'scores':{
	'1':0,
	'2':0,
	'3':0,
	'4':0,
},
'about':'Created by Jaycar Electronics',
'song': '',
'artist': '',
}


def attachwindow(app):
	app.startSubWindow("game",)
	# some defines
	app.setBg('black',override=True)
	app.setSticky('nw')
	app.setFg('white')
	app.setSize('fullscreen')
	# widgets:
	app.addLabel('debug','Press Esc to close')

	app.addEmptyLabel('guess')
	app.addEmptyLabel('song_name')
	app.addEmptyLabel('song_artist')
	app.addEmptyLabel('player_stage')


	# configuration
	app.getLabelWidget('guess').config(font=('times','20','italic'))
	app.getLabelWidget('song_name').config(font=('times','34'))
	app.getLabelWidget('song_artist').config(font=('times','26','italic'))
	app.getLabelWidget('player_stage').config(font=('times','12'))

	# test

	app.setLabel('guess','test')
	app.setLabel('song_name','test')
	app.setLabel('player_stage','test')


	
	app.registerEvent(count_down)
	app.bindKey('<space>',key_press)
	app.bindKey('<Return>',key_press)
	app.bindKey('<Escape>',show_scores)
	app.stopSubWindow()

	#score window

	app.startSubWindow('scores')
	app.setSize('fullscreen')
	app.setSticky('ew')
	app.addLabels(['p1','p2'])
	app.addLabels(['p3','p4'])
	app.addLabel('created by Jaycar Electronics')
	app.addTextArea('history')
	app.getLabelWidget('p1').config(font=('times','28','italic'))
	app.getLabelWidget('p2').config(font=('times','28','italic'))
	app.getLabelWidget('p3').config(font=('times','28','italic'))
	app.getLabelWidget('p4').config(font=('times','28','italic'))
	app.stopSubWindow()

def turnoff_lights():
	for p in players:
		p[0].on()

def button_callback(gpiobutton):
	global g_state
	if g_state['controllers'] == 'on':
		g_state['controllers'] = 'off' #caught one button, so disable so that others can't hijack it
		p = find_player(gpiobutton.pin)
		p[0].off() #turn on their LED
		g_state['c'] = players.index(p) + 1
		g_state['player'] = p

