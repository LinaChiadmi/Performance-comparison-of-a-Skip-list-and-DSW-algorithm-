import graphviz

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

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
            if node.left:
                self._insert_rec(node.left, value)
            else:
                node.left = TreeNode(value)
        else:
            if node.right:
                self._insert_rec(node.right, value)
            else:
                node.right = TreeNode(value)
    
    def search(self, value):
        return self._search_rec(self.root, value)

    def _search_rec(self, node, value):
        if not node:  # If the node is None, value is not found
            return None
        if node.value == value:
            return node
        elif value < node.value:
            return self._search_rec(node.left, value)
        else:
            return self._search_rec(node.right, value)
        
    def delete(self, value):
        self.root = self._delete_rec(self.root, value)

    def _delete_rec(self, node, value):
        if not node:
            return node

        # Find the node to delete
        if value < node.value:
            node.left = self._delete_rec(node.left, value)
        elif value > node.value:
            node.right = self._delete_rec(node.right, value)
        else:
            # Node to delete is found

            # Case 1: Node has no children (leaf node)
            if not node.left and not node.right:
                return None

            # Case 2: Node has one child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Case 3: Node has two children
            min_larger_node = self._get_min(node.right)
            node.value = min_larger_node.value  # Replace node with its in-order successor
            node.right = self._delete_rec(node.right, min_larger_node.value)

        return node

    def _get_min(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def generate_graphviz(self):
        dot = graphviz.Digraph()
        
        def add_nodes_edges(node):
            if not node:
                return
            dot.node(str(id(node)), str(node.value))
            if node.left:
                dot.edge(str(id(node)), str(id(node.left)))
                add_nodes_edges(node.left)
            if node.right:
                dot.edge(str(id(node)), str(id(node.right)))
                add_nodes_edges(node.right)
        
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
        pseudo_root.right = self.root
        current = pseudo_root

        while current.right:
            if current.right.left:
                self.rotate_right(current)
            else:
                current = current.right

        self.root = pseudo_root.right

    def rotate_right(self, parent):
        child = parent.right
        parent.right = child.left
        child.left = parent.right.right
        parent.right.right = child

    def balance_tree(self):
        n = self.get_size()
        m = (2 ** (n.bit_length() - 1)) - 1

        self.perform_rotations(n - m)

        while m > 1:
            m //= 2
            self.perform_rotations(m)

    def perform_rotations(self, count):
        parent = TreeNode(0)
        parent.right = self.root
        current = parent

        for _ in range(count):
            if not current.right or not current.right.right:
                break  # Avoid invalid rotations
            self.rotate_left(current)
            current = current.right

        self.root = parent.right


    def rotate_left(self, parent):
        if not parent.right or not parent.right.right:
            return  # Skip rotation if there are no nodes to rotate

        child = parent.right
        parent.right = child.right
        child.right = parent.right.left
        parent.right.left = child


    def get_size(self):
        def count_nodes(node):
            if not node:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)

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
            self._range_search_rec(node.left, low, high, results)

        if node.value < high:
            self._range_search_rec(node.right, low, high, results)

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
