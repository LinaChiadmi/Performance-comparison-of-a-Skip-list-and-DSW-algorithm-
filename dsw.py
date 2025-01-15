import graphviz
import numpy as np  

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = np.array([None, None], dtype=object)  # [left, right]

    def __repr__(self):
        return f"TreeNode({self.value})"

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = TreeNode(value)
        else:
            self._insert_rec(self.root, value)

    def _insert_rec(self, node, value):
        if value < node.value:
            if node.children[0] is None:
                node.children[0] = TreeNode(value)
            else:
                self._insert_rec(node.children[0], value)
        else:
            if node.children[1] is None:
                node.children[1] = TreeNode(value)
            else:
                self._insert_rec(node.children[1], value)
    
    def search(self, value):
        return self._search_rec(self.root, value)

    def _search_rec(self, node, value):
        if not node:
            return None
        if node.value == value:
            return node
        elif value < node.value:
            return self._search_rec(node.children[0], value)
        else:
            return self._search_rec(node.children[1], value)
        
    def delete(self, value):
        self.root = self._delete_rec(self.root, value)

    def _delete_rec(self, node, value):
        if not node:
            return node

        if value < node.value:
            node.children[0] = self._delete_rec(node.children[0], value)
        elif value > node.value:
            node.children[1] = self._delete_rec(node.children[1], value)
        else:
            if not node.children[0] and not node.children[1]:
                return None
            if not node.children[0]:
                return node.children[1]
            elif not node.children[1]:
                return node.children[0]

            min_larger_node = self._get_min(node.children[1])
            node.value = min_larger_node.value
            node.children[1] = self._delete_rec(node.children[1], min_larger_node.value)

        return node

    def _get_min(self, node):
        current = node
        while current.children[0]:
            current = current.children[0]
        return current

    def generate_graphviz(self):
        dot = graphviz.Digraph()
        
        def add_nodes_edges(node):
            if not node:
                return
            dot.node(str(id(node)), str(node.value))
            if node.children[0]:
                dot.edge(str(id(node)), str(id(node.children[0])))
                add_nodes_edges(node.children[0])
            if node.children[1]:
                dot.edge(str(id(node)), str(id(node.children[1])))
                add_nodes_edges(node.children[1])
        
        add_nodes_edges(self.root)
        return dot

    def perform_dsw(self):
        print("Tree before DSW:\n")
        self.generate_graphviz().render("tree_before_dsw", format="png", cleanup=True)

        self.create_backbone()
        print("Backbone created:\n")
        self.generate_graphviz().render("backbone", format="png", cleanup=True)

        self.balance_tree()
        print("Balanced tree:\n")
        self.generate_graphviz().render("balanced_tree", format="png", cleanup=True)

    def create_backbone(self):
        pseudo_root = TreeNode(0)
        pseudo_root.children[1] = self.root
        current = pseudo_root

        while current.children[1]:
            if current.children[1].children[0]:
                self.rotate_right(current)
            else:
                current = current.children[1]

        self.root = pseudo_root.children[1]

    def rotate_right(self, parent):
        child = parent.children[1]
        parent.children[1] = child.children[0]
        child.children[0] = parent.children[1].children[1]
        parent.children[1].children[1] = child

    def balance_tree(self):
        n = self.get_size()
        m = (2 ** (n.bit_length() - 1)) - 1
        self.perform_rotations(n - m)

        while m > 1:
            m //= 2
            self.perform_rotations(m)

    def perform_rotations(self, count):
        parent = TreeNode(0)
        parent.children[1] = self.root
        current = parent

        for _ in range(count):
            if not current.children[1] or not current.children[1].children[1]:
                break  # Avoid invalid rotations
            self.rotate_left(current)
            current = current.children[1]

        self.root = parent.children[1]

    def rotate_left(self, parent):
        if not parent.children[1] or not parent.children[1].children[1]:
            return  # Skip rotation if there are no nodes to rotate

        child = parent.children[1]
        parent.children[1] = child.children[1]
        child.children[1] = parent.children[1].children[0]
        parent.children[1].children[0] = child

    def get_size(self):
        def count_nodes(node):
            if not node:
                return 0
            return 1 + count_nodes(node.children[0]) + count_nodes(node.children[1])

        return count_nodes(self.root)
    
    def range_search(self, low, high):
        results = []
        self._range_search_rec(self.root, low, high, results)
        return results

    def _range_search_rec(self, node, low, high, results):
        if not node:
            return

        if low <= node.value <= high:
            results.append(node.value)

        if node.value > low:
            self._range_search_rec(node.children[0], low, high, results)

        if node.value < high:
            self._range_search_rec(node.children[1], low, high, results)


# Example usage
if __name__ == "__main__":
    tree = BinaryTree()
    values = [10, 5, 3, 2, 1, 15, 20]
    for val in values:
        tree.insert(val)

    print("Original Tree Visualization:")
    dot = tree.generate_graphviz()
    dot.render("original_tree", format="png", cleanup=True)

    tree.perform_dsw()

    print("Balanced Tree Visualization:")
    balanced_dot = tree.generate_graphviz()
    balanced_dot.render("balanced_tree", format="png", cleanup=True)
