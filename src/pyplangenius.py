#!/usr/bin/env python

import argparse
from find_macpo import find_macpo
from action_sequence_builder import ActionSequenceBuilder
from plan_graphs import PartialOrderGraph, TotalOrderGraph


def run_pyplangenius(args):
    asb = ActionSequenceBuilder(args.pddl_domain, args.pddl_problem, False)
    action_sequence, state_sequence = asb.build_action_sequence()

    # Print total order plan
    print "The complete Action Sequence is: "
    print action_sequence

    # Generate total order graph
    total_order_graph = TotalOrderGraph(action_sequence)
    total_order_graph.save_pdf('output_graphs/total_order.pdf')

    print "Action sequence graph saved to: output_graphs/total_order.pdf"

    if not args.no_poplan:
        print "Extracting partial order plan from action sequence (with threat resolution %s)"%('disabled' if args.no_threat_resolution else 'enabled')
        # Obtain partial order plan
        partial_plan = find_macpo(action_sequence, state_sequence, not args.no_threat_resolution)

        # Print partial_plan
        print partial_plan

        # Generate total order graph
        po_graph = PartialOrderGraph(partial_plan)
        po_graph.save_pdf('output_graphs/partial_order.pdf')

        print "Partial Order graph saved to: output_graphs/partial_order.pdf"



    # if args.showgui:
    #     print "Graphical User Interface not developed yet."


if __name__ == '__main__':
    welcome_message =  "Welcome to pyPlanGenius: James Paterson's and Enrique Fernandez's final project for 16.412 Cognitive Robotics.\n"
    welcome_message += "This project implements algorithms for assembling total order plans and extracting partial order plans from them."
    welcome_message += "Please run the project with:\n\tusage: pyplangenius.py [-h] [pddl_domain] [pddl_problem]\n"
    welcome_message += "\n May 2013. Massachusetts Institute of Technology.\n"

    print welcome_message

    argparser = argparse.ArgumentParser(description="Welcome to pyplangenius, James Paterson and Enrique Fernandez 16.412 Final Project.")
    argparser.add_argument("pddl_domain", nargs='?', help="Name of the PDDL domain file stored in the pddl folder.", default="simpleworld-domain.pddl")
    argparser.add_argument("pddl_problem", nargs='?', help= "Name of the PDDL problem file stored in the pddl folder.", default="simpleworld-problem.pddl")
    #argparser.add_argument("--showgui", help="Display GUI", action="store_true")
    argparser.add_argument("--no-poplan", help="Only generate action sequence, but don't extract partial order plan.", action="store_true")
    argparser.add_argument("--no-threat-resolution", help="Generates a partial order plan in which threats are not resolved.", action="store_true")


    run_pyplangenius(argparser.parse_args())
