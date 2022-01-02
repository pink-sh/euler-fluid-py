import sys

import wx
import wx.glcanvas as glcanvas
import random
from container import Container
from constants import SIZE, SCALE, PAGE_SIZE
from pprint import pprint
from threading import Thread
import time
from IX import IX, getIdx
from profile import profile


try:
	from OpenGL.GL import *
	from OpenGL.GLUT import *
	haveOpenGL = True
except ImportError:
	haveOpenGL = False

#----------------------------------------------------------------------

EVT_RESULT_ID = wx.Window.NewControlId()

def EVT_RESULT(win, func):
	win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
	def __init__(self, data):
		wx.PyEvent.__init__(self)
		self.SetEventType(EVT_RESULT_ID)
		self.data = data

class ChildThread(Thread):

	def __init__(self, myframe, type_, position):
		Thread.__init__(self)
		self.myframe = myframe

		self.mytype = type_
		self.myposition = position
		
		self.aborting = False
		self.start()

	def run(self):
		while True:
			time.sleep(0.5)
			if self.aborting == True:
				break

			obj = type('th', (object,),
				{'type': self.mytype, 'position': self.myposition})()

			wx.PostEvent(self.myframe, ResultEvent(obj))

	def abort(self):
		self.aborting = True

	def setType(self, type):
		self.mytype = type

	def setPosition(self, position):
		self.myposition = position


class MyCanvasBase(glcanvas.GLCanvas):
	def __init__(self, parent):
		glcanvas.GLCanvas.__init__(self, parent, -1)
		self.init = False
		self.context = glcanvas.GLContext(self)

		self.lastx = self.x = 30
		self.lasty = self.y = 30
		self.size = None

		self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_MOUSE_EVENTS, self.handleMouse)
		self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
		self.worker = None
		EVT_RESULT(self,self.OnMousePressed)


	def stopWorker(self):
		if (self.worker is not None):
			self.worker.abort()
			self.worker = None


	def OnSize(self, event):
		wx.CallAfter(self.DoSetViewport)
		event.Skip()


	def DoSetViewport(self):
		size = self.size = self.GetClientSize()
		self.SetCurrent(self.context)
		glViewport(0, 0, size.width, size.height)

	def OnPaint(self, event):
		dc = wx.PaintDC(self)
		self.SetCurrent(self.context)
		if not self.init:
			self.InitGL()
			self.init = True
		self.OnDraw()

	def OnMouseUp(self, event):
		print("Killing Worker")
		self.stopWorker()

	


class FluidCanvas(MyCanvasBase):
	def __init__(self, parent):
		super().__init__(parent)
		self.mouseClick = False
		self.currentAction = None
		self.previousPosition=(0,0)
		self.dc = wx.ClientDC(self)
		self.container = Container( 0.2, 0, 0.0000001 )

	def InitUI(self):
		self.Bind(wx.EVT_PAINT, self.OnPaint) 
		self.Centre() 
		self.Show(True)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		# glMatrixMode (GL_MODELVIEW)
		# glLoadIdentity()

		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

		# self.container = Container( 0.2, 0, 0.0000001 )

	def OnPaint(self, e):
		dc = wx.PaintDC(self)
		dc.Clear()
		dc.SetBrush(wx.Brush(wx.Colour(0,255,0)))
		# dc.DrawRectangle(0, 0, 10, 10)

		boundSize = int(PAGE_SIZE/SIZE)
		for x in range(0,640,boundSize-1):
			for y in range(0,640,boundSize-1):
				# print(IX(x/boundSize,y/boundSize,SIZE))
				# idx = getIdx(x/boundSize,y/boundSize)
				alpha = 0
				# if idx in self.container.density.keys():
				if int(x/boundSize) < SIZE and int(y/boundSize) < SIZE:
					alpha = 255 if self.container.density[int(x/boundSize)][int(y/boundSize)] > 255 else self.container.density[int(x/boundSize)][int(y/boundSize)]
				dc.SetBrush(wx.Brush(wx.Colour(0,255,0,alpha=int(alpha))))
				dc.DrawRectangle(x,y, boundSize, boundSize)

		self.SwapBuffers()	

	
	def OnMousePressed(self, evt):
		self.currentAction = evt.data.type
		pos = evt.data.position

		# print(self.currentAction, pos[0], pos[1])

		boundSize = int(PAGE_SIZE/SIZE)

		x = int(pos[0]/boundSize)
		y = int(pos[1]/boundSize)

		if self.currentAction == 'pushing':
			self.container.AddDensity(y, x, 200)


		amountX = x - self.previousPosition[0]
		amountY = y - self.previousPosition[1]

		# self.container.AddVelocity(pos[1]/SCALE, pos[0]/SCALE, amountY / 10, amountX / 10)
		if self.currentAction == 'dragging':
			self.container.AddVelocity(y, x, amountY / 10, amountX / 10)

		self.previousPosition = (x,y)

		self.container.Step()
		
		# wx.Frame.Update(self)
		self.Refresh()
		# self.Update()

	def handleMouse(self,evt):
		if evt.Dragging():
			if (self.currentAction == 'pushing'):
				self.worker.setType('dragging')
			self.worker.setPosition(evt.GetPosition())

		if evt.LeftDown():
			self.worker = ChildThread(myframe=self, type_="pushing", position=evt.GetPosition())

		if evt.LeftUp():
			self.stopWorker()




#----------------------------------------------------------------------


if __name__ == '__main__':
	app = wx.App(False)
	if not haveOpenGL:
		wx.MessageBox('This sample requires the PyOpenGL package.', 'Sorry')
	else:
		frm = wx.Frame(None, -1, title='Fluid Sample', size=(PAGE_SIZE, PAGE_SIZE), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
		canvas = FluidCanvas(frm)
		frm.Show()
	app.MainLoop()