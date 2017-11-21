#! /usr/bin/python2


import threading


class Main(threading.Thread):
	"""docstring for Main"""
	def __init__(self, qu_usr_ip, qu_cmd):
		super(Main, self).__init__()
		self.qu_usr_ip = qu_usr_ip
		self.qu_cmd = qu_cmd


	def run(self):
		pass
