from gpiozero import LED, Button
from time import sleep

button_pins = [21,9,10,11] #set these to the button pins that you have, in order. 
led_pins = [26,19,13,6] #set these to the led pins you have in order

'''
the idea would be, if the led and buttons are in the form of [a,b,c,d][e,f,g,h]
the zip function will bring it to:
[(LED(a),Button(e)) , (b,f), ... ]


'''

players = list(zip([LED(x) for x in led_pins],
            [Button(x) for x in button_pins]))



## some helper functions:

def find_player(button_pin):
	for x in players:
		if x[1].pin == button_pin:
			return x #returns the player object in the list.

