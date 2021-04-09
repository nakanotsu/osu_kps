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
# warnings.filterwarnings("ignore", category=DeprecationWarning)

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
	global open_files
	global f
	global f2
	window.KPS_DISPLAY.SetLabel('<KPS>: ' + kps_label_updater)
	window.KPS_MAX_DISPLAY.SetLabel('<MAX_KPS>: ' + kps_max_label_updater)
	with open("kps.txt", "w") as f:
		f.write(kps_label_updater)
	with open("max_kps.txt", "w") as f2:
		f2.write(kps_max_label_updater)	

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
		if clock.running is False: # double check for clock already started bug
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

def listener_checker():
	print('CLOCKS RUNNING...')
	print('clock(timer): ', clock.running)
	print('clock(no_events): ', clock2.running)
	print('clock(listener_checker): ', clock3.running)	
	'''LISTENER'''
	keyboard.unhook_all() #PREVENTS LISTENER IS REMOVED BUG, REMOVE HOOK, THEN ADD AGAIN EVERY SECOND.
	print('UNHOOKED')
	keyboard.on_press(clockSchedule)
	print('HOOKED')
	print('---')


'''CLOCKS'''
clock = task.LoopingCall(timer)
clock2 = task.LoopingCall(no_events)
clock3 = task.LoopingCall(listener_checker)

'''GUI'''
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
clock3.start(1)
reactor.run()
# print (reactor stopped?)
print('reactor end')