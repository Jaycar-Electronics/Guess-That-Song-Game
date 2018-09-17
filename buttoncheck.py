#!/usr/bin/python3

from config import players,find_player
from time import sleep


def pbutton(arg):
	print('button press',arg.pin)
	p = find_player(arg.pin)
	print('player:',p)
	print('flashing for 5 seconds')
	for x in range(25):
		p[0].toggle()
		sleep(0.2)
	print('==='*10)
		

for x in players:
	x[1].when_pressed = pbutton


t = True
while True:
	t = not t
	for x in players:
		x[0].toggle()
	print('tick'if t else 'tock')
	sleep(1)
