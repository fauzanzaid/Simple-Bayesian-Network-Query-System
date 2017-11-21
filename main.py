#! /usr/bin/python2


import threading


class Main(threading.Thread):
	"""docstring for Main"""
	def __init__(self, qu_usr_ip, qu_cmd):
		super(Main, self).__init__()
		self.qu_usr_ip = qu_usr_ip
		self.qu_cmd = qu_cmd


	def send_cmd(self, cmd, *args):
		msg = (cmd, args)
		self.qu_cmd.put(msg)


	def run(self):

		while True:
			usr_ip = self.qu_usr_ip.get()
			time, dev, arg = usr_ip
			# print "Main rcvd", usr_ip

			if arg == 'q':
				self.send_cmd("quit")
				break
