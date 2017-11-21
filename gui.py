#! /usr/bin/python2


import time

import turtle


class GUI(object):
	"""docstring for GUI"""
	
	DISPATCH_DELAY = 1
	
	def __init__(self, qu_usr_ip, qu_cmd):
		self.time_init = time.time()
		
		self.qu_usr_ip = qu_usr_ip
		self.qu_cmd = qu_cmd


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
		pass
