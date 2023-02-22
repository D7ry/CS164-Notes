import pandas as pd
#script I wrote to do my hw
EPSL = "ε" #epsilon
class Grammar:

	def __init__(self, name : str, non_terminals : set, terminals : set, start : str = "S"):
		self.productions = dict() # str -> list(list(str))
		for nt in non_terminals:
			self.productions[nt] = [] # make a new list for each NT to store productions
		self.terminals = terminals
		self.terminals.add(EPSL) #add epsilon to terminals automatically
		self.terminals.add('$') #add end of input to terminals automatically
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
			for symbol in rhs:
				if symbol not in self.terminals and not self.is_non_terminal(symbol):
					raise Exception("Can't find {} among terminals or non-terminals.".format(symbol))
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
			if found: #start removing left recursion
				print("Remove left recursion on {} -> {}".format(lhs, rhs))
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
				new_nt_prod_rhs.append(EPSL)
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

		print("Terminals: ", self.terminals)
		print("Non-terminals: ", self.productions.keys())
		print("Start symbol: ", self.start)

	def remove_ambiguity(self):
		None #tbd

	def left_factored(self):
		for lhs, rhss in self.productions.items():
			left = set()
			for rhs in rhss:
				if rhs[0] in left:
					return False
				left.add(rhs[0])
		return True

	# print and return the firsts and follows
	def get_firsts_and_follows(self) -> tuple[dict, dict]:
		firsts = dict() #dict<str,set>
		follows = dict() #dict<str,set>
		
		#return a copy of firsts[symbol] if symbol is in firsts, otherwise return an empty set
		def first(symbol) -> set[str]: 
			if symbol in self.terminals:
				ret = set()
				ret.add(symbol)
				return ret
			return firsts[symbol].copy() if symbol in firsts else set()

		#return a copy of follows[symbol] if symbol is in follows, otherwise return an empty set
		def follow(symbol) -> set[str]:
			return follows[symbol].copy() if symbol in follows else set()

		def calc_first(lhs:str):
			firsts[lhs] = set()
			rhss = self.productions[lhs]
			for rhs in rhss:
				if rhs[0] == EPSL: #assuming if epsilon is the first element, then it is the only element
					firsts[lhs].add(EPSL)
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
						elif elem == EPSL:
							firsts[lhs].add(EPSL)
						else:# elem is y1, y2, y3, etc
							calc_first(elem) if elem not in firsts else None #get first of elem if not already calculated
							if EPSL not in firsts[elem]: #if epsilon not in first(Y1), then stop
								firsts[lhs].update(firsts[elem]) #first(X) = first(Y1)
								toTheEnd = False
								break #gg
							firsts_copy = firsts[elem].copy() #must copy because we are modifying the set
							firsts_copy.remove(EPSL) #remove epsilon
							firsts[lhs].update(firsts_copy) #keep going
					if toTheEnd:
						firsts[lhs].add(EPSL)

		# firsts
		for lhs in self.productions.keys():
			calc_first(lhs)

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
							if EPSL in first_Yi_plus_1: #if epsilon in first(Yi+1), then link follow of follow(Yi+1) to follow of follow(Yi)(transitive property)
								link(rhs[i+1], Yi)
								first_Yi_plus_1.remove(EPSL)
							follows[Yi].update(first_Yi_plus_1) #follow(Yi) += first(Yi+1)
					i -= 1
						
		#put follow(src) into follow(dst) for all dst in links[src]
		def update_link(src, reason = None):
			for dst in links[src]:
				if dst != reason:
					#print("Linking follow({}) to follow({})".format(src, dst))
					follows[dst].update(follow(src))
					if dst in links: 
						#print("follow({}) updated, updating links...".format(dst))
						update_link(dst, src) #recursively update links
						#print("back to linking follow({})".format(src))
				else:
					None
					#print("Linking follow({}) to follow({}) skipped because of recursion".format(src, dst))
		for src in links.keys():
			update_link(src)

		#print out firsts and follows in a table
		print("Firsts and Follows:")
		print("Symbol\tFirst\tFollow")
		non_terms = list(self.non_terminals())
		non_terms.sort()
		for symbol in non_terms:
			print("{}\t{}\t{}".format(symbol, firsts[symbol], follows[symbol]))
		print()

		return firsts, follows

	def get_ll1(self):
		print("Generating LL1 table...")
		if not self.left_recursion_removed:
			raise Exception("Left recursion not removed.")
		if not self.left_factored():
			raise Exception("Left factoring not done.")
		#return a copy of firsts[symbol] if symbol is in firsts, otherwise return an empty set
		firsts, follows = self.get_firsts_and_follows()
		def first(symbol) -> set[str]: 
			if symbol in self.terminals:
				ret = set()
				ret.add(symbol)
				return ret
			return firsts[symbol].copy() if symbol in firsts else set()

		#return a copy of follows[symbol] if symbol is in follows, otherwise return an empty set
		def follow(symbol) -> set[str]:
			return follows[symbol].copy() if symbol in follows else set()

		# generate ll1 table
		ll1_table = dict()
		def ll1_table_add_entry(row, col, rhs:list[str]):
			print("Adding entry {} -> {} on {} to ll1_table".format(row, "".join(rhs), col))
			if row not in self.non_terminals():
				raise Exception("Row {} is not a non-terminal".format(row))
			if col not in self.terminals:
				raise Exception("Column {} is not a terminal".format(col))
			r = "".join(rhs)
			s = row + " -> " + r
			if row in ll1_table:
				ll1_table[row][col] = s
			else:
				ll1_table[row] = dict()
				ll1_table[row][col] = s


		for capA, rhss in self.productions.items():
			print("Processing {} -> ...".format(capA))
			for rhs in rhss:
				print("-> {}".format("".join(rhs)))
				#for each production A -> alpha
				alpha = rhs[0]
				rule2 = False
				#1. Find First(α) and for each terminal in First(α), make entry A –> α in the table.
				print("first({}) = {}".format(alpha, first(alpha)))
				for terminal in first(alpha):
					if terminal == EPSL:
						rule2 = True
						continue
					ll1_table_add_entry(capA, terminal, rhs) #rule 1: add all terminals in first(alpha) to ll1_table
				#2. If First(α) contains ε (epsilon) as terminal, 
				# then find the Follow(A) and for each terminal in Follow(A), make entry A –>  ε in the table.
				if rule2:
					for terminal in follow(capA):
						ll1_table_add_entry(capA, terminal, [EPSL])

		return ll1_table




					

def print_ll1(ll1_table):
	print("LL1 Table:")
	df = pd.DataFrame(ll1_table).transpose()
	df.sort_index(inplace=True)
	print(df.to_string())
				
# test = Grammar("test", {"E", "E'", "T", "T'", "F"}, {"(", ")", "id", "+", "*",}, "E")	
		
# test.add_production("E", [["T", "E'"]])
# test.add_production("E'", [["+", "T", "E'"], [EPSL]])
# test.add_production("T", [["F", "T'"]])
# test.add_production("T'", [["*", "F", "T'"], [EPSL]])
# test.add_production("F", [["(", "E", ")"], ["id"]])

# test.remove_left_recursion()
# test.print(True)
# ll1_table = test.get_ll1()
# print_ll1(ll1_table)


# q1a = Grammar("q1a", {"S", "B", "C"}, {"a", "x", "c"})

# q1a.add_production("S", [["S", "a"], ["B"]])
# q1a.add_production("B", [["B", "x", "C"], ["C"]])
# q1a.add_production("C", [["c"], [EPSL]])

# q1a.remove_left_recursion()
# q1a.print(True)
# print_ll1(q1a.get_ll1())

#not left factored
# q1b = Grammar("q1b", {"L"}, {"int", "+", "*", "(", ")"}, "L")
# q1b.add_production("L", [["int"], ["int", "+", "L"], ["int", "*", "L"], ["(", "L", ")"]])
# q1b.remove_left_recursion()
# print_ll1(q1b.get_ll1())

# q1b = Grammar("q1b", {"L", "L'"}, {"int", "+", "*", "(", ")"}, "L")
# q1b.add_production("L", [["int", "L'"], ["(","L",")"]])
# q1b.add_production("L'", [["+", "L"], ["*", "L"], [EPSL]])
# q1b.remove_left_recursion()
# q1b.print()
# print_ll1(q1b.get_ll1())

# q1c = Grammar("q1c", {"A", "A'"}, {"bool", "or", "and"}, "A")
# q1c.add_production("A", [["bool", "A'"], ["and", "bool"]])
# q1c.add_production("A'", [["or", "bool"], [EPSL]])
# q1c.print()
# q1c.remove_left_recursion()
# print_ll1(q1c.get_ll1())

# q2 = Grammar("Q2", {"A", "B", "C"}, {"*", "(", ")", "int", "+"}, "A")
# q2.add_production("A", [["A", "*", "B"], ["C"]])
# q2.add_production("B", [["B", "+", "C"], ["C"]])
# q2.add_production("C", [["(", "B", ")"], ["int"]])
# q2.print()
# q2.remove_left_recursion()
# q2.print()
# print_ll1(q2.get_ll1())

q5 = Grammar("Q5", {"S", "B", "C", "D", "E"}, {"a", "t", "o", "p", "m"}, "S")
q5.add_production("S", [["B", "a", "t"], ["C", "o", "p"]])
q5.add_production("B", [["D"]])
q5.add_production("C", [["E"]])
q5.add_production("D", [["m"]])
q5.add_production("E", [["m"]])
q5.print()
q5.get_firsts_and_follows()