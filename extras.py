import json

import os
import sys

import time
import inspect
import random

import tty
#import terminos

escapeSequences = ['\n', '\r']

def showColours():
	for i in range(256):
		print(f"\033[38;5;{i}m{str(i).rjust(3)}", end=" ")
		if (i + 1) % 16 == 0:
			print("\033[0m")  # Reset after every line

class randomColour:
	def __repr__(self):
		#return "\033[38;5;204m"
		return f"\033[38;5;{random.randint(0, 255)}m"
		
class bg_randomColour:
	def __repr__(self):
		#return "\033[38;5;204m"
		return f"\033[48;5;{random.randint(0, 255)}m"

# Text Colors
black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"

# Bright Text Colors
bright_black = "\033[90m"
bright_red = "\033[91m"
bright_green = "\033[92m"
bright_yellow = "\033[93m"
bright_blue = "\033[94m"
bright_magenta = "\033[95m"
bright_cyan = "\033[96m"
bright_white = "\033[97m"

# Background Colors
bg_black = "\033[40m"
bg_red = "\033[41m"
bg_green = "\033[42m"
bg_yellow = "\033[43m"
bg_blue = "\033[44m"
bg_magenta = "\033[45m"
bg_cyan = "\033[46m"
bg_white = "\033[47m"

# Bright Background Colors
bg_bright_black = "\033[100m"
bg_bright_red = "\033[101m"
bg_bright_green = "\033[102m"
bg_bright_yellow = "\033[103m"
bg_bright_blue = "\033[104m"
bg_bright_magenta = "\033[105m"
bg_bright_cyan = "\033[106m"
bg_bright_white = "\033[107m"

# Text Styles
reset = "\033[0m"
bold = "\033[1m"
dim = "\033[2m"
italic = "\033[3m"
underline = "\033[4m"
blink = "\033[5m"
reverse = "\033[7m"
hidden = "\033[8m"
strikethrough = "\033[9m"

#extra colours
pink = "\033[38;5;204m"
orange = "\033[38;5;214m"

rainbow = randomColour()
bg_rainbow = bg_randomColour()

rgbColour = '\033[38;2;0;0;255m'
def rgb(R, G, B):
	global rgbColour
	rgbColour = f'\033[38;2;{clamp(0, 255, R)};{clamp(0, 255, G)};{clamp(0, 255, B)}m'
	return rgbColour
	
bg_rgbColour = ''
def bg_rgb(R, G, B):
	global bg_rgbColour
	bg_rgbColour = f'\033[48;2;{clamp(0, 255, R)};{clamp(0, 255, G)};{clamp(0, 255, B)}m'
	return bg_rgbColour

colourNames = [
    # Text Colors
    black, red, green, yellow, blue, magenta, cyan, white,

    # Bright Text Colors
    bright_black, bright_red, bright_green, bright_yellow, 
    bright_blue, bright_magenta, bright_cyan, bright_white,

    # Background Colors
    bg_black, bg_red, bg_green, bg_yellow, bg_blue, 
    bg_magenta, bg_cyan, bg_white,

    # Bright Background Colors
    bg_bright_black, bg_bright_red, bg_bright_green, 
    bg_bright_yellow, bg_bright_blue, bg_bright_magenta, 
    bg_bright_cyan, bg_bright_white,

    # Text Styles
    reset, bold, dim, italic, underline, blink, 
    reverse, hidden, strikethrough,
    
    #extra colours
    pink, orange, rainbow, rgbColour, bg_rgbColour
]

######################################################################################################################################################################


def clampOverflow():
	pass


def clamp(x1, x2, xin):
	if xin < x1:
		return x1
		
	elif xin > x2:
		return x2 
	
	else:
		return xin


# Use this like print() when changing colour just pass the colour as an item before what should be printed
# for example call cprint(colour, 'string', colour, int), it uses ansi codes to set text colours, background colours and styles
def cprint(*args, **kwargs): #this function will print in colour
	
	colour = bright_white
	
	for item in args:
		
		if '\033' in str(item):
		#if item in colourNames:
			colour = item
			print(f'{colour}', end='')
		
		else:
			print(f"{colour}{item}", end=' ')
	
	print(reset, **kwargs)

#cprint(red, 'this is red\n', blue, 'this is blue\n', black, 'this is black\n', reset, 'the\n', 'rest\n', 'is\n', 'reset\n')


# To use this function just call printList(optional list title, pass a list, optionally pass a time duration to pause between each item print):
def listPrint(*args, sleep=0): 	#this function will print every item of every child in a nested list and indicate its structure #resource inneficient but cool
	frame = inspect.currentframe().f_back
	itemsList = []
	
	if type(args[0]) != list:
		cprint(bright_magenta, args[0])
		if len(args) > 1:
			itemsList = args[1]
		else:
			itemsList = args[0]
			
		if type(itemsList) != list:
			cprint(bright_red, bold, "error", reset, bg_yellow,f"line {frame.f_lineno}", reset, 'not a', green, 'type list')
			return
	else:
		itemsList = args[0]
		
		if type(itemsList) != list:
			cprint(bright_red, bold, "error", reset, bg_yellow,f"line {frame.f_lineno}", reset, 'not a', green, 'type list')
			return
		
	
	through = [0] 						#this is to know what level you are at and keeps track of the itteration, len(through) indicates how many levels there are
	listReturn = itemsList 				#listRetun becomes the child list
	
	t = 0							#this keeps track of what level i am at
	
	while True: #keeps the loop running, the loop should only check one item at t time, next itteration will check the next item
		
		if type(listReturn) == list: #if the current listReturn is an list
			
			if through[-1] < len(listReturn): #if nth level is smaller than the length of lan(listReturn)
				
				if type(listReturn[through[-1]]) == list: 	#if the nth child of listRetun is an list
					
					listReturn = listReturn[through[-1]] 		#update listReturn to nth child
					t += 1										#update level track count
					through.append(0) 							#append another level
					cprint(magenta, f"{f''.join('|' + str(through[i]) + '  ' for i in range(len(through) - 1))}└──") 	#this will indicating moving up a level
					
				else: 										#if nth child is not a list then print nth child
					
					cprint(f"\033[35m{f''.join('|' + str(through[i]) + '  ' for i in range(len(through)))}\033[0m{listReturn[through[-1]]}") 	#print nth child
					through[-1] += 1 							#this will increment the current level of through
					
			else:									#if the nth lever is bigger than len(listReturn)
				
				listReturn = itemsList 					#sets list return back to the original list input
				t -= 1 									#decrement level track
				del through[-1] 						#go back one to the prev level
				
				if len(through) < 1: 				#if the list is complete it will go through all items in in through and delete them
					break 								#then if there is no more items in through it will break the whileLoop
				
				through[-1] += 1 						#increment nth level
				cprint(magenta, '.') 					#this will print a . indicating it finished the previous list and will go to its sibling list
				
				for i in through: 					#this for loop will run through each item in through to get the appropriate listReturn
					
					if i < len(listReturn): 			#this will check if the current level is less than len(listReturn)
					
						if type(listReturn[i]) == list: 	#checks weather the nth item of the current level is a list
						
							listReturn = listReturn[i] 			#if it is a list update listReturn to the nth item
						
							if through.index(i) >= t: 				#this is meant to check weather the current level has been appended before
							
								through.append(0) 						#if if not append a new level
								t += 1 									#then update the tracking variable
								cprint(magenta, f"{f''.join('|' + str(through[i]) + '  ' for i in range(len(through) - 1))}└──") 	#moving up a level
		
		if sleep > 0: 					#just for visual Aesthetics, checks if when the function was called it was asked to add a delay between each step
			time.sleep(sleep) 				#the amount of delay specified

######################################################################################################################################################################

fd = sys.stdin.fileno()
def modeTUI():
	tty.setraw(fd)


def promptTUI(*args, normalColour = reset, cursorColour = bg_blue, chosenColour = bg_bright_black, cursorPosition = [0, 0]):
	nrmC = normalColour
	curC = cursorColour
	choC = chosenColour
	
	chosen = False
	
	choice = None
	cursorPos = cursorPosition
	
	unknown = False

	maxi = 1
	maxlen = 0
	for i in range(len(args)):
		if type(args[i]) == list:
			maxi = max(maxi, len(args[i]))
			for item in args[i]:
				if type(item) == dict:
					maxlen = max(maxlen, len(str(list(item.keys())[0])))
				
				else:
					maxlen = max(maxlen, len(str(item)))
		
		elif type(args[i]) == dict:
			maxlen = max(maxlen, len(str(list(args[i].keys())[0])))
		
		else:
			maxlen = max(maxlen, len(str(args[i])))

	while True:	
		if unknown:
			print(f'\033[{maxi}A')
					
		ii = 0
		while True:
			if ii < maxi:
				for i in range(len(args) + 1):
					if i > len(args) - 1:
						if ii < maxi - 1:
							print()
							print('\r', end="")
					
					elif type(args[i]) == list:
						if ii < len(args[i]):
							hlc = nrmC
							
							spaces = ''
							key = args[i][ii]
							choiceKey = key
							if type(args[i][ii]) == dict:
								key = list(args[i][ii].keys())[0]
								choiceKey = args[i][ii][key]
								spaces = ' ' * ( maxlen - len(str(list(args[i][ii].keys())[0])) )
								
							else:
								spaces = ' ' * ( maxlen - len(str(args[i][ii])) )
							
							if cursorPos[0] == i and cursorPos[1] == ii:
								hlc = curC
								choice = choiceKey
							
							#spaces = ' ' * ( maxlen - len(str(args[i][ii])) )
							cprint(hlc, str(key) + spaces, end=' ')
							
						else:
							spaces = ' ' * maxlen
							cprint(spaces, end=' ')
					
					else:
						if ii == 0:
							hlc = nrmC
							
							key = args[i]
							choiceKey = key
							if type(args[i]) == dict:
								key = list(args[i].keys())[0]
								choiceKey = args[i][key]
							
							if cursorPos[0] == i:
								hlc = curC
								choice = choiceKey
							
							spaces = ' ' * ( maxlen - len(str(args[i])) )
							cprint(hlc, str(key) + spaces, end=' ')
							
						else:
							cprint(' ' * maxlen, end=' ')
				
				ii += 1
				
			else:
				print('\r', end="")
				break
			
			print('\r', end="")
				
		if chosen:
			print('\033[E')
			os.system("stty sane")
			return [choice, cursorPos]
		
		print('\033[?25l', end='')
		modeTUI()
		ch = sys.stdin.read(1)
		
		if ch == '\x11':
			print('\033[E')
			os.system("stty sane")
			exit()
		
		elif ch == '\r':
			curC = choC
			chosen = True
			
		elif ch == '\x1b':
			ch = sys.stdin.read(2)
			if ch == '[A':
				#cprint(yellow, 'up')
				#cursorPos[1] -= 1
				if cursorPos[0] <= len(args) - 1:
					if type(args[cursorPos[0]]) == list:
						cursorPos[1] = clamp(0, len(args[cursorPos[0]]) - 1, cursorPos[1] - 1)
			
			if ch == '[B':
				#cprint(yellow, 'down')
				#cursorPos[1] += 1
				if cursorPos[0] <= len(args) - 1:
					if type(args[cursorPos[0]]) == list:
						cursorPos[1] = clamp(0, len(args[cursorPos[0]]) - 1, cursorPos[1] + 1)
			
			if ch == '[C':
				#cursorPos[0] += 1
				cursorPos[0] = clamp(0, len(args) - 1, cursorPos[0] + 1)
				if type(args[cursorPos[0]]) == list:
					cursorPos[1] = clamp(0, len(args[cursorPos[0]]) - 1, cursorPos[1])
			
			if ch == '[D':
				#cursorPos[0] -= 1
				cursorPos[0] = clamp(0, len(args) - 1, cursorPos[0] - 1)
				if type(args[cursorPos[0]]) == list:
					cursorPos[1] = clamp(0, len(args[cursorPos[0]]) - 1, cursorPos[1])
				
		print('\r', end="")
		unknown = True
	
	os.system("stty sane")


def splitScreenPrint(*args): #work in progress
	tWidth, tLength = os.get_terminal_size()
	splits = len(args)
	splitSize = int((tWidth - splits) / splits)
	
	screen = []
	maxLines = 0
	
	for i in range(splits):
		screen.append([])
		
		if type(args[i]) == list:
			addColour = False
			colour = reset
			minus = len(colour)
			totalMinus = len(colour)
			for item in args[i]:
				if '\033' not in str(item) and str(item) not in escapeSequences:
					if len(screen[i]) != 0:
						if len(screen[i][-1]) + totalMinus - len(colour) != 0:
							screen[i][-1] += ' '
					
					else:
						pass
				
				if item in escapeSequences:
					if item == '\n':
						screen[i][-1] += reset + ' ' * (splitSize - len(screen[i][-1]) + totalMinus)
						screen[i].append(colour)
						totalMinus = len(colour)
				
				elif '\033' in str(item):
					colour = item
					#minus = len(colour)
					addColour = True
					
				else:
					if len(screen[i]) == 0:
						screen[i].append(colour)
						minus = len(colour)
						totalMinus = len(colour)
						addColour = False
					
					newStr = str(item)
					while True:
						if len(screen[i][-1] + newStr) - totalMinus >= splitSize:
							leftover = len(screen[i][-1] + newStr) - totalMinus - splitSize
							
							if addColour:
								screen[i][-1] += colour + newStr[:len(newStr) - leftover]
								minus = len(colour)
								totalMinus = len(colour)
								addColour = False
								
							else:
								screen[i][-1] += newStr[:len(newStr) - leftover]
								totalMinus = len(colour)
							
							newStr = newStr[len(newStr) - leftover:]
							screen[i].append(colour)
						
						else:
							if addColour:
								screen[i][-1] += colour + newStr
								totalMinus += len(colour)
								addColour = False
								break
								
							else:
								screen[i][-1] += newStr
								break
							
			screen[i][-1] += reset + ' ' * (splitSize - len(screen[i][-1]) + totalMinus)
			
		else:
			ii = 0
			newStr = str(args[i])
			while True:
				if len(newStr) > splitSize:
					screen[i].append(newStr[:splitSize])
					newStr = newStr[splitSize:]
					
				else:
					screen[i].append(newStr)
					break
					
		maxLines = max(maxLines, len(screen[i]))
				
	for ii in range(maxLines):
		line = []
		for i in range(splits):
			if i != 0:
				prevLen = len(str(line[-1]))
			
				line.append(' ' * (splitSize - prevLen) + f'{magenta}|{reset}')
			
			if ii < len(screen[i]):
				line.append(screen[i][ii])
				
			else:
				line.append('')
	
		for item in line:
			print('\033[K', end='')
			print(reset+item, end='')
		
		print()
	
	return maxLines





