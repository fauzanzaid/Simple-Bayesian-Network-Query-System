#! /usr/bin/python2
# -*- coding: utf-8 -*-

import threading

from bayesian_network import BayesianNetwork, get_prob_from_names


class Main(threading.Thread):
	"""docstring for Main"""

	MAX_SEL = 10

	MSG_WELCOME = "Welcome to Bayesian Network solver! Press q to quit"
	MSG_SEL_LMT = "You cannot select more than 10 variables!"
	MSG_WORKING = "Calculating probability..."

	def __init__(self, qu_usr_ip, qu_cmd, input_filename="input1.txt"):
		super(Main, self).__init__()
		self.qu_usr_ip = qu_usr_ip
		self.qu_cmd = qu_cmd

		self.input_filename = input_filename
		self.init_network()

		self.cur_names_qry = []
		self.cur_names_cond = []
		self.cur_name_mrkv = None


	def init_network(self):
		self.bn = BayesianNetwork()
		self.bn.init_from_file(self.input_filename)
		self.node_names = sorted([n.name for n in self.bn.nodes])


	def send_cmd(self, cmd, *args):
		msg = (cmd, args)
		self.qu_cmd.put(msg)


	def run(self):

		self.send_cmd("init_node_names", self.node_names)
		self.send_cmd("draw_base")
		self.send_cmd("display_msg", self.MSG_WELCOME)

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

				elif arg[0] == "qry" or arg[0] == "cond":

					if arg[0] == "qry":
						if arg[1] in self.cur_names_qry:
							self.send_cmd("off", arg[0], arg[1])
							self.cur_names_qry.remove(arg[1])
						elif arg[1][1:] in self.cur_names_qry:
							self.send_cmd("off", arg[0], arg[1][1:])
							self.cur_names_qry.remove(arg[1][1:])
							self.send_cmd("on", arg[0], arg[1])
							self.cur_names_qry.append(arg[1])
						elif "~"+arg[1] in self.cur_names_qry:
							self.send_cmd("off", arg[0], "~"+arg[1])
							self.cur_names_qry.remove("~"+arg[1])
							self.send_cmd("on", arg[0], arg[1])
							self.cur_names_qry.append(arg[1])
						elif len(self.cur_names_qry) < self.MAX_SEL:
							self.send_cmd("on", arg[0], arg[1])
							self.cur_names_qry.append(arg[1])
						else:
							self.send_cmd("display_msg", self.MSG_SEL_LMT)
							continue

					elif arg[0] == "cond":
						if arg[1] in self.cur_names_cond:
							self.send_cmd("off", arg[0], arg[1])
							self.cur_names_cond.remove(arg[1])
						elif arg[1][1:] in self.cur_names_cond:
							self.send_cmd("off", arg[0], arg[1][1:])
							self.cur_names_cond.remove(arg[1][1:])
							self.send_cmd("on", arg[0], arg[1])
							self.cur_names_cond.append(arg[1])
						elif "~"+arg[1] in self.cur_names_cond:
							self.send_cmd("off", arg[0], "~"+arg[1])
							self.cur_names_cond.remove("~"+arg[1])
							self.send_cmd("on", arg[0], arg[1])
							self.cur_names_cond.append(arg[1])
						elif len(self.cur_names_cond) < self.MAX_SEL:
							self.send_cmd("on", arg[0], arg[1])
							self.cur_names_cond.append(arg[1])
						else:
							self.send_cmd("display_msg", self.MSG_SEL_LMT)
							continue

					# Calc
					p = get_prob_from_names(self.bn, self.cur_names_qry, self.cur_names_cond)
					self.send_cmd("display_expr", p.to_string())
					self.send_cmd("display_msg", self.MSG_WORKING)
					val = p.evaluate(self.bn)
					self.send_cmd("display_prob", val)

				elif arg[0] == "mrkv":
					if self.cur_name_mrkv != None:
						self.send_cmd("off", arg[0], self.cur_name_mrkv)
					self.send_cmd("on", arg[0], arg[1])
					self.cur_name_mrkv = arg[1]

					cur_node_mrkv = self.bn.nodes_by_name[self.cur_name_mrkv]
					mrkv_blanket = cur_node_mrkv.get_markov_blanket()
					self.send_cmd("draw_mrkv", [n.name for n in mrkv_blanket])
