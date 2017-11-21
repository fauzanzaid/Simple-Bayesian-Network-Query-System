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
