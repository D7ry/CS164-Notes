#script I wrote to do my hw
epsilon = "ε"
class Grammar:

	def __init__(self, name : str, non_terminals : set, terminals : set, start : str = "S"):
		self.productions = dict() # str -> list(list(str))
		for nt in non_terminals:
			self.productions[nt] = [] # make a new list for each NT to store productions
		self.terminals = terminals
		for term in self.terminals:
			if term in self.productions:
				raise Exception("Terminal {} is also a non-terminal.".format(term))
		#non-terminals is self.productions.keys()
		self.name = name
		self.start = start
		if start not in non_terminals:
			raise Exception("Start symbol {} not in non-terminals.".format(start))
		print("Initializing grammar {}.".format(name))
		print("Non-terminals: ", self.productions.keys())
		print("Terminals: ", terminals)
		self.left_recursion_removed = False
	
	def non_terminals(self):
		return self.productions.keys()

	def is_non_terminal(self, symbol:str):
		return symbol in self.productions.keys()

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
		firsts = dict() #dict<str,set>
		follows = dict() #dict<str,set>
		
		#return a copy of firsts[symbol] if symbol is in firsts, otherwise return an empty set
		def first(symbol) -> set[str]: 
			if symbol in self.terminals:
				return symbol
			return firsts[symbol].copy() if symbol in firsts else set()

		#return a copy of follows[symbol] if symbol is in follows, otherwise return an empty set
		def follow(symbol) -> set[str]:
			return follows[symbol].copy() if symbol in follows else set()

		def calc_first(lhs:str):
			firsts[lhs] = set()
			rhss = self.productions[lhs]
			for rhs in rhss:
				if rhs[0] == epsilon: #assuming if epsilon is the first element, then it is the only element
					firsts[lhs].add(epsilon)
				elif rhs[0] in self.terminals:
					firsts[lhs].add(rhs[0])
				else: #loop through all symbols in rhs
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
							calc_first(elem) if elem not in firsts else None #get first of elem if not already calculated
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
			calc_first(lhs)
		print("Firsts:")
		print(firsts)
		print()

		# follows
		follows[self.start] = {"$"} #start symbol
		links = dict() # symbol -> set of symbols to which the symbol contributes its follow to
		def link(src, dst):
			if dst == src: #don't link to itself
				return
			if src in links:
				links[src].add(dst)
			else:
				links[src] = {dst}
		for lhs, rhss in self.productions.items():
			for rhs in rhss: # rhs = [symbol_1, symbol_2, symbol_3, ...]
				i = len(rhs) - 1
				while i >= 0: # go from right to left
					if self.is_non_terminal(rhs[i]): #terminals don't have follow
						Yi = rhs[i]
						if Yi not in follows:
							follows[Yi] = set()
						if i == len(rhs) - 1: #last element, link follow of lhs to follow of symbol_i
							link(lhs, Yi)
						else: #not last element
							first_Yi_plus_1 = first(rhs[i+1])
							if epsilon in first_Yi_plus_1: #if epsilon in first(Yi+1), then link follow of follow(Yi+1) to follow of follow(Yi)(transitive property)
								link(rhs[i+1], Yi)
								first_Yi_plus_1.remove(epsilon)
							follows[Yi].update(first_Yi_plus_1) #follow(Yi) += first(Yi+1)
					i -= 1
						
		#loop through links
		def update_link(src):
			for dst in links[src]:
				print("Linking follow({}) to follow({})".format(src, dst))
				follows[dst].update(follow(src))
				if dst in links:
					print("follow({}) updated, updating links...".format(dst))
					update_link(dst) #recursively update links
					print("back to linking follow({})".format(src))

		for src in links.keys():
				update_link(src)
		print("Follows:")
		print(follows)
			
				
		
		
		

q1a = Grammar("q1a", {"S", "B", "C"}, {"a", "x", "c"})

q1a.add_production("S", [["S", "a"], ["B"]])
q1a.add_production("B", [["B", "x", "C"], ["C"]])
q1a.add_production("C", [["c"], [epsilon]])

q1a.print()
q1a.remove_left_recursion()
q1a.print(True)
q1a.get_ll1()