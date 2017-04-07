from pddl.pddl_world import *


class CausalLink:
    '''This class represents a causal link between two action steps.'''
    PClink, TPlink, TClink, Startlink = range(4)

    def __init__(self, producer_step, consumer_step, reason_predicate, causal_link_type = PClink):
        self.producer_step = producer_step
        self.consumer_step = consumer_step
        self.reason_predicate = reason_predicate
        self.link_type = causal_link_type

    def __repr__(self):
        return "Causal Link: " + self.__str__()

    def __str__(self):
        out = "%s ---(%s)---> %s" % (self.producer_step.get_grounded_action_description(), self.reason_predicate if self.reason_predicate else "", self.consumer_step.get_grounded_action_description())
        return out


class PartialOrderPlan:
    '''This class represents a Partial Order Plan'''

    def __init__(self, action_steps, causal_links, iniState, endState):
        self.action_steps = action_steps
        self.causal_links = causal_links
        self.iniState = iniState
        self.endState = endState
        self.nodes = set()


    def add_causal_link(self, producer_step, consumer_step, reason_predicate, causal_link_type = CausalLink.PClink):
        # TODO: Save causal links in a dictionary.
        self.causal_links.append(CausalLink(producer_step, consumer_step, reason_predicate, causal_link_type))
        self.nodes.add(producer_step)
        self.nodes.add(consumer_step)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        out = "Partial Order Plan: \n"
        out += "Initial " + str(self.iniState)
        out += "Goal " + str(self.endState)
        out += "\nCausal Links: \n"
        out += "\n".join(["   Causal Link %i: (%s)" %(i, str(causal_link)) for i, causal_link in enumerate(self.causal_links)])
        return out