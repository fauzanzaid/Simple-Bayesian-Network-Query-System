#! /usr/bin/python2

import re
from operator import mul

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

		for n in self.nodes:
			cpt_list = n.cpt_list
			for i,cp in enumerate(cpt_list):
				binary = format(i, "0"+str(len(n.parents))+"b")
				event_values = [int(v) for v in list(binary)]

				events_query_0 = [Event(n,0)]
				events_query_1 = [Event(n,1)]
				events_evidence = []
				for j,p in enumerate(n.parents):
					events_evidence.append(Event(p,event_values[j]))
				prob_0 = Probability(events_query_0, events_evidence)
				prob_1 = Probability(events_query_1, events_evidence)

				n.cpt[prob_0] = 1-float(cp)
				n.cpt[prob_1] = float(cp)


class BayesianNetworkNode(object):
	"""docstring for BayesianNetworkNode"""
	def __init__(self, name):
		self.name = name
		self.parents = []
		self.children = []
		self.cpt_list = None
		self.cpt = {}


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


	def get_all_parents(self):
		all_parents = set(self.parents)
		for n in iter(all_parents):
			all_parents = all_parents | n.get_all_parents()
		return all_parents


	def __hash__(self):
		return hash((self.name))

	def __eq__(self, other):
		return (self.name) == (other.name)

	def __ne__(self, other):
		return not(self==other)



class Event(object):
	"""docstring for Event"""
	def __init__(self, node, value=None):
		self.node = node
		self.value = value


	def __hash__(self):
		return hash((self.node, self.value))

	def __eq__(self, other):
		return (self.node, self.value) == (other.node, other.value)

	def __ne__(self, other):
		return not(self==other)


class Probability(object):
	"""docstring for Probability"""
	def __init__(self, events_query, events_evidence=[]):
		self.events_query = frozenset(events_query)
		self.events_evidence = frozenset(events_evidence)
		self.events_query_by_node = {}
		self.events_evidence_by_node = {}

		for event in self.events_query:
			self.events_query_by_node[event.node] = event
		for event in self.events_evidence:
			self.events_evidence_by_node[event.node] = event


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

		nodes_common = [n for n in self.events_query_by_node if n in self.events_evidence_by_node]
		for n in nodes_common:
			if self.events_query_by_node[n].value != self.events_evidence_by_node[n].value:
				return 0

		if len(self.events_query) == 0:
			# Null event
			return 0
		
		if len(self.events_query) == 1:
			event = next(iter(self.events_query))	# Get the only set element
			if self in event.node.cpt:
				# Value exists in CPT
				return event.node.cpt[self]
		
		if len(self.events_evidence) == 0:
			# Chain rule and Marginalization
			
			# Find all affecting nodes
			nodes_all = set()
			for event in self.events_query:
				nodes_all |= {event.node}
				nodes_all |= event.node.get_all_parents()

			events_by_node = {}
			for node in nodes_all:
				if node in self.events_query_by_node:
					events_by_node[node] = self.events_query_by_node[node]
				else:
					events_by_node[node] = Event(node, None)

			chain_uninst = []
			for node in nodes_all:
				events_query = [events_by_node[node]]
				events_evidence = []
				for p in node.parents:
					events_evidence.append(events_by_node[p])
				chain_uninst.append(Probability(events_query, events_evidence))

			uninst_nodes = self.get_uninst_nodes_from_chain(chain_uninst)

			chains_inst = []
			for i in xrange(2**(len(uninst_nodes))):
				binary = format(i, "0"+str(len(uninst_nodes))+"b")
				event_values = [int(v) for v in list(binary)]
				chains_inst.append(self.get_chain_inst_from_node_values(chain_uninst, dict(zip(uninst_nodes, event_values))))

			products = []
			for chain in chains_inst:
				products.append(reduce(mul, [prob.evaluate(bn) for prob in chain], 1))

			return sum(products)


		else:
			# Product rule
			events_query_num = self.events_query | self.events_evidence
			events_query_den = self.events_evidence
			val_num = Probability(events_query_num).evaluate(bn)
			val_den = Probability(events_query_den).evaluate(bn)
			return val_num/float(val_den)


	def get_uninst_nodes_from_chain(self, chain):
		uninst_nodes = set()
		for prob in chain:
			for event in prob.events_query | prob.events_evidence:
				if event.value == None:
					uninst_nodes |= {event.node}
		return uninst_nodes


	def get_chain_inst_from_node_values(self, chain_uninst, values_by_node):
		chain_inst = []
		for prob_uninst in chain_uninst:
			
			events_query_inst = []
			for event in prob_uninst.events_query:
				if event.value == None:
					# Event uninstantiated
					events_query_inst.append(Event(event.node, values_by_node[event.node]))
				else:
					# Event already instantiated
					events_query_inst.append(event)
			
			events_evidence_inst = []
			for event in prob_uninst.events_evidence:
				if event.value == None:
					# Event uninstantiated
					events_evidence_inst.append(Event(event.node, values_by_node[event.node]))
				else:
					# Event already instantiated
					events_evidence_inst.append(event)

			prob_inst = Probability(events_query_inst, events_evidence_inst)
			chain_inst.append(prob_inst)

		return chain_inst


	def __hash__(self):
		return hash((self.events_query, self.events_evidence))

	def __eq__(self, other):
		return (self.events_query, self.events_evidence) == (other.events_query, other.events_evidence)

	def __ne__(self, other):
		return not(self==other)



def get_prob_from_names(bn, names_qry, names_cond):
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

	p = Probability(events_query, events_evidence)
	return p
