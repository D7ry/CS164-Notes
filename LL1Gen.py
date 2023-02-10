#script I wrote to do my hw
epsilon = "ε"
class Grammar:

	def __init__(self, name : str, non_terminals : set, terminals : set):
		self.productions = dict() # str -> list(list(str))
		for nt in non_terminals:
			self.productions[nt] = [] # make a new list for each NT to store productions
		self.terminals = terminals
		#non-terminals is self.productions.keys()
		self.name = name
		print("Initializing grammar {}.".format(name))
		print("Non-terminals: ", self.productions.keys())
		print("Terminals: ", terminals)
		self.left_recursion_removed = False

	# epsilon is indicated using "ε" sign
	def add_production(self, lhs:str, rhss:list[list[str]]):
		if lhs not in self.productions:
			raise Exception("Can't find {} among non-terminals.".format(lhs))
		for rhs in rhss:
			self.productions[lhs].append(rhs)

	def __replace_production(self, lhs:str, rhss:list[list[str]]):
		if lhs not in self.productions:
			raise Exception("Can't find {} among non-terminals.".format(lhs))
		for rhs in rhss:
			self.productions[lhs] = rhss

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
				# create new non-terminal
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
				self.add_production(new_nt, new_nt_prod_rhs)
				self.__replace_production(lhs, to_replace)
		print("...left recursion removed")
		self.left_recursion_removed = True
	

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
	def remove_ambiguity(self):
		None #tbd
	
	def get_ll1(self):
		if not self.left_recursion_removed:
			raise Exception("Left recursion not removed.")
		firsts = dict()
		follows = dict()

		def get_first(lhs:str):
			firsts[lhs] = set()
			rhss = self.productions[lhs]
			for rhs in rhss:
				if rhs[0] == epsilon: #assuming if epsilon is the first element, then it is the only element
					firsts[lhs].add(epsilon)
				elif rhs[0] in self.terminals:
					firsts[lhs].add(rhs[0])
				else: #non-terminal loop
					toTheEnd = True
					#loop through all elements in rhs, stop at first terminal, keep going if epsilon
					#appears in first(Yi), add epsilon in all elenents in rhs have epsilon.
					for elem in rhs: 
						if elem in self.terminals: #stop at first terminal
							firsts[lhs].add(elem)
							toTheEnd = False
							break
						elif elem == epsilon:
							firsts[lhs].add(epsilon)
						else:# elem is y1, y2, y3, etc
							get_first(elem) if elem not in firsts else None #get first of elem if not already calculated
							if epsilon not in firsts[elem]: #if epsilon not in first(Y1), then stop
								firsts[lhs].update(firsts[elem]) #first(X) = first(Y1)
								toTheEnd = False
								break #gg
							firsts_copy = firsts[elem].copy() #must copy because we are modifying the set
							firsts_copy.remove(epsilon) #remove epsilon
							firsts[lhs].update(firsts_copy) #keep going
					if toTheEnd:
						firsts[lhs].add(epsilon)
		# firsts
		for lhs in self.productions.keys():
			get_first(lhs)
		print("Firsts:")
		print(firsts)
			
				
		
		
		

q1a = Grammar("q1a", {"S", "B", "C"}, {"a", "x", "c"})

q1a.add_production("S", [["S", "a"], ["B"]])
q1a.add_production("B", [["B", "x", "C"], ["C"]])
q1a.add_production("C", [["c"], [epsilon]])

q1a.print()
q1a.remove_left_recursion()
q1a.print(True)
q1a.get_ll1()