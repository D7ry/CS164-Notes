# all epsilon edges left. epsilon edges are counted as edge obj initialize with cond = None.
epsilon_edges = []

class e: #edge
	def __init__(self, src, dest, cond = None): #cond = none for epsilon moves only
		self.src = src
		self.dest = dest
		self.cond = cond
		if self.cond == None:
			epsilon_edges.append(self)

class v: #vertex, edges are only outgoing
	def __init__(self, name, edges, is_start = False, is_final = False):
		self.name = name
		self.edges = edges
		self.is_start = is_start
		self.is_final = is_final


vertices = {}
vertices['A'] = v('A', [e('A', 'K'), e('A', 'B')], is_start=True)
vertices['B'] = v('B', [e('B', 'C'), e('B', 'J')])
vertices['C'] = v('C', [e('C', 'E'), e('C', 'H')])
vertices['D'] = v('D', [e('D', 'B')])
vertices['E'] = v('E', [e('E', 'F', 'a')])
vertices['F'] = v('F', [e('F', 'G', 'b')])
vertices['G'] = v('G', [e('G', 'D', 'a')])
vertices['H'] = v('H', [e('H', 'I', 'b')])
vertices['I'] = v('I', [e('I', 'D', 'b')])
vertices['J'] = v('J', [e('J', 'Z')])
vertices['K'] = v('K', [e('K', 'N'), e('K', 'O')])
vertices['L'] = v('L', [e('L', 'M', 'b')])
vertices['M'] = v('M', [e('M', 'K')])
vertices['N'] = v('N', [e('N', 'L', 'a')])
vertices['O'] = v('O', [e('O', 'Z')])
vertices['Z'] = v('Z', [], is_final=True)

print("proceeding to remove epsilon edges...")
while epsilon_edges != []:
	epe = epsilon_edges.pop(0)
	print("processing epsilon edge: " + epe.src + " -> " + epe.dest)
	v1 = vertices[epe.src]
	v2 = vertices[epe.dest]
	if v1 == v2:
		continue
	for v2e in v2.edges:
		v1.edges.append(e(v1.name, v2e.dest, v2e.cond))
		print("added edge: {} -> {} on {}".format(v1.name, v2e.dest, v2e.cond))
	v1.edges.remove(epe)
	print("removed edge: " + epe.src + " -> " + epe.dest)
	if v1.is_start:
		v2.is_start = True
		print("vertex {} is now start".format(v2.name))
	if v2.is_final:
		v1.is_final = True
		print("vertex {} is now final".format(v1.name))

print("done removing epsilon edges")
