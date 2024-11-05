import sys
import pygraphviz
import subprocess

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
        self.visualization = pygraphviz.AGraph(directed=True, rankdir='LR')

    def add_elements(self, nodes: list[ProcessingElement]) -> None:
        self.elements += nodes

        # Add the nodes added to our pipeline visualization.
        for pe in nodes:
            shape = "circle"
            fillcolor = "blue"
            if pe.name == "Loader":
                shape = "square"
                fillcolor = "red"
            tooltip_text = pe.get_tooltip()
            self.visualization.add_node(pe.name,
                                        shape=shape,
                                        style="filled",
                                        fillcolor=fillcolor,
                                        tooltip=tooltip_text)

    def add_edge(self, from_node: ProcessingElement,
                 to_node: ProcessingElement) -> None:
        if from_node not in self.elements:
            raise ValueError("node not added to graph")
        if to_node not in self.elements:
            raise ValueError("node not added to graph")

        from_node.add_output(to_node)
        to_node.add_input(from_node)

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
        output_dir = 'app/static/pipelines/' + self.name.lower().replace(
            " ", "_") + '/visualizations'

        # Create the output directory if it doesn't exist and save image.
        os.makedirs(output_dir, exist_ok=True)
        dot_filepath = os.path.join(output_dir, 'pipeline.dot')
        png_filepath = os.path.join(output_dir, 'pipeline.svg')
        self.visualization.write(dot_filepath)
        command = ["dot", "-Tsvg", dot_filepath, "-o", png_filepath]
        subprocess.run(command, check=True)
