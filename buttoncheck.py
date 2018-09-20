#!/usr/bin/python3

from config import players,find_player
from time import sleep

'''
	button testing code file
	===========
	this code will assign each button to the pbutton function
	for button presses
	as well as flash the LED's on and off
	to make sure that the LEDs work.


	use this while building to make sure your wiring is correct
'''

def pbutton(arg):

	print('button press',arg.pin)
	p = find_player(arg.pin)
	print('player:',p)
	print('flashing for 5 seconds')
	for x in range(25):
		p[0].toggle()
		sleep(0.2)
	print('==='*10)
		




if __name__ == '__main__':
	for i,x in enumerate(players):
		x[1].when_pressed = pbutton

		if i%2:	x[0].toggle()


	t = True
	while True:
		t = not t
		for x in players:
			x[0].toggle()
		print('tick'if t else 'tock')
		sleep(1)
