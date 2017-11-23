#! /usr/bin/python2
# -*- coding: utf-8 -*-

import threading

from bayesian_network import BayesianNetwork


class Main(threading.Thread):
	"""docstring for Main"""

	MAX_SEL = 10

	def __init__(self, qu_usr_ip, qu_cmd):
		super(Main, self).__init__()
		self.qu_usr_ip = qu_usr_ip
		self.qu_cmd = qu_cmd

		self.input_filename = "input1.txt"
		self.init_network()

		self.cur_names_qry = []
		self.cur_names_cond = []
		self.cur_name_mrkv = None


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
					if arg[1] in self.cur_names_qry:
						self.send_cmd("off", arg[0], arg[1])
						self.cur_names_qry.remove(arg[1])
						# Calc
					elif arg[1][1:] in self.cur_names_qry:
						self.send_cmd("off", arg[0], arg[1][1:])
						self.cur_names_qry.remove(arg[1][1:])
						self.send_cmd("on", arg[0], arg[1])
						self.cur_names_qry.append(arg[1])
						# Calc
					elif "~"+arg[1] in self.cur_names_qry:
						self.send_cmd("off", arg[0], "~"+arg[1])
						self.cur_names_qry.remove("~"+arg[1])
						self.send_cmd("on", arg[0], arg[1])
						self.cur_names_qry.append(arg[1])
						# Calc
					elif len(self.cur_names_qry) < self.MAX_SEL:
						self.send_cmd("on", arg[0], arg[1])
						self.cur_names_qry.append(arg[1])
						# Calc
					else:
						pass
						# Send msg

				elif arg[0] == "cond":
					if arg[1] in self.cur_names_cond:
						self.send_cmd("off", arg[0], arg[1])
						self.cur_names_cond.remove(arg[1])
						# Calc
					elif arg[1][1:] in self.cur_names_cond:
						self.send_cmd("off", arg[0], arg[1][1:])
						self.cur_names_cond.remove(arg[1][1:])
						self.send_cmd("on", arg[0], arg[1])
						self.cur_names_cond.append(arg[1])
						# Calc
					elif "~"+arg[1] in self.cur_names_cond:
						self.send_cmd("off", arg[0], "~"+arg[1])
						self.cur_names_cond.remove("~"+arg[1])
						self.send_cmd("on", arg[0], arg[1])
						self.cur_names_cond.append(arg[1])
						# Calc
					elif len(self.cur_names_cond) < self.MAX_SEL:
						self.send_cmd("on", arg[0], arg[1])
						self.cur_names_cond.append(arg[1])
						# Calc
					else:
						pass
						# Send msg

				elif arg[0] == "mrkv":
					if self.cur_name_mrkv != None:
						self.send_cmd("off", arg[0], self.cur_name_mrkv)
					self.send_cmd("on", arg[0], arg[1])
					self.cur_name_mrkv = arg[1]

					cur_node_mrkv = self.bn.nodes_by_name[self.cur_name_mrkv]
					mrkv_blanket = cur_node_mrkv.get_markov_blanket()
					self.send_cmd("draw_mrkv", [n.name for n in mrkv_blanket])
