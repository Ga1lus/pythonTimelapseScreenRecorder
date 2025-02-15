import os
import multiprocessing
import signal
import time
import ffmpeg

from extras import *

delay = multiprocessing.Value('f', 0)
frameRate = 24
screenshotsPath = '/home/things/screenshotTimelapse'

pid = []
status = {'active': f'{red}not started', 'delay':f'{bright_yellow}0', 'empty':f'{green}empty'}

if len(os.listdir('/home/things/screenshotTimelapse/screenshots/')) > 0:
	status['empty'] = f'{red}not empty'

#_________________________________________________________________________________
def screenshotProcess():
	i = 0
	while True:
		#cprint(yellow, i)
		os.system(f'scrot -z /home/things/screenshotTimelapse/screenshots/frame_{i}.png')
		i += 1
		time.sleep(delay.value)

#_________________________________________________________________________________
def imageFolder():
	os.system('thunar /home/things/screenshotTimelapse/screenshots/')
	
def videoFolder():
		os.system('thunar /home/things/screenshotTimelapse/videos/')

def timelapseDelay():
	while True:
		try:
			x = float(input('input timelapse delay: '))
			break
		except:
			cprint(red, 'invalid input')
	
	delay.value = x
	status['delay'] = f'{bright_yellow}{x}'

def startTimelapse():
	global pid
	
	if len(os.listdir('/home/things/screenshotTimelapse/screenshots/')) > 0:
		cprint(red, "screenshots folder not empty!")
		setVideoMenu()
		time.sleep(0.75)
	
	else:
		process = multiprocessing.Process(target=screenshotProcess)
		process.daemon = True
		process.start()
		pid = process.pid
		status['active'] = f'{green}active'
		status['empty'] = f'{red}not empty'
	
def pauseTimelapse():
	if type(pid) == list:
		cprint(red, 'process not started')
		time.sleep(0.75)
		return	
	
	os.kill(pid, signal.SIGSTOP)
	status['active'] = f'{orange}paused'

def continueTimelapse():
	if type(pid) == list:
		cprint(red, 'process not started')
		time.sleep(0.75)
		return
	
	os.kill(pid, signal.SIGCONT)
	status['active'] = f'{green}active'

def stopTimelapse():
	global pid
	
	if type(pid) == list:
		cprint(red, 'process not started')
		time.sleep(0.75)
		return
	
	choice = promptTUI(yesNo)
	if choice[0]:
		os.kill(pid, signal.SIGKILL)
		time.sleep(0.25)
		
	status['active'] = f'{red}stoped'
	pid = []
	
def createVideo():
	if type(pid) != list:
		cprint(red, 'recording still active')
		setTimelapseMenu()
		time.sleep(0.75)
		return
	
	if len(os.listdir('/home/things/screenshotTimelapse/screenshots/')) > 0:
		pass
	
	else:
		cprint(red, 'image folder is empty')
		setTimelapseMenu()
		time.sleep(0.75)
		return
	
	name = input("input video name: ")
	inputStream = ffmpeg.input(f'{screenshotsPath}/screenshots/frame_%d.png', framerate=frameRate)
	outputStream = ffmpeg.output(inputStream, f'{screenshotsPath}/videos/{name}.mp4')
	ffmpeg.run(outputStream)
	
	cprint(green, 'video created, enter to continue: ')
	input()
	

def clearFrames():
	choice = promptTUI(yesNo)
	if choice[0]:
		os.system('rm -rf /home/things/screenshotTimelapse/screenshots')
		os.system('mkdir /home/things/screenshotTimelapse/screenshots')
	
	time.sleep(0.25)
	status['empty'] = f'{green}empty'

#_________________________________________________________________________________
def setMainManu():
	global activeMenu
	activeMenu = mainMenu

def setTimelapseMenu():
	global activeMenu
	activeMenu = timelapseMenu
	
def setVideoMenu():
	global activeMenu
	activeMenu = videoMenu
	
def stopLoop():
	if type(pid) != list:
		cprint(red, 'recording still active')
		setTimelapseMenu()
		time.sleep(0.75)
		return
	
	choice = promptTUI(yesNo)
	if choice[0]:
		time.sleep(0.25)
		exit()

activeMenu = []

mainMenu = [{'|timelapse options|': setTimelapseMenu}, {'|image/video options|': setVideoMenu}, {'|exit|':stopLoop}]

timelapseMenu = [{'|set delay|': timelapseDelay},{'|start|': startTimelapse},{'|pause|': pauseTimelapse}, {'|continue|': continueTimelapse}, {'|stop|': stopTimelapse}, {'|go to menu|': setMainManu}]

videoMenu = [{'|open images|': imageFolder}, {'|open videos|': videoFolder}, {'|create video|': createVideo}, {'|clear frames|': clearFrames}, {'|go to menu|': setMainManu}]

yesNo = [{'|yes|':True}, {'|no|':False}]

#_________________________________________________________________________________
activeMenu = mainMenu

while True:
	#promptTUI([{'delay': timelapseDelay}],[{'start': startTimelapse},{'pause': pauseTimelapse},{'continue': continueTimelapse},{'stop': stopTimelapse}],[{'video': createVideo},{'delete': clearFrames}])[0]()
	print(f"recording: {status['active']} {reset}| delay: {status['delay']} {reset}| image folder: {status['empty']}{reset}")
	promptTUI(*activeMenu, cursorPosition=[0,0])[0]()
	time.sleep(0.25)
	os.system('clear')
	
	
	
	
