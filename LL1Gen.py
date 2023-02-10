#script I wrote to do my hw
epsilon = "ε"
class Grammar:

	def __init__(self, name : str, non_terminals : set, terminals : set):
		self.productions = dict() # none_terminal -> productions
		for nt in non_terminals:
			self.productions[nt] = [] # make a new list for each NT to store productions
		self.t = terminals
		self.name = name
		print("Initializing grammar {}.".format(name))
		print("Non-terminals: ", self.productions.keys())
		print("Terminals: ", terminals)

	# epsilon is indicated using "ε" sign
	def add_production(self, lhs:str, rhss:list[list[str]]):
		if lhs not in self.productions:
			raise Exception("Can't find {} among non-terminals.".format(lhs))
		for rhs in rhss:
			self.productions[lhs].append(rhs)

	def remove_left_recursion(self):
		print("Removing left recursion...")
		for lhs, rhs in list(self.productions.items()):
			found = False
			# check for left recursion
			for one_rhs in rhs:
				if one_rhs[0] == lhs:
					found = True
					break
			print("Remove left recursion on {} -> {}".format(lhs, rhs))
			if found: #start removing left recursion
				new_nt = lhs + '\''
				self.productions[new_nt] = []
				new_nt_prod_rhs = [] #list of productions for new non-terminal
				to_replace = [] #list of productions for old non-terminal, to replace the old productions
				for one_rhs in rhs:
					new_rhs = one_rhs.copy()
					new_rhs.append(new_nt)
					if new_rhs[0] == lhs: # add to rhs of the new non-terminal
						new_rhs.pop(0) # remove nt
						new_nt_prod_rhs.append(new_rhs)
					else: # add to rhs of old non-terminal
						to_replace.append(new_rhs)
				new_nt_prod_rhs.append(epsilon)
				self.productions[new_nt] = new_nt_prod_rhs
				self.productions[lhs] = to_replace
		print("...left recursion removed")

	def remove_left_factoring(self):
		
	def print(self, concise=True):
		print("Dumping grammar...")
		print("Productions:")
		
		for nt in self.productions.keys():
			if concise:
				print("{} -> ".format(nt), end='')
				for rhs in self.productions[nt]:
					for elem in rhs:
						print("{}".format(elem), end='')
					print('|',end='')
				print()
			else:
				for rhs in self.productions[nt]:
					print("{} -> {}".format(nt, rhs))
		

q1a = Grammar("q1a", {"S", "B", "C"}, {"a", "x", "c"})

q1a.add_production("S", [["S", "a"], ["B"]])
q1a.add_production("B", [["B", "x", "C"], ["C"]])
q1a.add_production("C", [["c"], [epsilon]])

q1a.print()
q1a.remove_left_recursion()
q1a.print(True)