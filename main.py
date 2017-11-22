#! /usr/bin/python2


import threading

from bayesian_network import BayesianNetwork


class Main(threading.Thread):
	"""docstring for Main"""
	def __init__(self, qu_usr_ip, qu_cmd):
		super(Main, self).__init__()
		self.qu_usr_ip = qu_usr_ip
		self.qu_cmd = qu_cmd

		self.input_filename = "input1.txt"

		self.init_network()


	def init_network(self):
		self.bn = BayesianNetwork()
		self.bn.init_from_file(self.input_filename)
		self.node_names = [n.name for n in self.bn.nodes]


	def send_cmd(self, cmd, *args):
		msg = (cmd, args)
		self.qu_cmd.put(msg)


	def run(self):

		self.send_cmd("init_node_names", self.node_names)
		self.send_cmd("draw_base")

		while True:
			usr_ip = self.qu_usr_ip.get()
			t, dev, arg = usr_ip
			# print "Main rcvd", usr_ip

			if dev == "keypress":
				if arg == 'q':
					self.send_cmd("quit")
					break

			else:
				if arg == None:
					pass

				elif arg[0] == "qry":
					pass

				elif arg[0] == "cond":
					pass

				elif arg[0] == "mrkv":
					pass
