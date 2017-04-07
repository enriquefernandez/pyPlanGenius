# Python PDDL parser written by Steve Levine
# Used in our Final Project for 16.412 by James Paterson and Enrique Fernandez
# paterson@mit.edu
# efernan@mit.edu
# Sunday, May 5, 2013

from pddl_world import *
import string
"""
Functions relating to lexically parsing parenthetical expressions.
"""

"""
Lexically parse a string. Namely, divide into:
	"(", ")", and words.
Don't care too much about performance...
"""
def lexical_parse(expr, special_tokens="()", whitespace=" \t\r\n"):
	expr = expr + " "	# Process an edge case.
	tokens = []
	word_current = ""
	for i in range(len(expr)):
		s = expr[i]
		if s in special_tokens or s in whitespace:
			if word_current != "":
				tokens.append(word_current)
				word_current = ""
			if s in special_tokens:
				tokens.append(s)
		else:
			# Part of a character - build up the word.
			word_current += s

	return tokens


"""
Syntactically parse a liste of tokens. Namely, returns a list of ParenExpressions which are
each recursively filled in.
"""
def syntactic_parse(tokens):
	paren_expressions = []
	while len(tokens) > 0:
			token = tokens.pop(0)
			if token == ")":
				return paren_expressions
			elif token == "(":
				p = syntactic_parse(tokens)
				paren_expressions.append(p)
			else:
				paren_expressions.append(token.lower())
	
	return paren_expressions
	




"""
Functions related to lexical and syntactic parsing.
"""
def pget(p, tag):
	if tag in p:
		i = p.index(tag)
		if len(p) > i + 1:
			return p[i + 1]
		else:
			return None
	else:
		return None


"""
Semantically parse a predicate
"""
def process_predicate(p):
	if p[0] == "not":
		pred = process_positive_predicate(p[1])
		return (pred, False)
	else:
		pred = process_positive_predicate(p)
		return (pred, True)
		

def process_positive_predicate(p):
	for o in p:
		if isinstance(o, list):
			print "Error: Malformed predicate!"
			return Predicate("!!!", [])

	pname = p[0]
	args = []
	for arg in p[1:]:
		args.append(arg)

	return Predicate(pname, args)


"""
Semantically parse a conjunction of temporally annotated conditions or effects.
"""
def process_preconditions(p):
	preconds = []

	if p[0] != "and":
		print "Error! Must be a conjunction or predicates."
	else:
		for psub in p[1:]:
			pred = process_predicate(psub)
			preconds.append(pred)
			
	return preconds

def process_effects(p):
	effects = []
	
	if p[0] != "and":
		print "Error! Must be a conjunction or predicates."
	else:
		for psub in p[1:]:
			pred = process_predicate(psub)
			effects.append(pred)
	
	return effects

def process_parameters(p):
	for o in p:
		if isinstance(o, list):
			print "Error: Malformed parameter list!"
			return []
	params = []
	for param in p:
		if "?" in param:
			tag = param
			paramType = ()

			idx = p.index(tag)
			if ("-" in p):
				while (p[idx] != "-"):
					idx = idx+1
				paramType = p[idx+1].lower()

			parameter = Parameter(tag,paramType)

			params.append(parameter)
	return params

def process_operator_schema(p):
	if p[0] != ":action":
		print "Error: Not a non-timed action!"
	action_name = p[1]

	params = pget(p, ":parameters")
	#dur = pget(p, ":duration")
	conds = pget(p, ":precondition")
	eff = pget(p, ":effect")

	if params == None or conds == None or eff == None:
		print "Error! Operator schema doesn't have everything."
		return None

	parameters = process_parameters(params)
	#duration = process_duration(dur)
	conditions = process_preconditions(conds)
	effs = process_effects(eff)


	preconditions = []
	for c in conditions:
		(pred, pos) = c
		if not pos:
			print "Warning: Negative preconditions are not allowed!"
			return None
		else:
			preconditions.append(pred)

	add_effects = []
	del_effects = []
	for e in effs:
		(pred, pos) = e
		if pos:
			add_effects.append(pred)
		else:
			del_effects.append(pred)

	op = OperatorSchema(action_name, parameters, preconditions, add_effects, del_effects)
	return op
	

"""
Return a list of predicate schemas (basically just predicates but have variables).
"""
def process_predicate_schemas(p):
	preds = []
	if p[0] != ":predicates":
		print "Error: Not a sequence of predicates!"
		return []
	for exp in p[1:]:
		if not isinstance(exp, list):
			print "Error: Malformed predicate schema!"
			return []
		prop_name = exp[0]
		variables = [x for x in exp[1:] if "?" in x]
		preds.append(Predicate(prop_name, variables))
	return preds

def process_domain(p):
	domain = DomainPDDL()
	if not isinstance(p, list):
		print "Error: Invalid domain file!"
		return domain
	if p[0][0] != "define":
		print "Error: Invalid domain file!"
		return domain
	if p[0][1][0] != "domain":
		print "Error: Not a domain file!"
		return domain
	for e in p[0][1:]:
		if e[0] == ":predicates":
			# Defining a set of predicate schema
			preds = process_predicate_schemas(e)
			for pred in preds:
				domain.predicate_schemas[pred.property] = pred

		elif e[0] == ":action":
			# Defining an action
			op = process_operator_schema(e)
			domain.operator_schemas[op.action_name] = op

	return domain
	
def process_objects(p):
	if p[0] != ":objects":
		print "Error: Not an objects list!"
		return []
	# Assume typing! Makes things easier...
	i = 1
	objs = []
	while i < len(p):
		name = p[i];
		objType = p[i+2].lower()


		obj = Object(name,objType)
		objs.append(obj)
		i += 3
	return objs

def process_initial_conditions(p):
	if p[0] != ":init":
		print "Error: Not an initial conditions list!"
		return None
	inits = []
	for init in p[1:]:
		(pred, pos) = process_predicate(init)
		if pos:
			inits.append(pred)
		else:
			print "Error: Initial conditions must also be positive!"
			return []
	W_0 = WorldState()
	W_0.predicates = inits
	return W_0

def process_goal_conditions(p):
	goals = []
	if p[0] != ":goal":
		print "Error: Not a goal specification!"
		return []
	if not isinstance(p[1], list):
		print "Error: Goal must be a conjunction of predicates!"
		return []
	if p[1][0] != "and":
		print "Error: Goal must be a conjunction of predicates!"
		return []
	for g in p[1][1:]:
		(pred, pos) = process_predicate(g)
		if pos:
			goals.append(pred)
		else:
			print "Error: Goals must be positive!"
			return []

	return goals

def process_problem(p):
	problem = ProblemPDDL()
	if not isinstance(p, list):
		print "Error: Invalid problem file!"
		return domain
	if p[0][0] != "define":
		print "Error: Invalid problem file!"
		return domain
	if p[0][1][0] != "problem":
		print "Error: Not a problem file!"
		return domain

	for e in p[0][1:]:
		if e[0] == ":objects":
			# Define the objects in the world.
			objs = process_objects(e)
			problem.objects = objs

		if e[0] == ":init":
			# Defining the initial conditions
			W_0 = process_initial_conditions(e)
			problem.initial_conditions = W_0

		elif e[0] == ":goal":
			# Defining goal conditions
			goals = process_goal_conditions(e)
			problem.goal_conditions = goals

	return problem


def parse_dispatch_activity(cmd):
	tokens = lexical_parse(cmd, special_tokens="()[],", whitespace=" \t\r\n\"")
	exp = syntactic_parse(tokens)
	if len(exp) < 7:
		print "Error parsing dispatch command; not enough stuff."
		return None
	if  exp[1] != "[" or exp[3] != "," or exp[5] != "]" or not(isinstance(exp[6], list)):
		print "Error parsing dispatch command; invalid syntax!"
		return None

	cid = int(exp[0])
	lb = float(exp[2])
	ub = float(exp[4])
	
	action_name = exp[6][0]
	args = exp[6][1:]
	action = Action(action_name, args)
	return (cid, lb, ub, action)
	

def parse_domain_file(filename):
	with open(filename, "r") as f:
		domain_text = f.read()	
	tokens = lexical_parse(domain_text)
	exp = syntactic_parse(tokens)
	domain = process_domain(exp)
	return domain

def parse_problem_file(filename):
	with open(filename, "r") as f:
		problem_text = f.read()	
	tokens = lexical_parse(problem_text)
	exp = syntactic_parse(tokens)
	problem = process_problem(exp)
	return problem


if __name__ == '__main__':
	domain_file = "/home/steve/MERS/SVN/Mars toolkit/Exec-Monitor/tests/boeing_demo_temporal/boeing-domain-temporal.pddl"
	problem_file = "/home/steve/MERS/SVN/Mars toolkit/Exec-Monitor/tests/boeing_demo_temporal/boeing-problem.pddl"

	domain = parse_domain_file(domain_file)
	problem = parse_problem_file(problem_file)
	print domain
	print problem

