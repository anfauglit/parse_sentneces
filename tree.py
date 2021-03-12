import itertools
import json
import numpy as np
class Node:
	def __init__(self, label=''):
		self.data = str(label)
		self.lchild = None
		self.rchild = None
		self.subformula = ''
	def __str__(self):
		return f'{self.data}'
	
class Tree:
	def __init__(self, sent):
		self.fomula = sent
		self.tree = parse_classic(sent)
		self.node_number = count_nodes(self.tree, 0)

	def get_tree_edges(self, tree, tree_list):
		if  tree.lchild != None:
			tree_list.append((tree.data, tree.lchild.data))
			self.get_tree_edges(tree.lchild, tree_list)
		if  tree.rchild != None:
			tree_list.append((tree.data, tree.rchild.data))
			self.get_tree_edges(tree.rchild, tree_list)
		
	def get_tree_nodes(self, tree, tree_nodes):
		tree_nodes.append(tree.data)
		if  tree.lchild != None:
			self.get_tree_nodes(tree.lchild, tree_nodes)
		if  tree.rchild != None:
			self.get_tree_nodes(tree.rchild, tree_nodes)

	def get_subformula(self, sent):
		if  sent.lchild != None:
			yield from self.get_subformula(sent.lchild)	
		if  sent.rchild != None:
			yield from self.get_subformula(sent.rchild)	
				
		yield sent.subformula

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
		node.subformula = sent
		if conn_index == 1:
			node.lchild = parse_classic(sent[conn_index + 1:-1])
		else:
			node.lchild = parse_classic(sent[1:conn_index])
			node.rchild = parse_classic(sent[conn_index + 1:-1])
	else:
		node.data = sent
		node.subformula = sent

	return node

def calc_truth_val(tree, assignment):
	if tree.data == '*':
		return calc_truth_val(tree.lchild, assignment) and \
		calc_truth_val(tree.rchild, assignment)
	elif tree.data == '+':
		return calc_truth_val(tree.lchild, assignment) or \
		calc_truth_val(tree.rchild, assignment)
	elif tree.data == '-':
		return not calc_truth_val(tree.lchild, assignment)
		
	return assignment[tree.data]

def calc_truth_val_dict(tree, assignment, out_dict):
	if tree.data == '*':
		l_value = calc_truth_val_dict(tree.lchild, assignment, out_dict)
		r_value = calc_truth_val_dict(tree.rchild, assignment, out_dict)
		out_dict[tree.subformula] = l_value and r_value 
		return l_value and r_value
	elif tree.data == '+':
		l_value = calc_truth_val_dict(tree.lchild, assignment, out_dict)
		r_value = calc_truth_val_dict(tree.rchild, assignment, out_dict)
		out_dict[tree.subformula] = l_value or r_value 
		return l_value or r_value
	elif tree.data == '-':
		t_value = not calc_truth_val_dict(tree.lchild, assignment, out_dict)
		out_dict[tree.subformula] = t_value
		return t_value
		
	t_value = assignment[tree.data]
	out_dict[tree.subformula] = t_value
	return assignment[tree.data]

def get_json_table(sent):
	t = Tree(sent)
	tree_nodes = []
	t.get_tree_nodes(t.tree, tree_nodes)
	props = list(set([p for p in tree_nodes if \
	p.isalpha()]))
	ass = [dict(zip(props, a)) for a in list(itertools.product([True, False], \
	repeat=len(props)))]
	subs = sorted(list(set(t.get_subformula(t.tree))), key=len)
	r = []
	mydict = {}
	for a in ass:
		mydict.clear()
		calc_truth_val_dict(t.tree, a, mydict)
		r.append(mydict.copy())

	row_values = np.array([res[key] for res in r for key in subs])
	a =	np.reshape(row_values, (len(r), len(subs)))

	truth_table = {}
	truth_table['header'] = subs
	truth_table['body'] = a.tolist()
	json_tt = json.dumps(truth_table)
	
	return json_tt

if __name__ == "__main__":
	test_sents = ['(p*q)', '(-(p+q))', '((-p)+(p*q))']
	ass = [dict(zip('pq', a)) for a in list(itertools.product([True, False], repeat=2))]
	root = parse_classic(test_sents[0])
		
	tree_edges= []
	tree_nodes = []
	
	t = Tree(test_sents[2])
	t.get_tree_nodes(t.tree, tree_nodes)
	t.get_tree_edges(t.tree, tree_edges)
	
	subs = sorted(list(set(t.get_subformula(t.tree))), key=len)
	for sub in subs:
		print(f'{sub:^10}', end='')
	print('\n')
	r = []
	mydict = {}
	for a in ass:
		mydict.clear()
		calc_truth_val_dict(t.tree, a, mydict)
		r.append(mydict.copy())

	for res in r:
		for key in subs: 
			print(f'{str(res[key]):^10}', end='')
		print('\n')

	row_values = np.array([res[key] for res in r for key in subs])
	a =	np.reshape(row_values, (len(r), len(subs)))

	truth_table = {}
	truth_table['header'] = subs
	truth_table['body'] = a.tolist()
	json_tt = json.dumps(truth_table)
	print(get_json_table(test_sents[2]))
"""
	G = nx.Graph()
	G.add_nodes_from(tree_nodes)
	G.add_edges_from(tree_list)
	pos = graphviz_layout(G, prog='dot')
	nx.draw(G, pos, with_labels=True)
	plt.show()
"""
