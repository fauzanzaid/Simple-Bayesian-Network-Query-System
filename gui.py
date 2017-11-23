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


		self.MAX_VAR = 15

		self.LIN_SPC = 16
		self.P_PAD = 20
		self.W_PAD = 50

		self.TTL_BOX_HT = TitleBox.HTP
		self.TTL_BOX_WD = TitleBox.WDP
		self.TXT_BOX_HT = TextBox.HTP
		self.TXT_BOX_WD = TextBox.WDP

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
		self.init_P2_boxes()
		self.draw_boundary(self.P2_XP, self.P2_YP, self.P2_HTP, self.P2_WDP)
		self.P2_ttl_box.draw_base()
		for box in self.P2_btn_boxes:
			box.draw_base()


	def draw_base_P3(self):
		self.init_P3_boxes()
		self.draw_boundary(self.P3_XP, self.P3_YP, self.P3_HTP, self.P3_WDP)
		self.P3_ttl_box.draw_base()
		for box in self.P3_btn_boxes:
			box.draw_base()


	def draw_base_P4(self):
		self.init_P4_boxes()
		self.draw_boundary(self.P4_XP, self.P4_YP, self.P4_HTP, self.P4_WDP)
		self.P4_ttl_box.draw_base()
		for box in self.P4_btn_boxes:
			box.draw_base()


	def draw_mrkv_P4(self, node_names):
		self.ttl_mrkv.clear()
		mrkv_boxes = []
		for i,name in enumerate(node_names):
			mrkv_boxes.append(TextBox(self.ttl_mrkv, self.P4_X + TextBox.WDP, self.P4_Y - TitleBox.HTP - i*TextBox.HTP, name))
		for box in mrkv_boxes:
			box.draw_base()


	def draw_base_P5(self):
		self.draw_boundary(self.P5_XP, self.P5_YP, self.P5_HTP, self.P5_WDP)


	def init_P2_boxes(self):
		self.P2_ttl_box = TitleBox(self.ttl_base, self.P2_X, self.P2_Y, "Query variables")
		self.P2_btn_boxes = []
		for i,name in enumerate(self.node_names):
			self.P2_btn_boxes.append(ButtonBox(self.ttl_base, self.P2_X, self.P2_Y - TitleBox.HTP - i*ButtonBox.HTP, name))
			self.P2_btn_boxes.append(ButtonBox(self.ttl_base, self.P2_X + ButtonBox.WDP, self.P2_Y - TitleBox.HTP - i*ButtonBox.HTP, "~"+name))


	def init_P3_boxes(self):
		self.P3_ttl_box = TitleBox(self.ttl_base, self.P3_X, self.P3_Y, "Condition variables")
		self.P3_btn_boxes = []
		for i,name in enumerate(self.node_names):
			self.P3_btn_boxes.append(ButtonBox(self.ttl_base, self.P3_X, self.P3_Y - TitleBox.HTP - i*ButtonBox.HTP, name))
			self.P3_btn_boxes.append(ButtonBox(self.ttl_base, self.P3_X + ButtonBox.WDP, self.P3_Y - TitleBox.HTP - i*ButtonBox.HTP, "~"+name))


	def init_P4_boxes(self):
		self.P4_ttl_box = TitleBox(self.ttl_base, self.P4_X, self.P4_Y, "Markov Blanket")
		self.P4_btn_boxes = []
		for i,name in enumerate(self.node_names):
			self.P4_btn_boxes.append(ButtonBox(self.ttl_base, self.P4_X, self.P4_Y - TitleBox.HTP - i*ButtonBox.HTP, name))


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


	def get_box_by_name(self, section, name):
		if section == "qry":
			btn_boxes = self.P2_btn_boxes
		elif section == "cond":
			btn_boxes = self.P3_btn_boxes
		elif section == "mrkv":
			btn_boxes = self.P4_btn_boxes
		else:
			return None

		for box in btn_boxes:
			if box.text == name:
				return box
		return None


	def get_box_from_cood(self, x, y):
		for i,box in enumerate(self.P2_btn_boxes):
			if box.cood_in_box(x,y):
				return ("qry", box.text)
		for i,box in enumerate(self.P3_btn_boxes):
			if box.cood_in_box(x,y):
				return ("cond", box.text)
		for i,box in enumerate(self.P4_btn_boxes):
			if box.cood_in_box(x,y):
				return ("mrkv", box.text)
		return None


	def send_mouse_click(self, x, y):
		box = self.get_box_from_cood(x,y)
		msg = (time.time()-self.time_init, "mouse", box)
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

		elif func == "on":
			self.get_box_by_name(args[0], args[1]).on()

		elif func == "off":
			self.get_box_by_name(args[0], args[1]).off()
		elif func == "draw_mrkv":
			self.draw_mrkv_P4(args[0])

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

		self.ttl_mrkv = turtle.Turtle()
		self.ttl_mrkv.ht()
		self.ttl_mrkv.pu()
		self.ttl_mrkv.speed(0)
		self.ttl_mrkv.tracer(0,0)

		self.scr.ontimer(self.cmd_dispatcher, self.DISPATCH_DELAY)
		self.scr.onclick(self.send_mouse_click)
		self.scr.onkey(lambda:self.send_key_press("q"), "q")
		self.scr.listen()

		turtle.done()
		self.send_key_press("q")



class TextBox(object):
	"""docstring for TextBox"""

	WD = 72.5
	HT = 20
	PAD = 2.5
	TXT_PAD_X = 7
	TXT_PAD_Y = 2
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

		self.ttl_base.goto(self.cood_x+self.PAD, self.cood_y-self.PAD)

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

		self.ttl_base.goto(self.cood_x + self.PAD + self.TXT_PAD_X, self.cood_y - self.HTP + self.PAD + self.TXT_PAD_Y)
		self.ttl_base.write(self.text, font=("Mono", 8, "normal"))



class TitleBox(TextBox):
	"""docstring for TitleBox"""

	WD = 150
	HT = 20
	PAD = 2.5
	TXT_PAD = 2
	COL = ((0,0,0),(0.7,0.7,1.0))


	WDP = WD + PAD*2
	HTP = HT + PAD*2

	def __init__(self, ttl_base, cood_x, cood_y, text=""):
		super(TitleBox, self).__init__(ttl_base, cood_x, cood_y, text)



class ButtonBox(TextBox):
	"""docstring for ButtonBox"""

	COL = ((0,0,0),(0.7,0.8,0.7))
	COL_ON = ((0,0,0),(1.0,1.0,0.8))

	def __init__(self, ttl_base, cood_x, cood_y, text=""):
		super(ButtonBox, self).__init__(ttl_base, cood_x, cood_y, text)
		self.ttl_lit = turtle.Turtle()
		self.ttl_lit.ht()
		self.ttl_lit.pu()
		self.ttl_lit.speed(0)
		self.ttl_lit.tracer(0,0)


	def on(self):
		old_color = self.ttl_lit.color()
		# old_size = self.ttl_lit.pensize()

		self.ttl_lit.goto(self.cood_x+self.PAD, self.cood_y-self.PAD)

		self.ttl_lit.pd()
		self.ttl_lit.color(*self.COL_ON)
		# self.ttl_lit.pensize(old_size)
		self.ttl_lit.fill(True)

		self.ttl_lit.seth(0)
		self.ttl_lit.fd(self.WD)
		self.ttl_lit.rt(90)
		self.ttl_lit.fd(self.HT)
		self.ttl_lit.rt(90)
		self.ttl_lit.fd(self.WD)
		self.ttl_lit.rt(90)
		self.ttl_lit.fd(self.HT)
		self.ttl_lit.rt(90)

		self.ttl_lit.fill(False)
		# self.ttl_lit.pensize(old_size)
		self.ttl_lit.color(*old_color)
		self.ttl_lit.pu()

		self.ttl_lit.goto(self.cood_x + self.PAD + self.TXT_PAD_X, self.cood_y - self.HTP + self.PAD + self.TXT_PAD_Y)
		self.ttl_lit.write(self.text, font=("Mono", 8, "normal"))


	def off(self):
		self.ttl_lit.clear()


	def cood_in_box(self, x, y):
		if self.cood_x <= x <= self.cood_x + self.WD:
			if self.cood_y >= y >= self.cood_y - self.HT:
				return True
		return False
