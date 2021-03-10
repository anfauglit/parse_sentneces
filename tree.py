import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

class Node:
	def __init__(self, label=''):
		self.data=str(label)
		self.lchild = None
		self.rchild = None
	def __str__(self):
		return f'{self.data}'
	
def count_nodes(tree, count):
	count = count + 1
	if  tree.lchild == None:
		return count 
	else:
		count = count_nodes(tree.lchild, count)
	if tree.rchild == None:
		return count
	else:
		count = count_nodes(tree.rchild, count)
	return count

def get_subformula(sent):
	if  sent.lchild != None:
		yield from get_subformula(sent.lchild)	
	if  sent.rchild != None:
		yield from get_subformula(sent.rchild)	
			
	yield sent.data

def outer_conn_index(mystring):
	counter = 0
	logical_connectives = '*+-'
	"""
		Logican connectives:
		* -- conjunction (and)
		+ -- disjunction (or)
		- -- negation	(not)
	"""
	for i,c in enumerate(mystring):
		if c == '(':
			counter -= 1
		elif c == ')':
			counter += 1
		elif c in logical_connectives and counter == -1:
			return i

	return -1

def parse(sent):
	node = Node(sent)
	conn_index = outer_conn_index(sent)
	if conn_index > 0:
		if conn_index == 1:
			node.lchild = parse(sent[2:-1])
		else:
			node.lchild = parse(sent[1:conn_index])
			node.rchild = parse(sent[conn_index + 1:-1])

	return node
		
def parse_classic(sent):
	node = Node()
	conn_index = outer_conn_index(sent)
	if conn_index > 0:
		node.data = sent[conn_index]
		if conn_index == 1:
			node.lchild = parse_classic(sent[conn_index + 1:-1])
		else:
			node.lchild = parse_classic(sent[1:conn_index])
			node.rchild = parse_classic(sent[conn_index + 1:-1])
	else:
		node.data = sent

	return node
	
def tree_to_list(tree, tree_list):
	if  tree.lchild != None:
		tree_list.append((tree.data, tree.lchild.data))
		tree_to_list(tree.lchild, tree_list)
	if  tree.rchild != None:
		tree_list.append((tree.data, tree.rchild.data))
		tree_to_list(tree.rchild, tree_list)
	
def get_tree_nodes(tree, tree_nodes):
	tree_nodes.append(tree.data)
	if  tree.lchild != None:
		get_tree_nodes(tree.lchild, tree_nodes)
	if  tree.rchild != None:
		get_tree_nodes(tree.rchild, tree_nodes)

test_sents = ['(p*q)', '(-(p+q))', '((-p)+(p*q))']
root = parse_classic(test_sents[2])

for node in list(get_subformula(root)):
	print(node)
	
tree_list = []
tree_to_list(root, tree_list)
print(tree_list)
tree_nodes = []
get_tree_nodes(root, tree_nodes)
print(tree_nodes)

G = nx.Graph()
G.add_nodes_from(tree_nodes)
G.add_edges_from(tree_list)
pos = graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=True)
plt.show()
