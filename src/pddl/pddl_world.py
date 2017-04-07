# PDDL classes. Written by Steve Levine.
# Slightly modified by Enrique Fernandez and James Paterson to be used in our 16.412 Final Project.
# paterson@mit.edu
# efernan@mit.edu
# Sunday, May 5, 2013

import copy


"""
Various classes for PDDL stuff.
"""


class Parameter:
    def __init__(self, tag, paramType):
        self.tag = tag
        self.paramType = paramType


class Object:
    def __init__(self, name, objType):
        self.name = name
        self.objType = objType

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Predicate:
    def __init__(self, prop, args):
        self.property = prop.lower()
        self.arguments = [x.lower() for x in args]

    def __str__(self):
        return "(" + self.property + " " + " ".join(self.arguments) + ")"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Predicate):
            if self.property != other.property:
                return False

            for i in range(len(self.arguments)):
                if self.arguments[i] != other.arguments[i]:
                    return False

            # Checks passed!
            return True
        else:
            return False

    def __ne__(self, other):
        return not (self.__eq__(other))


class Action:
    def __init__(self, action, args):
        self.action_name = action
        self.arguments = args

    def __str__(self):
        return "(" + self.action_name + " " + " ".join(self.arguments) + ")"

    def __repr__(self):
        return self.__str__()


class OperatorSchema:
    def __init__(self, action, parameters, preconds, add_effects, del_effects):
        self.action_name = action
        self.parameters = parameters
        self.preconditions = preconds
        self.add_effects = add_effects
        self.del_effects = del_effects

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = "Operator Schema: " + self.action_name + "\n"
        out += "   Parameters: " + " ".join([str(x.tag) + "-" + (x.paramType) for x in self.parameters]) + "\n"
        out += "   Preconds:   " + " ".join([str(x) for x in self.preconditions]) + "\n"
        out += "   Add Eff:    " + " ".join([str(x) for x in self.add_effects]) + "\n"
        out += "   Del Eff:    " + " ".join([str(x) for x in self.del_effects]) + "\n"
        return out

    # Compute a binding from an action. A binding is a dictionary that maps variable names to values
    def compute_binding(self, action):
        if action.action_name != self.action_name:
            raise Exception("Attempted to bind operator to a different action!")
        if len(action.arguments) != len(self.parameters):
            raise Exception("Wrong number of arguments for " + action.action_name + "!")

        # Everything seems to match up, so bind.
        b = {}
        for i in range(len(self.parameters)):
            b[self.parameters[i].tag] = action.arguments[i]

        return b

    # Compute a binding for each condition or effect.
    def compute_grounded_conditions_and_effects(self, b):
        preconditions = []
        add_effects = []
        del_effects = []

        for p in self.preconditions:
            preconditions.append(self.ground_predicate_schema(p, b))

        for p in self.add_effects:
            add_effects.append(self.ground_predicate_schema(p, b))

        for p in self.del_effects:
            del_effects.append(self.ground_predicate_schema(p, b))

        return (preconditions, add_effects, del_effects)

    # Ground a predicate schema, given a binding.
    def ground_predicate_schema(self, pred_schema, b):
        prop = pred_schema.property
        args = []
        for i in range(len(pred_schema.arguments)):
            var = pred_schema.arguments[i]
            if not var in b:
                raise Exception("Error: binding for " + prop + " has no value for variable " + var + "!")
            args.append(b[var])
        return Predicate(prop, args)


class WorldState:
    def __init__(self):
        self.predicates = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = "World State:"
        for p in self.predicates:
            out += "\n     " + str(p)
        return out

    def __contains__(self, item):
        return item in self.predicates


"""
Domain and problem definitions
"""


class DomainPDDL:
    def __init__(self):
        self.operator_schemas = {}
        self.predicate_schemas = {}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = "PDDL Domain\n"
        for opname in self.operator_schemas:
            op = self.operator_schemas[opname]
            out += str(op) + "\n\n"

        out += "Predicate Schemas:\n"
        for predname in self.predicate_schemas:
            p = self.predicate_schemas[predname]
            out += "     " + str(p) + "\n"
        return out


class ProblemPDDL:
    def __init__(self):
        self.objects = []
        self.initial_conditions = None
        self.goal_conditions = []

    def get_object(self, name):
        for obj in self.objects:
            if obj.name == name:
                return obj

        raise Exception("The requested object doesn't exist.")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = "PDDL Problem:\n"
        out += "Objects:\n"
        for o in self.objects:
            out += "     " + str(o) + "\n"
        out += "Initial Conditions: " + str(self.initial_conditions) + "\n"
        out += "Goal Conditions:\n"
        for g in self.goal_conditions:
            out += "     " + str(g) + "\n"
        return out


class ActionStep:
    """Action Step is a grounded action that took place during a demonstration. An action sequence (or demonstration)
    is a list of these."""
    ActionNormal, ActionStart, ActionEnd = range(3)

    def __init__(self, operatorType, arguments, preconditions=None, effects=None):
        self.preconditions = []
        self.add_effects = []
        self.del_effects = []
        self.arguments = []

        if operatorType and arguments:
            # Normal action step
            self.action_type = ActionStep.ActionNormal
            self.operatorType = operatorType
            self.arguments = arguments
            a = Action(operatorType.action_name, arguments)
            binding = operatorType.compute_binding(a)
            self.preconditions, self.add_effects, self.del_effects = operatorType.compute_grounded_conditions_and_effects(
                binding)

        elif preconditions:
            # Preconditions specified. This is probably a final state being converted into an ActionStep
            self.action_type = ActionStep.ActionEnd
            self.preconditions = preconditions

        else:
            # Effects specified. This is probably an initial state being converted into an ActionStep
            # Note that initial steps could be empty
            self.action_type = ActionStep.ActionStart
            self.add_effects = effects
            self.preconditions = []

    def get_grounded_action_description(self):
        if self.action_type == ActionStep.ActionStart:
            return "START"
        elif self.action_type == ActionStep.ActionEnd:
            return "GOAL"
        else:
            return self.operatorType.action_name + " " + " ".join([str(x) for x in self.arguments])

    def get_dotstyled_action_description(self):
        if self.action_type == ActionStep.ActionStart:
            return "<<B>START</B>>"
        elif self.action_type == ActionStep.ActionEnd:
            return "<<B>GOAL</B>>"
        else:
            return "<<B>" + self.operatorType.action_name + "</B>   " + " ".join([str(x) for x in self.arguments]) + ">"

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = "Action Step: (" + self.get_grounded_action_description() + ")\n"
        out += "   Preconds:   " + " ".join([str(x) for x in self.preconditions]) + "\n"
        # out += "   Maint:      " + " ".join([str(x) for x in self.maintenance]) + "\n"
        out += "   Add Eff:    " + " ".join([str(x) for x in self.add_effects]) + "\n"
        out += "   Del Eff:    " + " ".join([str(x) for x in self.del_effects]) + "\n"
        return out


class State:
    """A State represent the list of predicates that hold after any given action step."""

    def __init__(self, predicates):
        self.predicates = predicates

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = "State:\n"
        out += "   Predicates:   " + " ".join([str(x) for x in self.predicates]) + "\n"
        return out

    def computeNextState(self, actionStep):
        '''Computes the next state from this state and an action step.'''

        nextStatePredicates = copy.deepcopy(self.predicates)
        for add_effect in actionStep.add_effects:
            if add_effect not in nextStatePredicates:
                nextStatePredicates.append(add_effect)

        for del_effect in actionStep.del_effects:
            if del_effect in nextStatePredicates:
                nextStatePredicates.remove(del_effect)

        return State(nextStatePredicates)

    def isFeasibleActionStep(self, actionStep):
        '''Checks if an action step is feasible given the current state of the world'''
        feasible = True
        for actionPrecondition in actionStep.preconditions:
            if actionPrecondition not in self.predicates:
                feasible = False
                break
        return feasible


    def findValidActions(self, operator_schemas, objects):
        '''finds valid ungrounded actions, given a current state, that will be 
        consistent if grounded to the right parameters'''
        validActions = []

        #objectDictionary maps object types to instantiated objects
        objectDictionary = {}
        counterDictionary = {}
        for op in operator_schemas:
            for param in op.parameters:
                if param.paramType not in objectDictionary:
                    objectDictionary[param.paramType] = []
                    counterDictionary[param.paramType] = 0

        for key in objectDictionary.keys():
            for obj in objects:
                if obj.objType == key:
                    objectDictionary[key].append(obj.name)

        #ground all actions in every combination and check for validity given current state
        for op in operator_schemas:
            searcher = Searcher()
            if searcher.isOperatorValid(copy.deepcopy(op), copy.deepcopy(self), copy.deepcopy(objectDictionary)):
                validActions.append(op)
        return validActions

    def containsState(self, state):
        '''Checks if one state is a subset of the other'''
        #TODO extend to handle "not" conditions in state
        contains = True
        for predicate in state.predicates:
            if predicate not in self.predicates:
                contains = False
                break
        return contains


class SearchTree:
    def __init__(self):
        self.tree = []


class Searcher:
    '''Finds if ungrounded action is valid based on the current state of the world .'''

    def __init__(self):
        pass

    def isOperatorValid(self, operator, currentState, objectDictionary):
        objectTypes = []
        for param in operator.parameters:
            objectTypes.append(param.paramType)
            #We now have all parameter types in the operator

        searchTree = SearchTree()
        currentNode = SearchNode(objectTypes[0], objectDictionary[objectTypes[0]], ())
        searchTree.tree.append(currentNode)

        for objType in range(1, len(objectTypes)):
            nextNode = SearchNode(objectTypes[objType], objectDictionary[objectTypes[objType]], currentNode)
            currentNode = nextNode
            searchTree.tree.append(currentNode)

        #Ground operator for all combinations of arguments
        search_done = False
        while (search_done == False):
            currentNode.findNextArguments()  #this is acut
            args = []
            for node in searchTree.tree:
                if node.is_search_done == True:
                    search_done = True
                    break
                else:
                    args.append(node.argument)

            #Now form action step and ground
            if args:
                actionStep = ActionStep(operator, args)
                #if any grounding is valid, the operator can be used by the demonstrator
                if currentState.isFeasibleActionStep(actionStep):
                    return True
        return False


class SearchNode:
    def __init__(self, objectType, objects, parent):
        self.objectType = objectType
        self.objects = objects
        self.copy_objects = copy.deepcopy(objects)
        self.parent = parent
        self.is_search_done = False
        self.argument = objects[0]

    def getParent(self):
        return self.parent

    def findNextArguments(self):

        if len(self.objects) == 0:

            if self.parent == ():
            #Search is done here, we need to stop
                self.is_search_done = True
            else:
                self.objects = copy.deepcopy(self.copy_objects)
                self.parent.findNextArguments()
                self.argument = self.objects.pop()
        else:
            self.argument = self.objects.pop()
            #args.append(self.parent.getArguments())
        return self.argument


class ActionSequence:
    """An ActionSequence represents a totally ordered plan, that is, an ordered list of action steps."""

    def __init__(self, iniState, endState):
        self.iniState = iniState
        self.endState = endState
        self.actionStepList = []

    def add_action_step(self, actionStep, currentState=None):
        """
        Adds an action step to the action sequence. If a currentState is specified, the method returns the next computed
        state.
        :param actionStep: The action step that is added to the end of the sequence.
        :param currentState: The current world state before executing the action state
        :return: The next world state, computed from the previous world state and the action step.
        """
        self.actionStepList.append(actionStep)

        if currentState:
            return currentState.computeNextState(actionStep)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = "Action Sequence:\n"
        out += "   Initial Conditions: " + " ".join([str(x) for x in self.iniState.predicates]) + "\n"
        out += "\n".join(["   Step %i: (%s)" % (i, step.get_grounded_action_description()) for i, step in
                          enumerate(self.actionStepList)])
        out += "\n   Goal Conditions: " + " ".join([str(x) for x in self.endState.predicates])
        return out
