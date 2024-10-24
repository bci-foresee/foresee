import sys

sys.path.append("./")

from app.static.processing_elements.processing_element import ProcessingElement
from signals.parent import Window
import networkx as nx
import matplotlib.pyplot as plt
import os


class Pipeline:

    def __init__(self, input_window: Window) -> None:
        self.elements: list[ProcessingElement] = []
        self.input_window = input_window
        # TODO btrevisan try to get this left to right
        self.visualization = nx.DiGraph()

    def add_elements(self, nodes: list[ProcessingElement]) -> None:
        self.elements += nodes

        # Add the nodes added to our pipeline visualization.
        for pe in nodes:
            self.visualization.add_node(pe.name)

    def add_edge(self, from_node: ProcessingElement,
                 to_node: ProcessingElement) -> None:
        if from_node not in self.elements:
            raise ValueError("node not added to graph")
        if to_node not in self.elements:
            raise ValueError("node not added to graph")

        from_node.add_output(to_node)
        to_node.add_input(from_node)

        # if self.detect_cycle(from_node):
        #     raise ValueError("cycle!")

        self.visualization.add_edge(from_node.name, to_node.name)

    def detect_cycle(self,
                     node: ProcessingElement,
                     visited: set[ProcessingElement] | None = None) -> bool:
        if visited is None:
            visited = set()

        if node in visited:
            return True

        visited.add(node)
        for neighbor in node.children:
            if neighbor == node or self.detect_cycle(neighbor, visited):
                return True

        visited.remove(node)
        return False

    def run(self, window) -> None:
        pass

    def visualize(self):
        print("Graphing")

        node_pos = {"Loader": (0, 0)}

        pos = nx.spring_layout(self.visualization, pos=node_pos)
        node_colors = ['blue'] * len(self.visualization.nodes())
        node_colors[0] = 'red'

        # # Draw the graph with different shapes
        node_sizes = [800 for _ in self.visualization.nodes()]
        nx.draw(self.visualization, pos=pos, with_labels=True, arrows=True, node_color=node_colors, node_size=node_sizes)

        output_dir = 'app/static/pipelines/' + self.name.lower().replace(
            " ", "_") + '/visualizations'

        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # # Save the plot to the specified location
        filepath = os.path.join(output_dir, 'pipeline.png')
        plt.savefig(filepath)
        # # # for pe in self.elements:
