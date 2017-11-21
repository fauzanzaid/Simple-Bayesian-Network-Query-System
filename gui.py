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

		self.TXT_BOX_HT = 20
		self.TXT_BOX_WD = 100
		self.TTL_BOX_HT = 20
		self.TTL_BOX_WD = 100

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

		self.P1_X = self.P_PAD + max(0, ( max(self.P2_WDP*3,self.P5_WDP) - self.P1_WDP )/2.0)
		self.P2_X = self.P_PAD + max(0, ( max(self.P1_WDP,self.P5_WDP) - self.P2_WDP*3 )/2.0)
		self.P3_X = self.P_PAD + self.P2_X + self.P2_WDP
		self.P4_X = self.P_PAD + self.P3_X + self.P3_WDP
		self.P5_X = self.P_PAD + max(0, ( max(self.P2_WDP*3,self.P1_WDP) - self.P5_WDP )/2.0)

		self.P1_Y = - self.P_PAD + self.P5_HTP + self.P2_HTP
		self.P2_Y = - self.P_PAD + self.P5_HTP
		self.P3_Y = self.P2_Y
		self.P4_Y = self.P2_Y
		self.P5_Y = - self.P_PAD + 0


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
			pass


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
