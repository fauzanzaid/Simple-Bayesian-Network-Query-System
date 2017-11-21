#! /usr/bin/python2
# -*- coding: utf-8 -*-

import time

import turtle


class GUI(object):
	"""docstring for GUI"""
	
	DISPATCH_DELAY = 1
	
	def __init__(self, qu_usr_ip, qu_cmd):
		self.time_init = time.time()
		
		self.qu_usr_ip = qu_usr_ip
		self.qu_cmd = qu_cmd

		self.set_constants()

		self.node_names = []


	def set_constants(self):

		#    ┌───────────┐   
		#    │     1     │   
		# ┌──┴──┬─────┬──┴──┐
		# │     │     │     │
		# │  2  │  3  │  4  │
		# │     │     │     │
		# └──┬──┴─────┴──┬──┘
		#    │     5     │   
		#    └───────────┘   


		self.MAX_VAR = 25

		self.LIN_SPC = 16
		self.P_PAD = 20
		self.W_PAD = 50

		self.TTL_BOX_HT = TitleBox.HT
		self.TTL_BOX_WD = TitleBox.WD
		self.TXT_BOX_HT = TextBox.HT
		self.TXT_BOX_WD = TextBox.WD

		self.P1_HT = self.LIN_SPC*3
		self.P1_WD = 400
		self.P2_HT = self.P3_HT = self.P4_HT = self.TTL_BOX_HT + self.TXT_BOX_HT*self.MAX_VAR
		self.P2_WD = self.P3_WD = self.P4_WD = max(self.TTL_BOX_WD, self.TXT_BOX_WD*2)
		self.P5_HT = self.LIN_SPC*2
		self.P5_WD = 400

		self.P1_HTP = self.P1_HT + 2*self.P_PAD
		self.P2_HTP = self.P3_HTP = self.P4_HTP = self.P2_HT + 2*self.P_PAD
		self.P5_HTP = self.P5_HT + 2*self.P_PAD

		self.P1_WDP = self.P1_WD + 2*self.P_PAD
		self.P2_WDP = self.P3_WDP = self.P4_WDP = self.P2_WD + 2*self.P_PAD
		self.P5_WDP = self.P5_WD + 2*self.P_PAD

		self.W_HT = self.P1_HTP + self.P2_HTP + self.P5_HTP
		self.W_WD = max(self.P1_WDP, self.P2_WDP*3, self.P5_WDP)
		self.W_HTP = self.W_HT + 2*self.W_PAD
		self.W_WDP = self.W_WD + 2*self.W_PAD

		self.P1_XP = max(0, ( max(self.P2_WDP*3,self.P5_WDP) - self.P1_WDP )/2.0)
		self.P2_XP = max(0, ( max(self.P1_WDP,self.P5_WDP) - self.P2_WDP*3 )/2.0)
		self.P3_XP = self.P2_XP + self.P2_WDP
		self.P4_XP = self.P3_XP + self.P3_WDP
		self.P5_XP = max(0, ( max(self.P2_WDP*3,self.P1_WDP) - self.P5_WDP )/2.0)

		self.P1_YP = self.P5_HTP + self.P2_HTP + self.P1_HTP
		self.P2_YP = self.P5_HTP + self.P2_HTP
		self.P3_YP = self.P2_YP
		self.P4_YP = self.P2_YP
		self.P5_YP = self.P5_HTP

		self.P1_X = self.P_PAD + self.P1_XP
		self.P2_X = self.P_PAD + self.P2_XP
		self.P3_X = self.P_PAD + self.P3_XP
		self.P4_X = self.P_PAD + self.P4_XP
		self.P5_X = self.P_PAD + self.P5_XP

		self.P1_Y = - self.P_PAD + self.P1_YP
		self.P2_Y = - self.P_PAD + self.P2_YP
		self.P3_Y = - self.P_PAD + self.P3_YP
		self.P4_Y = - self.P_PAD + self.P4_YP
		self.P5_Y = - self.P_PAD + self.P5_YP


	def draw_base(self):
		self.draw_base_P1()
		self.draw_base_P2()
		self.draw_base_P3()
		self.draw_base_P4()
		self.draw_base_P5()


	def draw_base_P1(self):
		self.draw_boundary(self.P1_XP, self.P1_YP, self.P1_HTP, self.P1_WDP)


	def draw_base_P2(self):
		self.draw_boundary(self.P2_XP, self.P2_YP, self.P2_HTP, self.P2_WDP)


	def draw_base_P3(self):
		self.draw_boundary(self.P3_XP, self.P3_YP, self.P3_HTP, self.P3_WDP)


	def draw_base_P4(self):
		self.draw_boundary(self.P4_XP, self.P4_YP, self.P4_HTP, self.P4_WDP)


	def draw_base_P5(self):
		self.draw_boundary(self.P5_XP, self.P5_YP, self.P5_HTP, self.P5_WDP)


	def draw_boundary(self, cood_x, cood_y, ht, wd):
		old_color = self.ttl_base.color()

		self.ttl_base.goto(cood_x, cood_y)

		self.ttl_base.pd()
		self.ttl_base.color((0.9,0.9,0.9))

		self.ttl_base.seth(0)
		self.ttl_base.fd(wd)
		self.ttl_base.rt(90)
		self.ttl_base.fd(ht)
		self.ttl_base.rt(90)
		self.ttl_base.fd(wd)
		self.ttl_base.rt(90)
		self.ttl_base.fd(ht)
		self.ttl_base.rt(90)

		self.ttl_base.color(*old_color)
		self.ttl_base.pu()


	def send_mouse_click(self, x, y):
		pos = None
		msg = (time.time()-self.time_init, "mouse", pos)
		self.qu_usr_ip.put(msg)


	def send_key_press(self, key):
		msg = (time.time()-self.time_init, "keypress", key)
		self.qu_usr_ip.put(msg)


	def cmd_dispatcher(self):
		if self.qu_cmd.empty():
			self.scr.ontimer(self.cmd_dispatcher, self.DISPATCH_DELAY)
			return

		func, args = self.qu_cmd.get()

		if func == "quit":
			self.scr.onclick(None)
			self.scr.onkey(None, "q")
			self.scr.bye()
			return

		elif func == "init_node_names":
			self.node_names = args[0]

		elif func == "draw_base":
			self.draw_base()

		self.scr.ontimer(self.cmd_dispatcher, self.DISPATCH_DELAY)


	def run(self):
		self.scr = turtle.Screen()
		self.scr.setup(width=self.W_WDP, height=self.W_HTP)
		self.scr.setworldcoordinates(0-self.W_PAD, 0-self.W_PAD, self.W_WD+self.W_PAD, self.W_HT+self.W_PAD)
		self.scr.title("Bayesian Network Solver")
		self.scr.delay(0)

		self.ttl_base = turtle.Turtle()
		self.ttl_base.ht()
		self.ttl_base.pu()
		self.ttl_base.speed(0)
		self.ttl_base.tracer(0,0)

		self.scr.ontimer(self.cmd_dispatcher, self.DISPATCH_DELAY)
		self.scr.onclick(self.send_mouse_click)
		self.scr.onkey(lambda:self.send_key_press("q"), "q")
		self.scr.listen()

		turtle.done()
		self.send_key_press("q")



class TextBox(object):
	"""docstring for TextBox"""

	WD = 100
	HT = 20
	PAD = 5
	TXT_PAD = 2
	COL = ((0,0,0),(0.9,0.9,0.9))

	WDP = WD + PAD*2
	HTP = HT + PAD*2


	def __init__(self, ttl_base, cood_x, cood_y, text=""):
		self.ttl_base = ttl_base
		self.cood_x = cood_x
		self.cood_y = cood_y
		self.text = text


	def draw_base(self):
		old_color = self.ttl_base.color()
		# old_size = self.ttl_base.pensize()

		self.ttl_base.goto(self.cood_x, self.cood_y)

		self.ttl_base.pd()
		self.ttl_base.color(*self.COL)
		# self.ttl_base.pensize(old_size)
		self.ttl_base.fill(True)

		self.ttl_base.seth(0)
		self.ttl_base.fd(self.WD)
		self.ttl_base.rt(90)
		self.ttl_base.fd(self.HT)
		self.ttl_base.rt(90)
		self.ttl_base.fd(self.WD)
		self.ttl_base.rt(90)
		self.ttl_base.fd(self.HT)
		self.ttl_base.rt(90)

		self.ttl_base.fill(False)
		# self.ttl_base.pensize(old_size)
		self.ttl_base.color(*old_color)
		self.ttl_base.pu()

		self.write()


	def write(self):
		self.ttl_base.goto(self.cood_x+self.TXT_PAD, self.cood_y-self.HT+self.TXT_PAD)
		self.ttl_base.write(self.text, font=("Mono", 8, "normal"))



class TitleBox(TextBox):
	"""docstring for TitleBox"""

	WD = 150
	HT = 30
	PAD = 5
	TXT_PAD = 7
	COL = ((0,0,0),(0.8,0.8,1.0))


	WDP = WD + PAD*2
	HTP = HT + PAD*2

	def __init__(self, ttl_base, cood_x, cood_y, text=""):
		super(TitleBox, self).__init__(ttl_base, cood_x, cood_y, text)



class ButtonBox(TextBox):
	"""docstring for ButtonBox"""

	COL = ((0,0,0),(0.7,0.8,0.7))
	COL_ON = ((0,0,0),(0.8,1.0,0.8))

	def __init__(self, ttl_base, cood_x, cood_y, text=""):
		super(ButtonBox, self).__init__(ttl_base, cood_x, cood_y, text)
		self.ttl_lit = turtle.Turtle()
		self.ttl_lit.ht()
		self.ttl_lit.pu()
		self.ttl_lit.speed(0)
		self.ttl_lit.tracer(0,0)


	def on(self):
		old_color = self.ttl_base.color()
		# old_size = self.ttl_base.pensize()

		self.ttl_base.goto(self.cood_x, self.cood_y)

		self.ttl_base.pd()
		self.ttl_base.color(*self.COL_ON)
		# self.ttl_base.pensize(old_size)
		self.ttl_base.fill(True)

		self.ttl_base.seth(0)
		self.ttl_base.fd(self.WD)
		self.ttl_base.rt(90)
		self.ttl_base.fd(self.HT)
		self.ttl_base.rt(90)
		self.ttl_base.fd(self.WD)
		self.ttl_base.rt(90)
		self.ttl_base.fd(self.HT)
		self.ttl_base.rt(90)

		self.ttl_base.fill(False)
		# self.ttl_base.pensize(old_size)
		self.ttl_base.color(*old_color)
		self.ttl_base.pu()

		self.write()


	def off(self):
		self.ttl_lit.clear()
