

from asa.parent import ProcessingElement

from signals.parent import Window

class Pipeline:
    def __init__(self, input_window: Window) -> None:
        self.elements: list[ProcessingElement] = []
        self.input_window = input_window

    def add_elements(self, nodes: list[ProcessingElement]) -> None:
        self.elements += nodes

    def add_edge(self, from_node: ProcessingElement, to_node: ProcessingElement) -> None:
        if from_node not in self.elements:
            raise ValueError("node not added to graph")
        if to_node not in self.elements:
            raise ValueError("node not added to graph")

        from_node.add_output(to_node)
        to_node.add_input(from_node)


        # if self.detect_cycle(from_node):
        #     raise ValueError("cycle!")

    def detect_cycle(self, node: ProcessingElement, visited: set[ProcessingElement] | None = None) -> bool:
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