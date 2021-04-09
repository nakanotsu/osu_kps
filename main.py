#pohmx development 2021
import keyboard
import time
import math
# import wx
# from twisted.internet import wxreactor
# install before importing reactor.
# wxreactor.install() 
from twisted.internet import task, reactor
import sys
import warnings
# ignore dumb warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

ID_EXIT = 101
win_size = 300, 200

last = [0,0]
elapsed = 0
no_events_e = 0
elapsed_chain = []
bound = 1
clock2_bound = 0.7
rate = 0.005
k = 0
max_kps = 0

kps_label_updater = ''
kps_max_label_updater = ''

''' TIMER '''
timerRunning = False
timer2Running = False
timerStarted = False

def updateText():
	global kps_label_updater
	global kps_max_label_updater
	window.KPS_DISPLAY.SetLabel('<KPS>: ' + kps_label_updater)
	window.KPS_MAX_DISPLAY.SetLabel('<MAX_KPS>: ' + kps_max_label_updater)
	f = open("kps.txt", "w")
	f2 = open("max_kps.txt", "w")
	f.write(kps_label_updater)
	f2.write(kps_max_label_updater)
	f.close()
	f2.close()


def no_events():
	global kps_max_label_updater
	global max_kps
	global no_events_e	
	global timer2Running
	if no_events_e > clock2_bound:
		max_kps = 0
		kps_max_label_updater = str(max_kps)
		updateText()
		timer2Running = False
		no_events_e = 0
		clock2.stop()
	no_events_e = elapsed_t()
		
def timer():
	global k
	global timerStarted
	global timerRunning
	global timer2Running
	global rate
	global max_kps
	global kps_label_updater
	global kps_max_label_updater

	if timerStarted is False:		
		timerStarted = True

	_e = elapsed_t()	

	kps_ = kps(k,1)
	kps_label_updater = str(kps_)
	updateText()

	if kps_ > max_kps:
		max_kps = kps_
		kps_max_label_updater = str(max_kps)
		updateText()

	if _e >= bound+rate*10:	
		if timer2Running is False:
			timer2Running = True
			clock2.start(clock2_bound)
		reset()
		clock.stop()

def clockSchedule(c):
	global timerRunning
	global k
	global elapsed_chain
	global no_events_e
	no_events_e = 0
	elapsed_chain.append(elapsed_t())
	k += 1
	if timerRunning is False:
		timerRunning = True		
		clock.start(rate)	

def elapsed_t():
	global last
	global elapsed
	if last[0] == 0: last[0] = time.time_ns()
	if last[0] != 0: last[1] = time.time_ns()
	if last[1] > last[0]: 
		elapsed = (last[1]-last[0])/1000000000
	return elapsed

def reset():
	global timerStarted
	global timerRunning
	global last
	global k
	global kps_label_updater
	timerStarted = False
	timerRunning = False	
	last[0] = 0
	k = 0
	kps_label_updater = str(0)
	updateText()
	elapsed_t()

def kps(key, t):
	if key != 0:
		return round(key/t)
	else:
		return 0

'''TAIKO'''
keyboard.on_press_key(20,clockSchedule) #T
keyboard.on_press_key(21,clockSchedule) #Y
keyboard.on_press_key(24,clockSchedule) #O
keyboard.on_press_key(25,clockSchedule) #P

'''CTB'''
keyboard.on_press_key(30,clockSchedule) #A
keyboard.on_press_key(75,clockSchedule) #4
keyboard.on_press_key(77,clockSchedule) #5

'''MANIA'''
keyboard.on_press_key(31,clockSchedule) #S
keyboard.on_press_key(32,clockSchedule) #D
keyboard.on_press_key(33,clockSchedule) #F
keyboard.on_press_key(57,clockSchedule) #SPACE
keyboard.on_press_key(36,clockSchedule) #J
keyboard.on_press_key(37,clockSchedule) #K
keyboard.on_press_key(38,clockSchedule) #L

'''OSU'''
keyboard.on_press_key(51,clockSchedule) #K
keyboard.on_press_key(52,clockSchedule) #L

'''CLOCK'''
clock = task.LoopingCall(timer)
clock2 = task.LoopingCall(no_events)

'''GUI
class construct_Frame(wx.Frame):
	def __init__(self, parent, ID, title, size):
		# <Frame constructor>
		wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition, wx.Size(size))
		menu = wx.Menu()
		menu.Append(ID_EXIT, "E&xit", "Terminate the program")
		menuBar = wx.MenuBar()
		menuBar.Append(menu, "&File")
		self.SetMenuBar(menuBar)
		wx.EVT_MENU(self, ID_EXIT, self.DoExit)
		# make sure reactor.stop() is used to stop event loop:
		wx.EVT_CLOSE(self, lambda evt: reactor.stop())

	def DoExit(self, event):
		reactor.stop()

class construct_App(wx.App):
	def OnInit(self):
		# <Construct a Frame, show & position it>
		Frame = construct_Frame(None, -1, "GUI", win_size)
		Frame.Show(True)
		self.SetTopWindow(Frame)
		# CREATING A LABEL, MUST HAVE A PARENT, ID, TEXT, POSITION *TUPLE, SIZE *TUPLE, STYLE(0 IS DEFAULT), NAME?
		self.KPS_DISPLAY = wx.StaticText(Frame, 0, "<KPS>: 0", (0,0), (win_size[0],win_size[1]/3), 0, 'KPS_LABEL')
		self.KPS_MAX_DISPLAY = wx.StaticText(Frame, 1, "<MAX_KPS>: 0", (0,win_size[1]/3), (win_size[0],win_size[1]/3), 0, 'Xd')
		# <Must return True>
		return True

# register the App instance with Twisted:
window = construct_App(0)
reactor.registerWxApp(window)
'''

# start the event loop:
reactor.run()