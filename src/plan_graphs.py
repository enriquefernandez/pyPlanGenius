from third_party import pydot
from partial_order_plan import CausalLink


class PlanGraph:

    def __init__(self, plan):
        # Store plan
        self.plan = plan

        # Create graphviz graph
        self.dot_graph = self.createDotGraph()

    def createDotGraph(self):
        raise NotImplementedError("Class PlanGraph is abstract.")


    def _repr_png_(self):
        return self.dot_graph.create_png()

    def _repr_svg_(self):
        return self.dot_graph.create_svg()

    def save_pdf(self, outputFile):
        self.dot_graph.write_pdf(outputFile)


class PartialOrderGraph(PlanGraph):

    def createDotGraph(self):
        dot_graph = pydot.Dot(graph_name="main_graph",rankdir="TB", labelloc='b',labeljust='r', ranksep=0.5)
        dot_graph.set_node_defaults(shape='rect', fontsize = 12)

        # Create START and END nodes
        start_node = pydot.Node(shape = "ellipse", name = "START", label="<<B>START</B>>", peripheries = 2)
        end_node = pydot.Node(shape = "ellipse", name="GOAL",label="<<B>GOAL</B>>", peripheries = 2)
        dot_graph.add_node(start_node)
        dot_graph.add_node(end_node)

        # Create all the other nodes
        for node in self.plan.nodes:
            node = pydot.Node(name= node.get_grounded_action_description(), label = node.get_dotstyled_action_description())
            dot_graph.add_node(node)

        #start_end_edge = pydot.Edge("START", "END", style="invis")
        #dot_graph.add_edge(start_end_edge)

        # Iterate over causal links
        for causal_link in self.plan.causal_links:
            link_label = str(causal_link.reason_predicate)

            if causal_link.link_type == CausalLink.PClink:
                edge_style = 'solid'
                edge_label = link_label
                edge_color = 'black'
                font_color = 'blue'
            elif causal_link.link_type == CausalLink.TPlink:
                edge_style = 'bold'
                edge_label = '<<FONT COLOR="orange"><B>TP</B></FONT>  : ' + link_label+' >'
                # edge_label = 'TP: ' + link_label
                edge_color = 'orange'
                font_color = 'blue'
            elif causal_link.link_type == CausalLink.TClink:
                edge_style = 'bold'
                edge_label = '<<FONT COLOR="orange"><B>TC</B></FONT>  : ' + link_label+' >'
                #edge_label = 'TC: ' + link_label
                edge_color = 'orange'
                font_color = 'blue'
            elif causal_link.link_type == CausalLink.Startlink:
                edge_style = 'solid'
                edge_label = " "
                edge_color = 'black'
                font_color = 'black'

            #edge = pydot.Edge(causal_link.producer_step.get_grounded_action_description(), causal_link.consumer_step.get_grounded_action_description(), fontsize=12, label = str(causal_link.reason_predicate) if causal_link.reason_predicate else " ")
            edge = pydot.Edge(causal_link.producer_step.get_grounded_action_description(), causal_link.consumer_step.get_grounded_action_description(), fontsize=11, label = edge_label, style = edge_style, fontcolor = font_color, color = edge_color)
            dot_graph.add_edge(edge)

        return dot_graph




class TotalOrderGraph(PlanGraph):

    def createDotGraph(self):

        dot_graph = pydot.Dot(graph_name="main_graph",rankdir="TB", labelloc='b',labeljust='r', ranksep=0.5)
        dot_graph.set_node_defaults(shape='rect', fontsize = 12)

        # Create START and END nodes
        start_node = pydot.Node(shape = "ellipse", name = "START", label="<<B>START</B>>", peripheries = 2)
        end_node = pydot.Node(shape = "ellipse", name="GOAL",label="<<B>GOAL</B>>", peripheries = 2)
        dot_graph.add_node(start_node)
        dot_graph.add_node(end_node)


        fromNode = start_node

        # Create nodes
        for i in range(len(self.plan.actionStepList)):
            #node = pydot.Node(shape = 'record', name="step%d"%i, label = self.plan.actionStepList[i].get_grounded_action_description()+'| {test|dos}', peripheries = 2)
            node = pydot.Node(shape = 'rect', name="step%d"%i, label = self.plan.actionStepList[i].get_dotstyled_action_description())
            dot_graph.add_node(node)
            edge = pydot.Edge(fromNode.get_name(), node.get_name())
            dot_graph.add_edge(edge)
            fromNode = node

        edge = pydot.Edge(fromNode.get_name(), end_node.get_name())
        dot_graph.add_edge(edge)


        # # Add edge from start to first action step
        # #edge = pydot.Edge('START', self.plan.actionStepList[0].get_grounded_action_description())
        # edge = pydot.Edge('START', "step%d"%0)
        # dot_graph.add_edge(edge)
        #
        # #Iterate over action steps
        # for i in range(len(self.plan.actionStepList) - 1):
        #     #edge = pydot.Edge(self.plan.actionStepList[i].get_grounded_action_description(), self.plan.actionStepList[i+1].get_grounded_action_description())
        #     edge = pydot.Edge("step%d"%i, "step%d"%(i+1))
        #     dot_graph.add_edge(edge)
        #
        #
        #
        # # Add final edge from last step to END
        # #edge = pydot.Edge(self.plan.actionStepList[-1].get_grounded_action_description(), 'END')
        # edge = pydot.Edge("step%d"%(len(self.plan.actionStepList) - 1), 'END')
        # dot_graph.add_edge(edge)

        return dot_graph



