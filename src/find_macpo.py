from partial_order_plan import PartialOrderPlan, CausalLink
from pddl.pddl_world import ActionSequence, ActionStep
import copy


def find_last_producer(precondition, action_steps, i):
    producer = None
    # print "Looking for %s from %d down to 0" %(precondition, i)
    for action_step in reversed(action_steps[:i+1]):
        if precondition in action_step.add_effects:
            producer = action_step
            # print "Found producer: ",action_step
            break

    assert producer, "The plan needs to be valid. All action preconditions need to be satisfied before executing the action"

    return producer


def add_start_causal_links(plan):
    for action_step in plan.action_steps[1:]:
        found = False
        for causal_link in plan.causal_links:
            if causal_link.consumer_step == action_step:
                found = True
                break
        if not found:
            plan.add_causal_link(plan.action_steps[0], action_step, None, CausalLink.Startlink) #TODO: Create a new predicate instead of passing None

def resolve_threats(plan):

    for causal_link in copy.copy(plan.causal_links):
        producer_idx = plan.action_steps.index(causal_link.producer_step)
        consumer_idx = plan.action_steps.index(causal_link.consumer_step)

        # Find all possible threats in action steps that happened before the producer step in the demonstrated sequence.
        for action_step in plan.action_steps[:producer_idx]:
            if causal_link.reason_predicate in action_step.del_effects:
                # An earlier action_step can potentially delete this causal link precondition
                # We solve the threat by enforcing that this action step happens earlier than the producer step
                # (as occurred in the demonstrated sequence)
                plan.add_causal_link(action_step, causal_link.producer_step, causal_link.reason_predicate, CausalLink.TPlink)

        # Find all possible threats in action steps that happened after the consumer step in the demonstrated sequence.
        # If any, enforce that they occur after the consumer step.
        for action_step in plan.action_steps[consumer_idx+1:]:
            if causal_link.reason_predicate in action_step.del_effects:
                # A later action_step can potentially delete this causal link precondition
                # We solve the threat by enforcing that this action step happens after the consumer step
                # (as occurred in the demonstrated sequence)
                plan.add_causal_link(causal_link.consumer_step, action_step, causal_link.reason_predicate, CausalLink.TClink)



    return plan


def find_macpo(action_sequence, state_sequence, resolveThreats = True):
    '''
    This function implements the algorithm that finds a minimal annotated partial orderings plan (MACPO).

    :param state_sequence: Complete state sequence, from the initial State to the state after the last action is executed.
    :type action_sequence: ActionSequence
    :param action_sequence: The action sequence (or total order plan) whose partial order plan we want to find.
    '''

    # assert isinstance(action_sequence, ActionSequence)

    action_steps = copy.copy(action_sequence.actionStepList)
    initialActionStep = ActionStep(None, None, None, action_sequence.iniState.predicates)
    endActionStep = ActionStep(None, None, action_sequence.endState.predicates, None)

    action_steps.insert(0, initialActionStep)
    action_steps.append(endActionStep)

    # print action_steps[-1].preconditions

    plan = PartialOrderPlan(action_steps, [], action_sequence.iniState, action_sequence.endState)

    for i, action_step in reversed(list(enumerate(action_steps[1:]))):
        for precondition in action_step.preconditions:
            #print precondition
            last_producer = find_last_producer(precondition, action_steps, i)
            plan.add_causal_link(last_producer, action_step, precondition)

    # Add causal links to START for action steps not referenced in any causal link
    add_start_causal_links(plan)

    if resolveThreats:
        resolve_threats(plan)

    return plan



