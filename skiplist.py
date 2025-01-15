import random
from graphviz import Digraph

class Node:
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level, p):
        self.max_level = max_level
        self.p = p
        self.header = Node(-1, max_level)
        self.level = 0

    def random_level(self):
        lvl = 0
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def insert(self, key, visualize=False):
        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        lvl = self.random_level()

        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.header
            self.level = lvl

        new_node = Node(key, lvl)

        for i in range(lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        if visualize:
            self.visualize()

    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]

        current = current.forward[0]
        if current and current.key == key:
            return current
        return None

    def delete(self, key, visualize=False):
        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1

        if visualize:
            self.visualize()

    def range_search(self, low, high):
        results = []
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < low:
                current = current.forward[i]

        current = current.forward[0]

        while current and current.key <= high:
            results.append(current.key)
            current = current.forward[0]

        return results

    def display(self):
        print("\nSkip List:")
        for i in range(self.level + 1):
            current = self.header.forward[i]
            print(f"Level {i}: ", end="")
            while current:
                print(current.key, end=" ")
                current = current.forward[i]
            print("")

    def visualize(self):
        dot = Digraph()
        dot.node(str(self.header.key), f"Header ({self.header.key})")

        # Loop through each level of the Skip List
        for i in range(self.level + 1):
            current = self.header  # Reset to header for each level
            while current.forward[i]:  # Traverse the current level
                next_node = current.forward[i]
                dot.node(str(next_node.key), str(next_node.key))
                dot.edge(str(current.key), str(next_node.key), label=f"Level {i}")
                current = next_node

        dot.render("skiplist", format="png", cleanup=True)
        print("Skip List visualized as skiplist.png")

# Example usage
if __name__ == "__main__":
    skiplist = SkipList(max_level=4, p=0.5)

    for num in [3, 6, 7, 9, 12, 19, 17, 26, 21]:
        skiplist.insert(num, visualize=True)

    skiplist.display()

    print("\nSearching for 19:", "Found" if skiplist.search(19) else "Not Found")

    print("\nDeleting 19")
    skiplist.delete(19, visualize=True)
    skiplist.display()

    print("\nRange search [6, 21]:", skiplist.range_search(6, 21))
