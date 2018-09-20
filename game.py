from appJar import gui
from functions import *
def attach_windows(app):
	# ========================================================
	app.startSubWindow("game")
	# ========================================================
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
	app.addEmptyLabel('player_spotlight')


	# configuration
	app.getLabelWidget('guess').config(font=('times','20','italic'))
	app.getLabelWidget('song_name').config(font=('times','34'))
	app.getLabelWidget('song_artist').config(font=('times','26','italic'))
	app.getLabelWidget('player_spotlight').config(font=('times','12'))

	# test

	app.setLabel('guess','Created by')
	app.setLabel('song_name','Jaycar Electronics')
	app.setLabel('player_spotlight','Author D.K.West')


	
	app.registerEvent(process_game)
	app.bindKey('<space>',key_press)
	app.bindKey('<Return>',key_press)
	app.bindKey('<Escape>',show_scores)
	app.stopSubWindow()
	# ========================================================
	# ========================================================


	# ========================================================
	app.startSubWindow('scores')
	# ========================================================
	#score window
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
	# ========================================================
	# ========================================================

