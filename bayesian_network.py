#! /usr/bin/python2

import re

class BayesianNetwork(object):
	"""docstring for BayesianNetwork"""
	def __init__(self):
		self.nodes = []
		self.nodes_by_name = {}


	def init_from_file(self, input_filename):

		parent_names_by_name = {}
		cpt_list_by_name = {}

		with open(input_filename) as f:
			for l in f:
				if l == "$$":
					break

				l = re.split(r"[>]", l[:-1])
				l = [i.strip() for i in l]
				l = filter(None,l)

				name = l[0]
				parent_names = re.split(r"[\[\], ]", l[1])
				parent_names = filter(None, parent_names)
				cpt_list = re.split(r" ",l[2])

				self.nodes.append(BayesianNetworkNode(name))
				self.nodes[-1].cpt_list = cpt_list

				self.nodes_by_name[name] = self.nodes[-1]
				parent_names_by_name[name] = parent_names

		for k in self.nodes_by_name:
			for pn in parent_names_by_name[k]:
				self.nodes_by_name[k].parents.append(self.nodes_by_name[pn])
				self.nodes_by_name[pn].children.append(self.nodes_by_name[k])



class BayesianNetworkNode(object):
	"""docstring for BayesianNetworkNode"""
	def __init__(self, name):
		self.name = name
		self.parents = []
		self.children = []
		self.cpt_list = None

	def get_markov_blanket(self):
		markov_blanket = []
		for node_p in self.parents:
			markov_blanket.append(node_p)
		for node_c in self.children:
			if node_c not in markov_blanket:
				markov_blanket.append(node_c)
			for node_cp in node_c.parents:
				if node_cp not in markov_blanket:
					markov_blanket.append(node_cp)
		if self in markov_blanket:
			markov_blanket.remove(self)
		return markov_blanket



class Event(object):
	"""docstring for Event"""
	def __init__(self, node, value=None):
		self.node = node
		self.value = value



class ConditionalProbability(object):
	"""docstring for ConditionalProbability"""
	def __init__(self, events_query, events_evidence=[]):
		self.events_query = events_query
		self.events_evidence = events_evidence


	def to_string(self):
		string = "P("
		for event in self.events_query:
			if event.value == None:
				string += event.node.name.lower() + ","
			elif event.value == 0:
				string += "~" + event.node.name.upper() + ","
			elif event.value == 1:
				string += event.node.name.upper() + ","

		if string[-1] == ",":
			string = string[:-1]

		string += "|"

		for event in self.events_evidence:
			if event.value == None:
				string += event.node.name.lower() + ","
			elif event.value == 0:
				string += "~" + event.node.name.upper() + ","
			elif event.value == 1:
				string += event.node.name.upper() + ","

		if string[-1] == ",":
			string = string[:-1]
		elif string[-1] == "|":
			string = string[:-1]

		string += ")"
		return string


	def evaluate(self, bn):
		return 0



def get_cond_prob_from_names(bn, names_qry, names_cond):
	events_query = []
	events_evidence = []

	for name in names_qry:
		value = None
		if name[0] == "~":
			name = name[1]
			value = 0
		else:
			name = name
			value = 1
		event = Event(bn.nodes_by_name[name], value)
		events_query.append(event)
	
	for name in names_cond:
		value = None
		if name[0] == "~":
			name = name[1]
			value = 0
		else:
			name = name
			value = 1
		event = Event(bn.nodes_by_name[name], value)
		events_evidence.append(event)

	cp = ConditionalProbability(events_query, events_evidence)
	return cp