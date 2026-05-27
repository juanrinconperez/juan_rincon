class Queue:
    """
    Class representing a circular queue with a size limit.

    Attributes:
    -----------
    head : int
        Index of the front element in the queue.
    tail : int
        Index of the last element in the queue.
    """

    def __init__(self, length: int):
        """
        Initializes an empty circular queue with a maximum capacity.

        Parameters:
        -----------
        length : int
            The maximum capacity of the circular queue.
        """
        self.array = [None] * length
        self.head = self.tail = -1
        self.length = length

    def size(self) -> int:
        if self.is_empty():
            return 0
        elif self.tail >= self.head:
            return self.tail - self.head + 1
        else:
            return self.length - (self.head - self.tail - 1)

    def is_full(self) -> bool:
        """
        Checks if the circular queue is full.

        Returns:
        --------
        bool
            True if the circular queue is full, False otherwise.
        """
        if self.is_empty():
            return False
        return (self.tail + 1) % self.length == self.head
    
    def is_empty(self) -> bool:
        """
        Checks if the queue is empty.

        Returns:
        --------
        bool
            True if the queue is empty, False otherwise.
        """
        return self.head == -1 and self.tail == -1

    def enqueue(self, item):
        """
        Adds an element to the circular queue if it is not full.

        Parameters:
        -----------
        item : any type
            The element to add to the circular queue.
        """
        if self.is_full():
            print("Queue is full")
        elif self.head == -1:
            self.head = self.tail = 0
            self.array[self.tail] = item
        else:
            self.tail = (self.tail + 1) % self.length
            self.array[self.tail] = item

    def dequeue(self):
        """
        Removes and returns the front element of the circular queue.

        Returns:
        --------
        any type
            The front element of the circular queue if it is not empty, None otherwise.
        """
        if self.is_empty():
            print("Queue is empty")
            return None
        elif self.head == self.tail:
            temp = self.array[self.head]
            self.array[self.head] = None
            self.head = self.tail = -1
            return temp
        else:
            temp = self.array[self.head]
            self.array[self.head] = None
            self.head = (self.head + 1) % self.length
            return temp

    def show(self):
        """
        Displays the elements of the circular queue in order.
        """
        if self.is_empty():
            print("Queue is empty")
        elif self.tail >= self.head:
            for i in range(self.head, self.tail + 1):
                print(self.array[i], end=" ")
        else:
            for i in range(self.head, self.length):
                print(self.array[i], end=" ")
            for i in range(0, self.tail + 1):
                print(self.array[i], end=" ")
        print()


class Node:
    def __init__(self, key, value=None):
        """
        Initializes a new Node with a key and an optional value.

        Parameters:
        ----------
        key : any
            Unique identifier for the node.
        value : any, optional
            Additional data associated with the node.
        """
        self._parent = None
        self._left = None
        self._right = None
        self.key = key
        self.data = value

    def get_left(self) -> 'Node':
        """
        Retrieves the left child of the node.

        Returns:
        -------
        Node or None
        """
        return self._left

    def set_left(self, node) -> None:
        """
        Sets the left child of the node and updates the parent reference.

        Parameters:
        ----------
        node : Node
        """
        self._left = node
        if node is not None:
            node.set_parent(self)

    def get_right(self) -> 'Node':
        """
        Retrieves the right child of the node.

        Returns:
        -------
        Node or None
        """
        return self._right

    def set_right(self, node) -> None:
        """
        Sets the right child of the node and updates the parent reference.

        Parameters:
        ----------
        node : Node
        """
        self._right = node
        if node is not None:
            node.set_parent(self)

    def get_parent(self) -> 'Node':
        """
        Retrieves the parent of the node.

        Returns:
        -------
        Node or None
        """
        return self._parent

    def set_parent(self, node) -> None:
        """
        Sets the parent of the node.

        Parameters:
        ----------
        node : Node
        """
        self._parent = node

    def __str__(self):
        """
        Returns a string representation of the node (its data).
        """
        return f"{self.data}"

    def show(self, level=0, prefix="Root: ") -> None:
        indent = " " * (level * 4)
        print(f"{indent}{prefix}{self}")

        if self.get_left() is not None:
            self.get_left().show(level + 1, prefix="L--- ")
        if self.get_right() is not None:
            self.get_right().show(level + 1, prefix="R--- ")

    def height(self) -> int:
        """
        For each node explored it adds one to the height and follows the path with the higher height between left and right
        """
        if self.get_left() is None:
            left_depth = -1
        else:
            left_depth = self.get_left().height()

        if self.get_right() is None:
            right_depth = -1
        else:
            right_depth = self.get_right().height()
        
        return 1 + max(left_depth, right_depth)
    
    def find_node(self, key:int) -> "Node":
        """
        Uses the structure of the Binary Trees to see in what place should the searched key be and returns the node
        If it doesn't find it it returns None
        """
        if self.key == key:
            return self
        if key > self.key and self.get_right() is not None:
            return self.get_right().find_node(key)
        if key < self.key and self.get_left() is not None:
            return self.get_left().find_node(key)
        return None
    
    def successor(self) -> "Node":
        """
        Finds the node with the following existing key and returns it
        If it doesn't find it it returns None
        """
        right = self.get_right()
        if right is not None:
            return right.min_key()
        
        current = self
        parent = self.get_parent()

        while parent is not None and current == parent.get_right():
            current = parent
            parent = parent.get_parent()
        
        return parent

    def min_key(self) -> "Node":
        """
        Goes always left to find the lower key node and returns it
        """
        current = self
        while current.get_left() is not None:
            current = current.get_left()
        return current
    
    def max_key(self) -> "Node":
        """
        Goes always right to find the maximum key node and returns it
        """
        current = self
        while current.get_right() is not None:
            current = current.get_right()
        return current
        
    def in_order_show(self) -> None:
        """
        Prints the nodes in key order
        """
        if self.get_left() is not None:
            self.get_left().in_order_show()
        print(self)
        if self.get_right() is not None:
            self.get_right().in_order_show()

    def pre_order_show(self) -> None:
        """
        Prints the nodes in order root-left subtree-right subtree
        """
        print(self)
        if self.get_left() is not None:
            self.get_left().pre_order_show()
        if self.get_right() is not None:
            self.get_right().pre_order_show()

    def post_order_show(self) -> None:
        """
        Prints the nodes in order left subtree-right subtree-root
        """
        if self.get_left() is not None:
            self.get_left().post_order_show()
        if self.get_right() is not None:
            self.get_right().post_order_show()
        print(self)

    def level_order_show(self) -> None:
        """
        Prints the nodes in order by levels from left to right using a queue
        We insert the sons of the node that we print and dequeue it until the queue is empty
        """
        queue = Queue(max(1, 2 ** (self.height() + 1)))
        queue.enqueue(self)
        while not queue.is_empty():
            node = queue.dequeue()
            print(node)
            if node.get_left() is not None:
                queue.enqueue(node.get_left())
            if node.get_right() is not None:
                queue.enqueue(node.get_right())

    def number_descendants(self) -> int:
        """
        For each son that isn't None it adds one to the number of descentands (counter) and does it for the left and right recursively
        Returns the number of descendants (counter)
        """
        counter = 0

        if self.get_left() is not None:
            counter += 1 + self.get_left().number_descendants()

        if self.get_right() is not None:
            counter += 1 + self.get_right().number_descendants()

        return counter
        
    def number_leafs(self) -> int:
        """
        Identifies if the node is a leaf (None sons) and it adds one for each of this case
        """
        counter = 0

        if self.get_left() is None and self.get_right() is None:
            return 1
        
        if self.get_left() is not None:
            counter += self.get_left().number_leafs()
        
        if self.get_right() is not None:
            counter += self.get_right().number_leafs()
    
        return counter
    
    def long_path(self) -> list:
        """
        It  checks if the left subtree has the bigger height or is the right one
        It adds the one that has the bigger high to a list and, recursively it follows that path

        If left is None it will always chose right and viceversa

        It ends when it reaches a lead node
        """
        if self.get_left() is None and self.get_right() is None:
            return []

        if self.get_left() is None:
            return [self.get_right().data] + self.get_right().long_path()

        if self.get_right() is None:
            return [self.get_left().data] + self.get_left().long_path()

        if self.get_left().height() > self.get_right().height():
            return [self.get_left().data] + self.get_left().long_path()
        else:
            return [self.get_right().data] + self.get_right().long_path()

class BinaryTree:
    def __init__(self):
        """
        Initializes the binary tree with no root node.

        Parameters:
        ----------
        root : Node
            The root node of the binary tree.
        """
        self.root = None

    def show(self) -> None:
        """Displays the entire binary tree."""
        if self.root is not None:
            self.root.show()
    
    def height(self) -> int:
        if self.root is None:
            return -1
        return self.root.height()
    
    def find_node(self, key) -> Node | None:
        if self.root is None:
            return None
        return self.root.find_node(key)
    
    def insert_node(self, node: Node) -> None:
        if self.root is None:
            self.root = node
            node.set_parent(None)
            return

        current = self.root

        while current is not None:
            if node.key > current.key:
                if current.get_right() is None:
                    current.set_right(node)
                    return
                current = current.get_right()
            else:
                if current.get_left() is None:
                    current.set_left(node)
                    return
                current = current.get_left()

    def delete_node(self, key) -> bool:
        node = self.find_node(key)
        if node is None:
            return False

        left = node.get_left()
        right = node.get_right()
        parent = node.get_parent()

        if left is None and right is None:
            if parent is None:
                self.root = None
            elif parent.get_left() == node:
                parent.set_left(None)
            else:
                parent.set_right(None)

        elif left is None:
            if parent is None:
                self.root = right
                right.set_parent(None)
            elif parent.get_left() == node:
                parent.set_left(right)
            else:
                parent.set_right(right)

        elif right is None:
            if parent is None:
                self.root = left
                left.set_parent(None)
            elif parent.get_left() == node:
                parent.set_left(left)
            else:
                parent.set_right(left)

        else:
            successor = node.successor()
            node.key = successor.key
            node.data = successor.data

            succ_parent = successor.get_parent()
            succ_right = successor.get_right()

            if succ_parent.get_left() == successor:
                succ_parent.set_left(succ_right)
            else:
                succ_parent.set_right(succ_right)

            if succ_right is not None:
                succ_right.set_parent(succ_parent)

        return True
    
    def skew(self) -> bool:
        node = self.root
        if self.root is None:
            return print("Empty tree")

        if node.get_left() is not None:
            height_left = node.get_left().height()
        else:
            height_left = -1

        if node.get_right() is not None:
            height_right = node.get_right().height()
        else:
            height_right = -1

        return abs(height_right - height_left) > 1
        
    def in_order(self) -> None:
        if self.root is None:
            return
        self.root.in_order_show()

    def pre_order(self) -> None:
        if self.root is None:
            return
        self.root.pre_order_show()

    def post_order(self) -> None:
        if self.root is None:
            return
        self.root.post_order_show()

    def level_order(self) -> None:
        if self.root is None:
            return
        self.root.level_order_show()

    def count_nodes_tree(self) -> int:
        if self.root is None:
            return 0
        return 1 + self.root.number_descendants()

    def count_leafs(self) -> int:
        if self.root is None:
            return 0
        return self.root.number_leafs()
    
    def longest_path(self) -> list:
        if self.root is None:
            return []
        return [self.root.data] + self.root.long_path()
    
    def paths_to_leaf_with_length(self, node:Node, remaining_edges:int, current_path:list[str] = None, results:list[list[str]] = None) -> list[list[str]]:
        """
        Returns all root-to-leaf paths with an exact length (in edges) equal
        to remaining_edges at the beginning of the call.

        Typical usage:
        paths = paths_to_leaf_with_length(tree.root, 3)

        Parameters:
        - node: current node (starts at the root)
        - remaining_edges: number of edges left to reach the target length
        - current_path: (internal) list storing the current path
        - results: (internal) accumulator of valid paths

        Returns:
        - List of paths; each path is a list of strings (str(node.data)).
        """
        if current_path is None:
            current_path = []
        if results is None:
            results = []

        if node is not None and remaining_edges >= 0:
            if current_path == []:
                current_path.append(node.data)

            if remaining_edges == 0 and node.get_left() is None and node.get_right() is None:
                add_solution(current_path, results)
            else:
                for next_node in (node.get_left(), node.get_right()):
                    if not is_None(next_node):
                        remaining_edges = add_to_path(next_node, remaining_edges, current_path)
                        self.paths_to_leaf_with_length(next_node, remaining_edges, current_path, results)
                        remaining_edges = undo_path(remaining_edges, current_path)

        return results

def add_solution(current_path:list[str], results:list[list[str]]) -> None:
    results.append(current_path[:])

def add_to_path(node:Node, remaining_edges:int, current_path:list[str]) -> int:
    current_path.append(node.data)
    return remaining_edges - 1

def undo_path(remaining_edges:int, current_path:list[str]) -> int:
    current_path.pop()
    return remaining_edges + 1

def is_None(node:Node) -> bool:
    return node is None

if __name__ == "__main__":
    tree = BinaryTree()

    print("INSERTANDO NODOS")
    tree.insert_node(Node(10, "diez"))
    tree.insert_node(Node(5, "cinco"))
    tree.insert_node(Node(15, "quince"))
    tree.insert_node(Node(3, "tres"))
    tree.insert_node(Node(7, "siete"))
    tree.insert_node(Node(12, "doce"))
    tree.insert_node(Node(18, "dieciocho"))

    print("\nARBOL")
    tree.show()

    print("\nALTURA")
    print(tree.height())

    print("\nBUSQUEDA")
    print(tree.find_node(7))
    print(tree.find_node(20))

    print("\nRECORRIDOS")
    print("IN ORDER")
    tree.in_order()
    print("PRE ORDER")
    tree.pre_order()
    print("POST ORDER")
    tree.post_order()
    print("LEVEL ORDER")
    tree.level_order()

    print("\nINFORMACION")
    print("Numero de nodos:", tree.count_nodes_tree())
    print("Numero de hojas:", tree.count_leafs())
    print("Camino mas largo:", tree.longest_path())
    print("Caminos de longitud 2:", tree.paths_to_leaf_with_length(tree.root, 2))
    print("Skew:", tree.skew())

    print("\nBORRADO HOJA (3)")
    tree.delete_node(3)
    tree.show()

    print("\nBORRADO NODO CON UN HIJO (5)")
    tree.delete_node(5)
    tree.show()

    print("\nBORRADO NODO CON DOS HIJOS (10)")
    tree.delete_node(10)
    tree.show()

    print("\nRECORRIDOS FINALES")
    print("IN ORDER")
    tree.in_order()
    print("LEVEL ORDER")
    tree.level_order()

    print("\nINFORMACION FINAL")
    print("Numero de nodos:", tree.count_nodes_tree())
    print("Numero de hojas:", tree.count_leafs())
    print("Camino mas largo:", tree.longest_path())