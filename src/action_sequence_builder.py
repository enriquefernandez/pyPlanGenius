from pddl.pddl_world import *
from pddl import parser

import readline
from third_party.blessings import Terminal


class ActionSequenceBuilder:
    def __init__(self, pddl_domaing, pddl_problem, showgui):

        self.showgui = showgui

        # Parse domain PDDL file
        self.domain = parser.parse_domain_file('../pddl/' + pddl_domaing)

        # Parse problem PDDL file
        self.problem = parser.parse_problem_file('../pddl/' + pddl_problem)

        self.completions = []

        # Tab completion : see https://www.ironalbatross.net/wiki/index.php5?title=Python_Readline_Completions for help
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.complete)

        # Color coding: see https://pypi.python.org/pypi/blessings/ for instructions
        self.term = Terminal()

    def set_completions(self, completions):
        self.completions = completions

    def complete(self, text, state):
        results = [x for x in self.completions if x.startswith(text)] + [None]
        return results[state]

    def build_action_sequence(self):
        # Create an action sequence

        #Set current state to initial state
        currentState = State(self.problem.initial_conditions.predicates)

        #Create a list of states
        stateList = [currentState]


        #Find the goal state
        goalState = State(self.problem.goal_conditions)

        actionSequence = ActionSequence(currentState, goalState)   #I think I'm going to have problems here
        #with currentsate changing each time

        i=1
        while (not currentState.containsState(goalState)):
            #Print the Current State of the world so the user can make an informed decision
            print "Current State:\n {t.green}".format(t=self.term)," ".join([str(x) for x in currentState.predicates]),"\n{t.normal}".format(t=self.term)

            #Get Demonstrated Action from user
            successful = False
            demonstratedAction = ();
            while (successful == False):
                # print (ungrounded) operators from the domain
                validActions = currentState.findValidActions(self.domain.operator_schemas.values(),self.problem.objects)
                print "Please choose {t.red}action{n}{t.normal}".format(n=i, t=self.term),"to perform from the list below:"
                
                actions_dict = {}
                for schema in validActions:
                    print "{t.cyan}".format(t=self.term),schema.action_name,"{t.normal}".format(t=self.term)

                
                    #action_names.append(schema.action_name)
                    actions_dict[schema.action_name] = schema
                self.set_completions(actions_dict.keys())
                userSchema = str(raw_input("{t.yellow}>>{t.normal}".format(t=self.term)))

                if userSchema in actions_dict:
                    successful = True
                    demonstratedAction = actions_dict[userSchema]
                    break
                if successful == False:
                    print "{t.red}ERROR: Action did not match available options{t.normal}".format(t=self.term)

            print "{t.green}You have selected the following action:\n{t.normal}".format(t=self.term), demonstratedAction


            #Get objects from user

            #print "Please select parameters from list below:\n",problem.objects
            parameterList = []
            for parameter in demonstratedAction.parameters:
                successful=False
                while(successful==False):

                    print "Select parameter{t.red}".format(t=self.term),"(",parameter.tag,"-",parameter.paramType,")","{t.normal}".format(t=self.term)," from the list below:"
                    object_names = []
                    for obj in self.problem.objects:
                        if obj.objType == parameter.paramType:
                            print "{t.cyan}".format(t=self.term),obj.name,"{t.normal}".format(t=self.term)
                            object_names.append(obj.name)
                    self.set_completions(object_names)
                    userParameter = str(raw_input("{t.yellow}>>{t.normal}".format(t=self.term)))
                    #Add checks here to make sure user has entered an allowable parameter
                    #Add checks here to make sure user has entered an allowable parameter
                    if userParameter in object_names:
                        parameterList.append(userParameter)
                        successful=True
                    else:
                        print "{t.red}ERROR:{t.normal}".format(t=self.term), "parameter not valid, try again!"

            # Create an action step and add to the action sequence
            actionStep = ActionStep(demonstratedAction, parameterList)
    
            if currentState.isFeasibleActionStep(actionStep):
                actionSequence.add_action_step(actionStep)
                print  "{t.green}Action added to action sequence.\n{t.normal}".format(t=self.term)

                #Compute the next state and add to the state list
                nextState = currentState.computeNextState(actionStep)
                stateList.append(nextState)
                #Next iteration
                currentState = nextState
                i+=1

            else:
                print "{t.red}ERROR: Combination between action and arguments not feasible.".format(t=self.term)
                print "Action NOT added to action sequence.{t.normal}".format(t=self.term)
                print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"


        # Return generated Action and State Sequence
        return actionSequence, stateList
