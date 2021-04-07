#pohmx development 2021
import keyboard
import time
import math
import wx
from twisted.internet import wxreactor
# install before importing reactor.
wxreactor.install() 
from twisted.internet import task, reactor
import sys
import warnings
# ignore dumb warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

ID_EXIT = 101
win_size = 300, 200

last = [0,0]
elapsed = 0
bound = 1
rate = 0.005
k = 0
max_kps = 0

kps_label_updater = ''
kps_max_label_updater = ''

''' TIMER '''
timerRunning = False
timerStarted = False

def timer():
	global k
	global timerStarted
	global timerRunning
	global rate
	global max_kps
	global kps_label_updater
	global kps_max_label_updater
	_e = elapsed_t()

	if timerStarted is False:		
		timerStarted = True
		print('timer started')

	kps_ = kps(k,1)
	kps_label_updater = str(kps_)
	window.KPS_DISPLAY.SetLabel('<KPS>: ' + kps_label_updater)

	if kps_ > max_kps:
		max_kps = kps_
		kps_max_label_updater = str(max_kps)
		window.KPS_MAX_DISPLAY.SetLabel('<MAX_KPS>: ' + kps_max_label_updater)

	if _e >= bound+rate*10:		
		window.KPS_DISPLAY.SetLabel('<KPS>: 0')
		print('timer stoped, max kps:', max_kps)
		reset()	
		clock.stop()


def clockSchedule():
	global timerRunning
	global k
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
	timerStarted = False
	timerRunning = False
	last[0] = 0
	k = 0
	elapsed_t()

def kps(key, t):
	if key != 0:
		return round(key/t)
	else:
		return 0

def pressed_T(e):
	clockSchedule()

def pressed_Y(e):
	clockSchedule()

def pressed_O(e):
	clockSchedule()

def pressed_P(e):
	clockSchedule()


'''UNIQUE LISTENERS'''
keyboard.on_press_key(20,pressed_T)
keyboard.on_press_key(21,pressed_Y)
keyboard.on_press_key(24,pressed_O)
keyboard.on_press_key(25,pressed_P)

'''COCK'''
clock = task.LoopingCall(timer)

'''WX'''
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

# start the event loop:
reactor.run()